"""Collection of validators used for click.options callbacks.

"""

import re

import click

from ovmm.config.environment import PASSWORD_LENGTH


def validate_user_name(ctx, param, value):
    if re.fullmatch(r'^[a-z][a-z0-9_]{5,}', value):
        return value
    else:
        raise click.BadParameter(
            'User names can only contain 0-9, a-z and _.')


def validate_email(ctx, param, value):
    if re.fullmatch(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                    value):
        return value
    else:
        raise click.BadParameter('Email address is not valid.')


def validate_password(ctx, param, value):
    if value in ['password', 'hallo123', 'admin']:
        raise click.BadParameter('You are kidding, right?')
    elif re.fullmatch(r'[A-Za-z0-9]{{{},}}'.format(PASSWORD_LENGTH), value):
        return value
    else:
        raise click.BadParameter('Use only alphanumeric characters.')


def validate_telephone(ctx, param, value):
    return ''.join(filter(str.isdigit, value))
