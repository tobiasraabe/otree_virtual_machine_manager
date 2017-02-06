# -*- coding: utf-8 -*-

import ast
import os

import click
import yaml

HOME = os.path.expanduser('~')
OSF = 'ovmm_sources'


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
    with open(os.path.join(HOME, OSF, 'ovmm_env.yml')) as file:
        conf = yaml.load(file.read())
except Exception as e:
    click.secho(
        'ERROR: Not all settings could be loaded. Fix it.'
    )
    raise e
else:
    # Required
    PSQL_CONN = dict(conf['OVMM_PSQL_CONN'])
    PSQL_TABLE = conf['OVMM_PSQL_TABLE']
    PORT_RANGES = {
        'daphne_port': list(
            literal_eval_lc(conf['OVMM_DAPHNE_RANGE'])),
        'http_port': list(
            literal_eval_lc(conf['OVMM_HTTP_RANGE'])),
        'ssl_port': list(
            literal_eval_lc(conf['OVMM_SSL_RANGE'])),
        'redis_port': list(
            literal_eval_lc(conf['OVMM_REDIS_RANGE'])),
    }

    # Optional
    PASSWORD_LENGTH = int(conf.get('OVMM_PASSWORD_LENGTH', 12))
    if PASSWORD_LENGTH < 6:
        click.secho(
            'ERROR: Minimal password length is 6.', fg='red'
        )
        PASSWORD_LENGTH = 6
        click.secho(
            'WARNING: Password length set to 6.', fg='yellow'
        )
    OSF = conf.get('OVMM_SOURCE_FOLDER', '/ovmm_sources')

    # Miscellaneous
    HOME = os.path.expanduser('~')
