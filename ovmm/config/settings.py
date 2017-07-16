# -*- coding: utf-8 -*-

import ast
import os

import click
import yaml

HOME = os.path.expanduser('~')
OSF = 'ovmm_sources'
USER_CONFIGS = 'user_configs'
USER_BACKUPS = 'user_backups'


def literal_eval_lc(lc_string: str) -> list:
    """Converts safely a list comprehension encapsulated in a string to the
    actual python object.

    Parameters
    ----------
    lc_string : str
        String encapsulation of list comprehension.

    Returns
    -------
    evaluated_lc : list
        The evaluated expression of the list comprehension.

    """

    temp = ast.parse(lc_string, mode='eval')
    evaluated_lc = eval(compile(temp, '', 'eval'))
    return evaluated_lc


try:
    with open(os.path.join(HOME, OSF, 'ovmm_conf.yml')) as file:
        conf = yaml.load(file.read())
except FileNotFoundError:
    click.secho(
        'ERROR: Settings could not be loaded.\n'
        'Collect settings from environment.'
    )
    PSQL_CONN = dict(ast.literal_eval(os.environ['OVMM_PSQL_CONN']))
    PSQL_TABLE = os.environ['OVMM_PSQL_TABLE']
    PORT_RANGES = {
        'daphne_port': list(
            literal_eval_lc(os.environ['OVMM_DAPHNE_RANGE'])),
        'ssl_port': list(
            literal_eval_lc(os.environ['OVMM_SSL_RANGE'])),
        'redis_port': list(
            literal_eval_lc(os.environ['OVMM_REDIS_RANGE'])),
    }

    PASSWORD_LENGTH = int(os.environ.get('OVMM_PASSWORD_LENGTH'))
except Exception as e:
    raise e
else:
    # Required
    ADMIN_PASSWORD = conf['OTREE_ADMIN_PASSWORD']
    PSQL_CONN = dict(conf['OVMM_PSQL_CONN'])
    PSQL_TABLE = conf['OVMM_PSQL_TABLE']
    PORT_RANGES = {
        'daphne_port': list(
            literal_eval_lc(conf['OVMM_DAPHNE_RANGE'])),
        'ssl_port': list(
            literal_eval_lc(conf['OVMM_SSL_RANGE'])),
        'redis_port': list(
            literal_eval_lc(conf['OVMM_REDIS_RANGE'])),
    }

    # Optional
    PASSWORD_LENGTH = int(conf.get('OVMM_PASSWORD_LENGTH', 8))
    if PASSWORD_LENGTH < 8:
        click.secho(
            'ERROR: Minimal password length is 8.', fg='red'
        )
        PASSWORD_LENGTH = 8
        click.secho(
            'WARNING: Password length set to 8.', fg='yellow'
        )
    OSF = conf.get('OVMM_SOURCE_FOLDER', 'ovmm_sources')

    # Miscellaneous
    HOME = os.path.expanduser('~')
