#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_handlers_postgres
----------------------

"""

import importlib
import psycopg2
import pytest

from ovmm.handlers import postgres
from ovmm.prompts.defaults import dummy_users

POSTGRES_MISC = {'table': 'user_table',
                 'daphne_port': [i for i in range(8001, 8021)],
                 'http_port': [i for i in range(7901, 7921)],
                 'ssl_port': [i for i in range(7801, 7821)],
                 'redis_port': [i for i in range(1, 21)]}

POSTGRES_CONN = {'dbname': 'postgres', 'user': 'postgres', 'host': 'localhost',
                 'port': 5432}


@pytest.fixture(autouse=True)
def patching(monkeypatch):
    monkeypatch.setenv('PSQL_CONN', POSTGRES_CONN)
    monkeypatch.setenv('PSQL_MISC', POSTGRES_MISC)
    importlib.reload(postgres)


@pytest.mark.order1
def test_check_connection_1():
    with pytest.raises(psycopg2.ProgrammingError):
        postgres.PostgreSQLDatabaseHandler.check_connection()


@pytest.mark.order2
def test_create_table():
    postgres.PostgreSQLDatabaseHandler.create_table()

    with psycopg2.connect(**POSTGRES_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT EXISTS (
            SELECT 1
            FROM pg_tables
            WHERE tablename = '{table}');""".format(**POSTGRES_MISC)
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

    with psycopg2.connect(**POSTGRES_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {}
            WHERE user_name = '{user_name}';"""
            .format(POSTGRES_MISC['table'], **dummy_users['werner'])
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

    with psycopg2.connect(**POSTGRES_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {}
            WHERE user_name = '{user_name}';"""
            .format(POSTGRES_MISC['table'], **dummy_users['max'])
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
def test_delete_user():
    postgres.PostgreSQLDatabaseHandler.delete_user(
        dummy_users['werner']['user_name'])

    with psycopg2.connect(**POSTGRES_CONN) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM {}
            WHERE user_name = '{user_name}';"""
            .format(POSTGRES_MISC['table'], **dummy_users['werner'])
        )
        temp = cur.fetchone()
        assert temp is None
    conn.close()
