# -*- coding: utf-8 -*-

import sys
import os
import click


# Include ovmm in PYTHONPATH
sys.path.insert(1, os.path.expanduser('~') + '/ovmm')
# Checks whether the ovmm_settings.py exists
try:
    from ovmm_settings import POSTGRES_CONNECTION
    from ovmm_settings import POSTGRES_MISC
except ImportError:
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
