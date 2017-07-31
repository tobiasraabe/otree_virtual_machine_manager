# -*- coding: utf-8 -*-

import ast
import os

import click


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
    pass


# Environment variables
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
    click.secho('ERROR: Not all environment variables are specified.\n'
                'Program does not work! Have you run ovmm initialise?',
                fg='red')
    pass
except ValueError:
    click.secho('ERROR: Check if ports and password length are integers\n'
                'and ports are stored in a valid python dict.\n'
                'Program does not work!',
                fg='red')
    pass
else:
    click.secho('SUCCESS: Configuration loaded.', fg='green')
