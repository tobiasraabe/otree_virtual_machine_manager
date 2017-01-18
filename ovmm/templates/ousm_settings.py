# -*- coding: utf-8 -*-

OUSM_SETTINGS = '''
"""This is the settings file for oTree Virtual Machine Manager.

"""

POSTGRES_CONNECTION = {
    # Arguments needed to connect with psycopg2
    'user': '_USER_',
    'password': '_PASSWORD_',
    'database': '_DATABASE_',
    'host': '_HOST_',
    'port': '_PORT_',
}

POSTGRES_MISC = {
    # Name for table containing user account information
    'table': '_TABLE_',
    # The ranges of free ports are specified by list comprehensions.
    # Adjust the values to your configuration.
    'daphne_port': [i for i in range(8001, 8021)],
    'http_port': [i for i in range(7901, 7921)],
    'ssl_port': [i for i in range(7801, 7821)],
    'redis_port': [i for i in range(1, 21)],
}
'''
