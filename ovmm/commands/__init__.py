# -*- coding: utf-8 -*-

import click
import importlib
import os
import sys


# Include ovmm in PYTHONPATH
sys.path.insert(1, os.path.expanduser('~') + '/ovmm')
# Checks whether the ovmm_settings.py exists
try:
    psql_conn = importlib.util.find_spec(
        'POSTGRES_CONNECTION', package='ovmm_settings')
    psql_misc = importlib.util.find_spec(
        'POSTGRES_MISC', package='ovmm_settings')
except Exception as e:
    raise e
if (psql_conn is None) | (psql_misc is None):
    click.secho(
        'The ovmm_settings file could not be imported. This is probably the\n'
        'first run. Please run `ovmm initialise` to configure your machine',
        fg='red')
    pass

# Sets a variable for the path to user's home directory
try:
    HOME = os.path.expanduser('~')
except Exception as e:
    raise e
    click.secho('Home directory could not be found!', fg='red')
