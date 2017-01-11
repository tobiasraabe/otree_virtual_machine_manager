# -*- coding: utf-8 -*-


import os
import sys
import click

try:
    sys.path.append({os.environ['HOME'] + '/ousm'})
    from ousm_settings import POSTGRES_SETTINGS
except ImportError:
    click.echo(
        'The ousm_settings file could not be imported. This is probably the '
        'first run. Please run `ousm initialise` to configure your machine')
    pass

__author__ = """Tobias Raabe"""
__email__ = 'tobiasraabe@uni-bonn.de'
__version__ = '0.1.0'
