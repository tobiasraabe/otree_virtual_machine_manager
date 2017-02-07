#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_handlers_postgres
----------------------

"""

import sys

import psycopg2
import pytest

from ovmm.config.settings import PSQL_CONN, PSQL_TABLE
from ovmm.handlers import postgres
from ovmm.prompts.defaults import dummy_users

# Variable is used to skip postgres tests if not on Ubuntu
pytestmark = pytest.mark.skipif(
    sys.platform != 'linux',
    reason='Tests for linux with PostgreSQL database only')
# Implement a skip if PostgreSQL is not installed.


@pytest.mark.order1
def test_check_connection_1():
    with pytest.raises(psycopg2.ProgrammingError):
        postgres.PostgreSQLDatabaseHandler.check_connection()


@pytest.mark.order2
def test_create_table():
    postgres.PostgreSQLDatabaseHandler.create_table()

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT EXISTS (
            SELECT 1
            FROM pg_tables
            WHERE tablename = '{}');""".format(PSQL_TABLE)
        )
        table_name = cur.fetchone()
        assert table_name[0]
    conn.close()


@pytest.mark.order3
def test_check_connection_2():
    postgres.PostgreSQLDatabaseHandler.check_connection()


@pytest.mark.order4
def test_create_user_1():
    psql = postgres.PostgreSQLDatabaseHandler()
    dummy_users['werner'].update({'password': '1234'})
    psql.create_user(dummy_users['werner'])

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {}
            WHERE user_name = '{user_name}';"""
            .format(PSQL_TABLE, **dummy_users['werner'])
        )
        user = cur.fetchone()
        for i in user:
            assert i in dummy_users['werner'].values()
    conn.close()


@pytest.mark.order5
def test_count_user_1():
    psql = postgres.PostgreSQLDatabaseHandler()
    num_free, num_max = psql.count_user()
    assert num_free == 19
    assert num_max == 20


@pytest.mark.order6
def test_create_user_2():
    psql = postgres.PostgreSQLDatabaseHandler()
    dummy_users['max'].update({'password': '98765'})
    psql.create_user(dummy_users['max'])

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {}
            WHERE user_name = '{user_name}';"""
            .format(PSQL_TABLE, **dummy_users['max'])
        )
        user = cur.fetchone()
        for i in user:
            assert i in dummy_users['max'].values()
    conn.close()


@pytest.mark.order7
def test_create_duplicate_user():
    psql = postgres.PostgreSQLDatabaseHandler()
    dummy_users['max'].update({'password': '98765'})
    with pytest.raises(psycopg2.IntegrityError):
        psql.create_user(dummy_users['max'])


@pytest.mark.order8
def test_count_user_2():
    psql = postgres.PostgreSQLDatabaseHandler()
    num_free, num_max = psql.count_user()
    assert num_free == 18
    assert num_max == 20


@pytest.mark.order9
def test_list_user():
    user_list = postgres.PostgreSQLDatabaseHandler.list_user()
    assert 'werner' in user_list
    assert 'max' in user_list


@pytest.mark.order10
def test_get_user():
    dict_user = postgres.PostgreSQLDatabaseHandler.get_user(
        dummy_users['werner']['user_name'])
    for key in dummy_users['werner'].keys():
        assert dict_user[key] == dummy_users['werner'][key]


@pytest.mark.order11
def test_delete_user():
    postgres.PostgreSQLDatabaseHandler.delete_user(
        dummy_users['werner']['user_name'])

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {}
            WHERE user_name = '{user_name}';"""
            .format(PSQL_TABLE, **dummy_users['werner'])
        )
        temp = cur.fetchone()
        assert temp is None
    conn.close()

# Exclude for now. Don't why password is not changed within the first
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
    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute("""DROP TABLE {};"""
                    .format(PSQL_TABLE))

        cur.execute(
            """SELECT EXISTS (
            SELECT 1
            FROM pg_tables
            WHERE tablename = '{}');""".format(PSQL_TABLE)
        )
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
            WHERE tablename = '{}');""".format(PSQL_TABLE)
        )
        table_name = cur.fetchone()
        assert table_name[0] == 1
    conn.close()


@pytest.mark.order14
def test_init_missing_column():
    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute("""ALTER TABLE {} DROP COLUMN daphne_port;"""
                    .format(PSQL_TABLE))
    conn.close()

    with pytest.raises(psycopg2.ProgrammingError):
        postgres.PostgreSQLDatabaseHandler()
