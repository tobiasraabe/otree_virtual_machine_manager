"""This module contains all tests related to postgres."""

import sys

import psycopg2
import pytest

from ovmm.config.environment import PSQL_CONN, PSQL_TABLE
from ovmm.handlers import postgres
from ovmm.prompts.defaults import DUMMY_USERS

# Variable is used to skip postgres tests if not on Ubuntu
pytestmark = pytest.mark.skipif(
    sys.platform != 'linux',
    reason='Tests for linux with PostgreSQL database only')
# Implement a skip if PostgreSQL is not installed.


@pytest.mark.order1
def test_check_connection_1():
    """Test whether the connection to the database cannot be established."""
    with pytest.raises(psycopg2.ProgrammingError):
        postgres.PostgreSQLDatabaseHandler.check_connection()


@pytest.mark.order2
def test_create_table():
    """Test whether the table can be created."""
    postgres.PostgreSQLDatabaseHandler.create_table()

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT EXISTS (
            SELECT 1
            FROM pg_tables
            WHERE tablename = '{}');""".format(PSQL_TABLE))
        table_name = cur.fetchone()
        assert table_name[0]
    conn.close()


@pytest.mark.order3
def test_check_connection_2():
    """Test whether a connection to the user database can be established."""
    postgres.PostgreSQLDatabaseHandler.check_connection()


@pytest.mark.order4
def test_create_user_1():
    """Test whether a user can be created."""
    psql = postgres.PostgreSQLDatabaseHandler()
    DUMMY_USERS['werner'].update({'password': '1234'})
    psql.create_user(DUMMY_USERS['werner'])

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {}
            WHERE user_name = '{user_name}';"""
            .format(PSQL_TABLE, **DUMMY_USERS['werner']))
        user = cur.fetchone()
        for i in user:
            assert i in DUMMY_USERS['werner'].values()
    conn.close()


@pytest.mark.order5
def test_count_user_1():
    """Test whether free port are correctly counted."""
    psql = postgres.PostgreSQLDatabaseHandler()
    num_free, num_max = psql.count_user()
    assert num_free == 19
    assert num_max == 20


@pytest.mark.order6
def test_create_user_2():
    """Test whether a second user can be created."""
    psql = postgres.PostgreSQLDatabaseHandler()
    DUMMY_USERS['max_born'].update({'password': '98765'})
    psql.create_user(DUMMY_USERS['max_born'])

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {}
            WHERE user_name = '{user_name}';"""
            .format(PSQL_TABLE, **DUMMY_USERS['max_born']))
        user = cur.fetchone()
        for i in user:
            assert i in DUMMY_USERS['max_born'].values()
    conn.close()


@pytest.mark.order7
def test_create_duplicate_user():
    """Test whether a duplicated user cannot be created."""
    psql = postgres.PostgreSQLDatabaseHandler()
    DUMMY_USERS['max_born'].update({'password': '98765'})
    with pytest.raises(psycopg2.IntegrityError):
        psql.create_user(DUMMY_USERS['max_born'])


@pytest.mark.order8
def test_count_user_2():
    """Test whether free ports are correctly counted."""
    psql = postgres.PostgreSQLDatabaseHandler()
    num_free, num_max = psql.count_user()
    assert num_free == 18
    assert num_max == 20


@pytest.mark.order9
def test_list_user():
    """Test whether a complete list of users can be printed."""
    user_list = postgres.PostgreSQLDatabaseHandler.list_user()
    assert 'werner' in user_list
    assert 'max_born' in user_list


@pytest.mark.order10
def test_get_user():
    """Test whether user information can be queried from the table."""
    dict_user = postgres.PostgreSQLDatabaseHandler.get_user(
        DUMMY_USERS['werner']['user_name'])
    for key in DUMMY_USERS['werner'].keys():
        assert dict_user[key] == DUMMY_USERS['werner'][key]


@pytest.mark.order11
def test_delete_user():
    """Test whether a user can be deleted."""
    postgres.PostgreSQLDatabaseHandler.delete_user(
        DUMMY_USERS['werner']['user_name'])

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {}
            WHERE user_name = '{user_name}';"""
            .format(PSQL_TABLE, **DUMMY_USERS['werner']))
        temp = cur.fetchone()
        assert temp is None
    conn.close()

# Exclude for now. Don't know why password is not changed within the first
# with statement
# @pytest.mark.order12
# def test_init_missing_connection():
#     password = 'test'
#     with psycopg2.connect(**PSQL_CONN) as conn:
#         cur = conn.cursor()
#         cur.execute("""ALTER USER postgres WITH PASSWORD '{}';"""
#                     .format(password))
#     conn.close()
#
#     with pytest.raises(psycopg2.OperationalError):
#         postgres.PostgreSQLDatabaseHandler()
#
#     with psycopg2.connect(password=password, **PSQL_CONN) as conn:
#         cur = conn.cursor()
#         cur.execute("""ALTER USER postgres WITH PASSWORD '';""")
#     conn.close()


@pytest.mark.order13
def test_init_missing_table():
    """Test whether a table can be dropped or created."""
    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute("""DROP TABLE {};"""
                    .format(PSQL_TABLE))

        cur.execute(
            """SELECT EXISTS (
            SELECT 1
            FROM pg_tables
            WHERE tablename = '{}');""".format(PSQL_TABLE))
        table_name = cur.fetchone()
        assert table_name[0] == 0
    conn.close()

    postgres.PostgreSQLDatabaseHandler()

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT EXISTS (
            SELECT 1
            FROM pg_tables
            WHERE tablename = '{}');""".format(PSQL_TABLE))
        table_name = cur.fetchone()
        assert table_name[0] == 1
    conn.close()


@pytest.mark.order14
def test_init_missing_column():
    """Test whether a missing column raises an error."""
    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute("""ALTER TABLE {} DROP COLUMN daphne_port;"""
                    .format(PSQL_TABLE))
    conn.close()

    with pytest.raises(psycopg2.ProgrammingError):
        postgres.PostgreSQLDatabaseHandler()
