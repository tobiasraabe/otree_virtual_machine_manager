# -*- coding: utf-8 -*-

import ast
import os

import click
import yaml

from .static import HOME, OSF


def check_list_integer(func):
    """Decorator which checks a list if it contains only integers."""
    def wrap(*args, **kwargs):
        checked_list = [int(i) for i in func(*args, **kwargs)]
        return checked_list
    return wrap


@check_list_integer
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
    # Miscellaneous
    # Restriction for password length by unix systems
    PASSWORD_LENGTH = int(os.environ.get('OVMM_PASSWORD_LENGTH', 8))
    if PASSWORD_LENGTH < 8:
        click.secho('ERROR: Minimal password length is 8.', fg='red')
        PASSWORD_LENGTH = 8
        click.secho('WARNING: Password length set to 8.', fg='yellow')
except ValueError:
    click.secho(
        'WARNING: The password is not correctly set and defaults to 8.',
        fg='yellow')
    PASSWORD_LENGTH = 8


# Environment variables
try:
    with open(os.path.join(HOME, OSF, 'ovmm_conf.yml')) as file:
        conf = yaml.load(file.read())
except FileNotFoundError:
    click.secho('WARNING: Setting could not be loaded from ovmm_conf.yml.\n'
                'Try to collect variables from environment.', fg='yellow')
    try:
        # oTree
        ADMIN_PASSWORD = os.environ.get('OTREE_ADMIN_PASSWORD', None)

        # Database
        PSQL_CONN = dict(ast.literal_eval(os.environ['OVMM_PSQL_CONN']))
        PSQL_TABLE = os.environ['OVMM_PSQL_TABLE']
        PORT_RANGES = {
            'daphne_port': list(
                literal_eval_lc(os.environ.get('OVMM_DAPHNE_RANGE', None))),
            'ssl_port': list(
                literal_eval_lc(os.environ['OVMM_SSL_RANGE'])),
            'redis_port': list(
                literal_eval_lc(os.environ['OVMM_REDIS_RANGE'])),
        }
    except KeyError:
        click.secho('ERROR: Environment variables could not be loaded. Have\n'
                    'you run sudo ovmm initialise?', fg='red')
        pass
except ValueError:
    click.secho('ERROR: Check if ports and password length are integers\n'
                'and ports are stored in valid list comprehensions.\n'
                'Program does not work!',
                fg='red')
    pass
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

    click.secho('SUCCESS: Configuration loaded.', fg='green')
