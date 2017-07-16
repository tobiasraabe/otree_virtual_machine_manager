# -*- coding: utf-8 -*-

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor

from ovmm.config.settings import PORT_RANGES, PSQL_CONN, PSQL_TABLE


class PostgreSQLDatabaseHandler:
    """This class contains all functions related to the PostgreSQL database
    which contains information about users.

    The main objectives are port handling so that every user receives distinct
    ports and, second, user information.

    Note
    ----
    The table contains the following columns:
    full_name : str
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
    ssl_port : smallint
        SSL port
    redis_port : smallint
        Redis port

    """

    def __init__(self):
        """Tries to connect to database to test the connection. If the user
        table does not exist, it is created.

        Raises
        ------
        psycopg2.OperationalError
            If connection to PostgreSQL database fails
        psycopg2.ProgrammingError
            If table does not exist in the database
        """

        try:
            self.check_connection()
        except psycopg2.OperationalError as ee:
            click.secho(
                'ERROR: Cannot connect to PostgreSQL server! You better check'
                ' the connection manually!', fg='red')
            raise ee
        except psycopg2.ProgrammingError as eee:
            err_msg_1 = 'relation "{}" does not exist'.format(PSQL_TABLE)
            err_msg_2 = 'INSERT has more expressions than target columns'
            if eee.diag.message_primary == err_msg_1:
                click.secho('ERROR: The user table does not exist!', fg='red')
                self.create_table()
                self.check_connection()
                click.secho('SUCCESS: The table was created.', fg='green')
            elif eee.diag.message_primary == err_msg_2:
                click.secho(
                    'ERROR: A table {} exists which is not properly defined.\n'
                    'Check it manually!'.format(PSQL_TABLE), fg='red')
                raise eee
            else:
                raise eee
        else:
            click.secho(
                'SUCCESS: Connection to database and table.', fg='green')

    @staticmethod
    def check_connection():
        """The function tries to connect to the PostgreSQL database and write
        a test entry. This test covers the case where `user_table` is defined
        but it is not properly set up.

        """

        with psycopg2.connect(**PSQL_CONN) as conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO {} VALUES ('test', 'test', 'test',
                        'test', 'test', '11111', '11111',  '11111');"""
                        .format(PSQL_TABLE))
            conn.rollback()
        conn.close()

    @staticmethod
    def create_table():
        """Creates user table in the postgres database with entries mentioned
        in the class docstring.

        """

        with psycopg2.connect(**PSQL_CONN) as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE {} (full_name TEXT NOT NULL,
                        user_name TEXT PRIMARY KEY, email TEXT NOT NULL,
                        telephone TEXT NOT NULL, password TEXT NOT NULL,
                        daphne_port SMALLINT UNIQUE,
                        ssl_port SMALLINT UNIQUE,
                        redis_port SMALLINT UNIQUE);"""
                        .format(PSQL_TABLE))
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
            cur.execute("""SELECT {} FROM {};"""
                        .format(port_name, PSQL_TABLE))
            ports_list = cur.fetchall()
        conn.close()

        return ports_list

    def get_free_ports(self, port_name: str):
        """Compares ports from user table with ports from ``ovmm_conf.yml``
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
        free_ports = [i for i in PORT_RANGES[port_name] if i not in ports_arr]

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
        for port_name in PORT_RANGES.keys():
            num1 = len(self.get_free_ports(port_name))
            if (num1 < num_free_ports) | (num_free_ports is None):
                num_free_ports = num1
            num2 = len(PORT_RANGES[port_name])
            if (num2 < num_max_ports) | (num_max_ports is None):
                num_max_ports = num2

        return num_free_ports, num_max_ports

    @staticmethod
    def get_user(user_name: str):
        """Returns a user entry from PostgreSQL table.

        Returns
        -------
        dict_user : dict
            A dictionary with user information

        """

        with psycopg2.connect(cursor_factory=RealDictCursor,
                              **PSQL_CONN) as conn:
            dict_cur = conn.cursor()
            dict_cur.execute(
                """SELECT * FROM {} WHERE user_name = '{}';"""
                .format(PSQL_TABLE, user_name))
            dict_user = dict_cur.fetchone()
        conn.close()

        return dict_user

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

        Raises
        ------
        psycopg2.IntegrityError
            If the user entry already exists in the database

        """

        for port_name in PORT_RANGES.keys():
            dict_user[port_name] = min(self.get_free_ports(port_name))

        with psycopg2.connect(**PSQL_CONN) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            # First, to catch multiple accounts.
            try:
                cur.execute("""INSERT INTO {} VALUES (%(full_name)s,
                            %(user_name)s, %(email)s, %(telephone)s,
                            %(password)s, %(daphne_port)s,
                            %(ssl_port)s, %(redis_port)s);"""
                            .format(PSQL_TABLE), dict_user)
            except psycopg2.IntegrityError:
                click.secho(
                    'ERROR: User account {user_name} already exists.'
                    .format(**dict_user), fg='red')
                raise
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

        """

        with psycopg2.connect(**PSQL_CONN) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute("""DELETE FROM {} WHERE user_name = '{}';"""
                        .format(PSQL_TABLE, user_name))
            cur.execute("""DROP DATABASE {};""".format(user_name))
            cur.execute("""DROP ROLE {};""".format(user_name))
        conn.close()

        click.secho('SUCCESS: User {} was removed from database.'
                    .format(user_name), fg='green')

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
            cur.execute("""SELECT user_name FROM {};"""
                        .format(PSQL_TABLE))
            user_arr = cur.fetchall()
        conn.close()

        user_list = [i[0] for i in user_arr]

        return user_list
