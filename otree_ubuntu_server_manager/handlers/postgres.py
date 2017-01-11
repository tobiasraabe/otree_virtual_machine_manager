#!/usr/bin/env python3

"""This document contains everything related to PSQL operations.

- **Critical parts**:
    - every function tries to establish its own connection. I'm sure that this
    is cleaner to some extend since one can use the `with`-statement and
    `connect`. If a with statement exits without errors, the changes are
    automatically committed and the connection is closed. If an error occurs,
    the changes are reverted.
    - add last_activity to the user_database and other keys (paper)
    - `dict_login` can be written into the main file

"""

import click
import psycopg2
import sys

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from ousm_settings import POSTGRES_CONNECTION as psql_conn
from ousm_settings import POSTGRES_MISC as psql_misc


class PostgreSQLDatabaseHandler(object):
    """This class contains all functions related to the PostgreSQL database
    containing information about users.

    - The functions are::

        :__init__:          Checks if connection to database is successful. If
                            the database does not exist, it is created.
        :_check_connection: Check connection to postgres and user table
        :_create_table:     Creates table for user accounts
        :_get_used_ports:   Returns a list of all ports, already in use
        :_get_free_ports:   Returns the lowest daphne port number which is not
                            already used.
        :count_user:        Returns the number of entries in the table.
        :create_user:       Creates a new entry in the table for user accounts
        :delete_user:       Deletes a user from user table

    """

    def __init__(self):
        """Tries to connect to database to test the connection. If the user
        table does not exist, it is created."""
        try:
            click.echo('Trying to connect to the database and user table')
            self._check_connection()
        except psycopg2.OperationalError:
            click.secho('Cannot connect to PostgreSQL server! You better '
                        'check the connection manually!', fg='red')
            sys.exit(0)
        except psycopg2.ProgrammingError as e:
            click.secho(
                'The user table does not exist! This happens usually if '
                'you run the script for the first time. If you want to '
                'include existing user with the user database, check out '
                '[placeholder] script.', fg='red')
            try:
                self._create_table()
                self._check_connection()
            except Exception as e:
                click.secho(
                    'SCRIPT EXITED HERE BECAUSE OF:\n{}\n\n'
                    'This happens sometimes, e.g. if you have changed the\n'
                    'configuration of the user table in postgres.py, but did\n'
                    'not drop the old table. Currently, there is no function\n'
                    'to convert tables. DIY!', fg='red')
                sys.exit(0)
        else:
            click.secho(
                'The connection to the PostgreSQL database was successful!',
                fg='green')

    def _check_connection(self):
        """The function tries to connect to the postgres database and to write
        a test entry. This test covers the case where `user_table` is defined
        but it is not properly set up."""

        with psycopg2.connect(**psql_conn) as conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO {table} VALUES ('test', 'test', 'test',
                        'test', 'test', '11111', '11111', '11111', '11111');"""
                        .format(**psql_misc))
            conn.rollback()
        conn.close()

    def _create_table(self):
        """Creates user table in the postgres database"""

        with psycopg2.connect(**psql_conn) as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE {table} (name TEXT NOT NULL,
                        user_name TEXT PRIMARY KEY, email TEXT NOT NULL,
                        telephone TEXT NOT NULL, password TEXT NOT NULL,
                        daphne_port SMALLINT UNIQUE,
                        http_port SMALLINT UNIQUE,
                        ssl_port SMALLINT UNIQUE,
                        redis_port SMALLINT UNIQUE);"""
                        .format(**psql_misc))
        conn.close()

    def _get_used_ports(self, port_name):
        """Returns a list of all ports for *port_name* from table."""

        ports_arr = None
        with psycopg2.connect(**psql_conn) as conn:
            cur = conn.cursor()
            cur.execute("""SELECT {} FROM {table};"""
                        .format(port_name, **psql_misc))
            ports_arr = cur.fetchall()
        conn.close()

        return ports_arr

    def _get_free_ports(self, port_name):
        """Compares ports from user table with ports from ousm_settings.py
        and returns a list of free ports for a given *port_name*."""

        arr = self._get_used_ports(port_name)
        ports_arr = [int(i[0]) for i in arr]
        free_ports_arr = [i for i in psql_misc[port_name]
                          if i not in ports_arr]

        return free_ports_arr

    def count_user(self):
        """Returns the number of entries in the table."""

        num_free_ports = 10000
        num_max_ports = 10000
        for port_name in ['daphne_port', 'http_port', 'ssl_port',
                          'redis_port']:
            num1 = len(self._get_free_ports(port_name))
            if (num1 < num_free_ports) | (num_free_ports is None):
                num_free_ports = num1
            num2 = len(psql_misc[port_name])
            if (num2 < num_max_ports) | (num_max_ports is None):
                num_max_ports = num2

        click.echo('Number of user accounts: {}'
                   .format(num_max_ports - num_free_ports))
        click.echo('Limit of additional accounts: {}'.format(num_free_ports))
        if num_free_ports == 0:
            click.secho('It is not possible to add more users!', fg='red')

    def create_user(self, dict_user):
        """Creates a user and adds information to user database"""

        for port_name in ['daphne_port', 'http_port', 'ssl_port',
                          'redis_port']:
            dict_user[port_name] = min(self._get_free_ports(port_name))

        with psycopg2.connect(**psql_conn) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            # First, to catch multiple accounts.
            try:
                cur.execute("""INSERT INTO {table} VALUES (%(user_full)s,
                            %(user_name)s, %(user_email)s, %(user_tel)s,
                            %(password)s, %(daphne_port)s, %(http_port)s,
                            %(ssl_port)s, %(redis_port)s);"""
                            .format(**psql_misc), dict_user)
            except psycopg2.IntegrityError:
                click.secho(
                    'The user {user_name} already exists. Please check the '
                    'existing account or delete it by executing delete_user.py'
                    .format(**dict_user), fg='red')
                sys.exit(0)
            # Second because the other is first.
            cur.execute("""CREATE USER {user_name};""".format(**dict_user))
            cur.execute("""ALTER USER {user_name} WITH PASSWORD
                        '{password}';""".format(**dict_user))
            cur.execute("""CREATE DATABASE {user_name};""".format(**dict_user))
            cur.execute("""ALTER DATABASE {user_name} OWNER TO
                        {user_name};""".format(**dict_user))
        conn.close()

        return dict_user

    def delete_user(self, user_name):
        """Deletes a user's database, role and removes the entry from the user
        database. Returns the http_port variable to deny access to ports."""

        http_port = None
        ssl_port = None
        with psycopg2.connect(**psql_conn) as conn:
            cur = conn.cursor()
            cur.execute("""SELECT http_port, ssl_port FROM {}
                        WHERE user_name = '{}';"""
                        .format(psql_misc['table'], user_name))
            http_port, ssl_port = cur.fetchone()
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            cur.execute("""DELETE FROM {} WHERE user_name = '{}';"""
                        .format(psql_misc['table'], user_name))
            cur.execute("""DROP DATABASE {};""".format(user_name))
            cur.execute("""DROP ROLE {};""".format(user_name))
        conn.close()

        click.secho('User {} was successfully removed from postgres server.'
                   .format(user_name), fg='green')

        return int(http_port), int(ssl_port)

    def list_user(self):
        with psycopg2.connect(**psql_conn) as conn:
            cur = conn.cursor()
            cur.execute("""SELECT user_name FROM {table};"""
                        .format(**psql_misc))
            user_arr = cur.fetchall()
            click.echo('\nList of user names:\n')
            for i in user_arr:
                click.echo(i[0])
        conn.close()
