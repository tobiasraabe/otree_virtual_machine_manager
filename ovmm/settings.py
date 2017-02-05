# -*- coding: utf-8 -*-

import ast
import os

import click

try:
    # Required
    PSQL_CONN = dict(ast.literal_eval(os.environ['OVMM_PSQL_CONN']))
    PSQL_TABLE = os.environ['OVMM_PSQL_TABLE']
    PORT_RANGES = {
        'daphne_port': list(ast.literal_eval(os.environ['OVMM_DAPHNE_RANGE'])),
        'http_port': list(ast.literal_eval(os.environ['OVMM_HTTP_RANGE'])),
        'ssl_port': list(ast.literal_eval(os.environ['OVMM_SSL_RANGE'])),
        'redis_port': list(ast.literal_eval(os.environ['OVMM_REDIS_RANGE'])),
    }

    # Optional
    PASSWORD_LENGTH = int(os.environ.get('OVMM_PASSWORD_LENGTH', 12))
    if PASSWORD_LENGTH < 6:
        click.secho(
            'ERROR: Minimal password length is 6.', fg='red'
        )
        PASSWORD_LENGTH = 6
        click.secho(
            'WARNING: Password length set to 6.', fg='yellow'
        )
    OSF = os.environ.get('OVMM_SOURCE_FOLDER', '/ovmm_sources')

    # Miscellaneous
    HOME = os.path.expanduser('~')
except Exception as e:
    click.secho(
        'ERROR: Not all settings could be loaded. Fix it.'
    )
    raise e
