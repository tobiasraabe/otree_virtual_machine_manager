# -*- coding: utf-8 -*-

import sys
import os
import click


# Include ousm in PYTHONPATH
sys.path.insert(1, os.path.expanduser('~') + '/ousm')
# Checks whether the ousm_settings.py exists
try:
    from ousm_settings import POSTGRES_CONNECTION
    from ousm_settings import POSTGRES_MISC
except ImportError:
    click.secho(
        'The ousm_settings file could not be imported. This is probably the\n'
        'first run. Please run `ousm initialise` to configure your machine',
        fg='red')
    pass

# Sets a variable for the path to user's home directory
try:
    HOME = os.path.expanduser('~')
except Exception as e:
    raise e
    click.secho('Home directory could not be found!', fg='red')
