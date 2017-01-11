# -*- coding: utf-8 -*-

import click
import os
import sys

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
    if sys.argv[1] == 'initialise':
        pass
    else:
        sys.exit(0)

__author__ = 'Tobias Raabe'
__email__ = 'tobiasraabe@uni-bonn.de'
__version__ = '0.1.0'
