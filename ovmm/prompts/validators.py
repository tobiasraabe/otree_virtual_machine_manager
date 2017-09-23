"""Collection of validators used for click.options callbacks.

"""

import re

import click

from ovmm.config.environment import PASSWORD_LENGTH


def validate_user_name(ctx, param, value: str) -> str:
    """Validates if ``value`` is a correct user name.


    Parameters
    ----------
    value : str
        Possible user name.

    Returns
    -------
    value : str
        Valid user name.

    Raises
    ------
    click.BadParameter
        If user name is not valid for unix systems.

    """
    if re.fullmatch(r'^[a-z][a-z0-9_]{5,}', value):
        return value
    else:
        raise click.BadParameter(
            'User names can only contain 0-9, a-z and _.')


def validate_email(ctx, param, value: str) -> str:
    """Validates if ``value`` is a valid email address.

    Parameters
    ----------
    value : str
        Possible email address.

    Returns
    -------
    value : str
        Valid email address.

    Raises
    ------
    click.BadParameter
        If email address is not valid.
    """
    if re.fullmatch(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                    value):
        return value
    else:
        raise click.BadParameter('Email address is not valid.')


def validate_password(ctx, param, value: str) -> str:
    """Validates if ``value`` is valid password.

    Parameters
    ----------
    value : str
        Possible password.

    Returns
    -------
    value : str
        Valid password.

    Raises
    ------
    click.BadParameter
        If password is not valid for unix systems.
    """
    if value in ['password', 'hallo123', 'admin']:
        raise click.BadParameter('You are kidding, right?')
    elif re.fullmatch(r'[A-Za-z0-9]{{{},}}'.format(PASSWORD_LENGTH), value):
        return value
    else:
        raise click.BadParameter('Use only alphanumeric characters.')


def validate_telephone(ctx, param, value: str) -> str:
    """Receives ``value``, filters digits, and returns a string containing
    the filtered digits.

    Parameters
    ----------
    value : str
        Possible telephone number.

    Returns
    -------
    str
        Contains only digits of ``value``.

    Notes
    -----
    This is not really a validation method but since the telephone
    number is more or less optional, empty strings, etc. are
    accepted.
    """
    return ''.join(filter(str.isdigit, value))
