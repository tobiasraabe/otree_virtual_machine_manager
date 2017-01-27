#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_handler_postgres
---------------------

"""

import pytest
from ovmm.handlers.postgres import PostgreSQLDatabaseHandler as postgres
import psycopg2
from ovmm.prompts.defaults import dummy_users


POSTGRES_MISC = {
    # Name for table containing user account information
    'table': 'user_table',
    # The ranges of free ports are specified by list comprehensions.
    # Adjust the values to your configuration.
    'daphne_port': [i for i in range(8001, 8021)],
    'http_port': [i for i in range(7901, 7921)],
    'ssl_port': [i for i in range(7801, 7821)],
    'redis_port': [i for i in range(1, 21)],
}

POSTGRES_CONN = {
    'dbname': 'postgres',
    'user': 'postgres',
    'host': 'localhost',
    'port': 5432,
}


@pytest.fixture(autouse=True)
def patches(monkeypatch):
    monkeypatch.setattr(PSQL_CONN, POSTGRES_CONN)
    monkeypatch.setattr(PSQL_MISC, POSTGRES_MISC)


@pytest.mark.order1
def test_check_connection_1():
    with pytest.raises(psycopg2.OperationalError)
        postgres.check_connection()


@pytest.mark.order2
def test_create_table():
    postgres.create_table()

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT EXISTS (
            SELECT 1
            FROM pg_tables
            WHERE tablename = '{table}');""".format(**PSQL_MISC)
        )
        table_name = cur.fetchone()
        assert PSQL_MISC['table'] in table_name
    conn.close()


@pytest.mark.order3
def test_check_connection_2():
    postgres.check_connection()


@pytest.mark.order4
def test_create_user_1():
    psql = postgres()
    psql.create_user(dummy_users['werner'])

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {table}
            WHERE user_name = '{user_name}';"""
            .format(**PSQL_MISC, dummy_users['werner']['user_name'])
        )
        user = cur.fetchone()
        for i in user:
            assert i in dummy_users['werner'].values()
    conn.close()


@pytest.mark.order5
def test_count_user_1():
    psql = postgres()
    num_free, num_max = psql.count_user()
    assert num_free == 19
    assert num_max == 1


@pytest.mark.order6
def test_create_user_2():
    psql = postgres()
    psql.create_user(dummy_user_2)

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {table}
            WHERE user_name = '{user_name}';"""
            .format(**PSQL_MISC, dummy_users['max']['user_name'])
        )
        user = cur.fetchone()
        for i in user:
            assert i in dummy_users['max'].values()
    conn.close()


@pytest.mark.order7
def test_count_user_2():
    psql = postgres()
    num_free, num_max = psql.count_user()
    assert num_free == 18
    assert num_max == 2


@pytest.mark.order8
def test_list_user():
    user_list = postgres.list_user()
    assert 'werner' in user_list
    assert 'max' in user_list


@pytest.mark.order9
def test_delete_user():
    postgres.delete_user(dummy_user['werner']['user_name'])

    with psycopg2.connect(**PSQL_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {table}
            WHERE user_name = '{user_name}';"""
            .format(**PSQL_MISC, dummy_users['werner']['user_name'])
        )
        with pytest.raises(psycopg2.ProgrammingError)
            cur.fetchone()
    conn.close()

