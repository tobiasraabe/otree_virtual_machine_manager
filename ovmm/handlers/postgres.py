# -*- coding: utf-8 -*-

import ast
import os
import sys

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    from ovmm_settings import POSTGRES_CONNECTION as PSQL_CONN
    from ovmm_settings import POSTGRES_MISC as PSQL_MISC
except ImportError:
    try:
        PSQL_CONN = ast.literal_eval(os.environ['PSQL_CONN'])
        PSQL_MISC = ast.literal_eval(os.environ['PSQL_MISC'])
    except KeyError:
        pass


class PostgreSQLDatabaseHandler:
    """This class contains all functions related to the PostgreSQL database
    which contains information about users.

    The main objectives are port handling so that every user receives distinct
    ports and, second, user information.

    Note
    ----
    The table contains the following columns:
    name : str
        Full name of user
    user_name : str
        Name of the account
    email : str
        Email address of user
    telephone : str
        Telephone number of user
    password : str
        Password of user account (PostgreSQL, Samba)
    daphne_port : smallint
        Daphne port
    http_port : smallint
        HTTP port
    ssl_port : smallint
        SSL port
    redis_port : smallint
        Redis port

    Attributes
    ----------
    port_name_list : List[str]
        List of variable names for port names in database

    """

    port_name_list = ['daphne_port', 'http_port', 'ssl_port', 'redis_port']

    def __init__(self):
        """Tries to connect to database to test the connection. If the user
        table does not exist, it is created.

        """

        try:
            self.check_connection()
        except psycopg2.OperationalError as e:
            click.secho(e, fg='red')
            click.secho('Cannot connect to PostgreSQL server! You better '
                        'check the connection manually!', fg='red')
            sys.exit(1)
        except psycopg2.ProgrammingError as e:
            click.secho(e, fg='red')
            click.secho('The user table does not exist!\n\n{}', fg='red')
            try:
                self.create_table()
                self.check_connection()
            except Exception as e:
                click.secho(e, fg='red')
                sys.exit(1)
        else:
            click.secho(
                'The connection to the PostgreSQL database was successful!',
                fg='green')

    @staticmethod
    def check_connection():
        """The function tries to connect to the PostgreSQL database and write
        a test entry. This test covers the case where `user_table` is defined
        but it is not properly set up.

        """

        with psycopg2.connect(**PSQL_CONN) as conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO {table} VALUES ('test', 'test', 'test',
                        'test', 'test', '11111', '11111', '11111', '11111');"""
                        .format(**PSQL_MISC))
            conn.rollback()
        conn.close()

    @staticmethod
    def create_table():
        """Creates user table in the postgres database with entries mentioned
        in the class docstring.

        """

        with psycopg2.connect(**PSQL_CONN) as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE {table} (name TEXT NOT NULL,
                        user_name TEXT PRIMARY KEY, email TEXT NOT NULL,
                        telephone TEXT NOT NULL, password TEXT NOT NULL,
                        daphne_port SMALLINT UNIQUE,
                        http_port SMALLINT UNIQUE,
                        ssl_port SMALLINT UNIQUE,
                        redis_port SMALLINT UNIQUE);"""
                        .format(**PSQL_MISC))
        conn.close()

    @staticmethod
    def get_used_ports(port_name: str):
        """Returns a list of all used ports for `port_name` from table.

        Parameters
        ----------
        port_name : str
            One of the port names described in class docstring

        Returns
        -------
        ports_list : List[str]
            List of port numbers for a given port name

        """

        with psycopg2.connect(**PSQL_CONN) as conn:
            cur = conn.cursor()
            cur.execute("""SELECT {} FROM {table};"""
                        .format(port_name, **PSQL_MISC))
            ports_list = cur.fetchall()
        conn.close()

        return ports_list

    def get_free_ports(self, port_name: str):
        """Compares ports from user table with ports from ``ovmm_settings.py``
        and returns a list of free ports for a given `port_name`.

        Paramters
        ---------
        port_name : str
            One of the port names described in the class docstring

        Returns
        -------
        free_ports : List[str]
            List of unassigned ports for a given port name

        """

        arr = self.get_used_ports(port_name)
        ports_arr = [int(i[0]) for i in arr]
        free_ports = [i for i in PSQL_MISC[port_name] if i not in ports_arr]

        return free_ports

    def count_user(self):
        """Returns the number possible additional accounts and the maximal
        number of accounts.

        Returns
        -------
        num_free_ports : int
            Number of possible, additional accounts
        num_max_ports : int
            Maximal number of accounts given information about ports

        """

        num_free_ports = 10000
        num_max_ports = 10000
        for port_name in self.port_name_list:
            num1 = len(self.get_free_ports(port_name))
            if (num1 < num_free_ports) | (num_free_ports is None):
                num_free_ports = num1
            num2 = len(PSQL_MISC[port_name])
            if (num2 < num_max_ports) | (num_max_ports is None):
                num_max_ports = num2

        return num_free_ports, num_max_ports

    def create_user(self, dict_user: dict) -> dict:
        """Gets the minimal unassigned port numbers, adds them to the
        dictionary of user information. After adding the user to the table,
        the extended dictionary is returned.

        Parameters
        ----------
        dict_user : dict
            A dict of user information containing port numbers

        Returns
        -------
        dict_user : dict
            Input dictionary extended by port entries

        """

        for port_name in self.port_name_list:
            dict_user[port_name] = min(self.get_free_ports(port_name))

        with psycopg2.connect(**PSQL_CONN) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            # First, to catch multiple accounts.
            try:
                cur.execute("""INSERT INTO {table} VALUES (%(user_full)s,
                            %(user_name)s, %(user_email)s, %(user_tel)s,
                            %(password)s, %(daphne_port)s, %(http_port)s,
                            %(ssl_port)s, %(redis_port)s);"""
                            .format(**PSQL_MISC), dict_user)
            except psycopg2.IntegrityError:
                click.secho(
                    'The user account {user_name} already exists.'
                    .format(**dict_user), fg='red')
                sys.exit(1)
            # Second because the other is first.
            cur.execute("""CREATE USER {user_name};""".format(**dict_user))
            cur.execute("""ALTER USER {user_name} WITH PASSWORD
                        '{password}';""".format(**dict_user))
            cur.execute("""CREATE DATABASE {user_name};""".format(**dict_user))
            cur.execute("""ALTER DATABASE {user_name} OWNER TO
                        {user_name};""".format(**dict_user))
        conn.close()

        return dict_user

    @staticmethod
    def delete_user(user_name: str):
        """Deletes a user's database, role and removes the entry from the user
        database. Returns the `http_port` variable to deny access to ports.

        Parameters
        ----------
        user_name : str
            Name of user account

        Returns
        -------
        http_port : int
            User's http port
        ssl_port : int
            User's ssl port

        """

        with psycopg2.connect(**PSQL_CONN) as conn:
            cur = conn.cursor()
            cur.execute("""SELECT http_port, ssl_port FROM {}
                        WHERE user_name = '{}';"""
                        .format(PSQL_MISC['table'], user_name))
            try:
                http_port, ssl_port = cur.fetchone()
            except TypeError:
                click.secho(
                    '{} does not exist in the database!', fg='red'
                )
                sys.exit(1)

            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur.execute("""DELETE FROM {} WHERE user_name = '{}';"""
                        .format(PSQL_MISC['table'], user_name))
            cur.execute("""DROP DATABASE {};""".format(user_name))
            cur.execute("""DROP ROLE {};""".format(user_name))
        conn.close()

        click.secho('User {} was successfully removed from postgres server.'
                    .format(user_name), fg='green')

        return int(http_port), int(ssl_port)

    @staticmethod
    def list_user():
        """This functions echoes a list of user names to shell.

        Returns
        -------
        user_list : list
            List of user names

        """

        with psycopg2.connect(**PSQL_CONN) as conn:
            cur = conn.cursor()
            cur.execute("""SELECT user_name FROM {table};"""
                        .format(**PSQL_MISC))
            user_arr = cur.fetchall()
        conn.close()
        user_list = [i[0] for i in user_arr]

        return user_list
