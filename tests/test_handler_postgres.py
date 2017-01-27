#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_handler_postgres
---------------------

"""

import pytest
from ovmm.handlers.postgres import PostgreSQLDatabaseHandler as postgres
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


# @pytest.fixture(autouse=True)
# def patches(monkeypatch):
#     monkeypatch.setattr

def test_connection1():
    with psycopg2.connect(database='postgres', user='postgres', password='hello', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        print('SUCCESS 1')


def test_connection_2():
    with psycopg2.connect(database='postgres', user='postgres', password='hello', host='localhost', port='5432') as conn:
        cur = conn.cursor()
        print('SUCCESS 2')


def test_connection_3():
    with psycopg2.connect(database='postgres', user='postgres', password='hello', host='localhost', port='5432') as conn:
        cur = conn.cursor()
        print('SUCCESS 3')


def test_connection_4():
    with psycopg2.connect(database='postgres', user='postgres', password='hello', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        print('SUCCESS 4')
