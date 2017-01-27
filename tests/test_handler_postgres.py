#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_handler_postgres
---------------------

"""

import pytest
from ovmm.handlers.postgres import PostgreSQLDatabaseHandler as postgres
import testing.postgresql
import psycopg2


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


@pytest.fixture(autouse=True)
def database():
    db = testing.postgresql.Postgresql()
    yield db
    db.stop()


def test_check_connection(monkeypatch):
    db = db()
    monkeypatch.setattr(PSQL_CONN, db.dsn())
    postgres.check_connection()


def test_connection()
    with psycopg2.connect(database='postgres', user='postgres', password='') as conn:
        cur = conn.cursor()
        print('SUCCESS 1')


def test_connection()
    with psycopg2.connect(database='postgres', user='postgres') as conn:
        cur = conn.cursor()
        print('SUCCESS 2')
