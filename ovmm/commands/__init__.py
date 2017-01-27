# -*- coding: utf-8 -*-

import click
import os
import sys


OVMM_SOURCE_FOLDER = 'ovmm_sources'


# Include ovmm in PYTHONPATH
sys.path.append(os.path.expanduser('~') + '/' + OVMM_SOURCE_FOLDER)
# Checks whether the ovmm_settings.py exists
try:
    import ovmm_settings  # noqa: F401
except ImportError:
    click.secho(
        'The ovmm_settings file could not be imported. This is probably the\n'
        'first run. Please run `ovmm initialise` to configure your machine',
        fg='red')
    pass

# Sets a variable for the path to user's home directory
HOME = os.path.expanduser('~')
