"""Collection of parsers used for click prompts.

"""

import re

import click

from ovmm.config.environment import PASSWORD_LENGTH


def parse_user_name(user_name: str) -> str:
    """Checks if ``user_name`` is valid.

    Parameters
    ----------
    user_name : str
        Possible user name.

    Returns
    -------
    user_name : str
        Valid user name.

    Raises
    ------
    click.BadParameter
        If user name is not valid.

    """
    if re.fullmatch(r'^[a-z][a-z0-9_]{5,}', user_name):
        return user_name
    else:
        raise click.BadParameter(
            'ERROR: Use at least six lower-case characters, '
            'digits and underscores.', param=user_name)


def parse_password(password: str) -> str:
    """Checks if ``password`` is suffiently strong.

    Parameters
    ----------
    password : str
        Possible password.

    Returns
    -------
    password : str
        Valid password.

    Raises:
    click.BadParameter
        If password is not sufficiently strong.

    """
    if password in ['password', 'hallo123', 'admin']:
        raise click.BadParameter('ERROR: You are kidding, right?')
    elif re.fullmatch(r'[A-Za-z0-9]{{{},}}'.format(PASSWORD_LENGTH), password):
        return password
    else:
        raise click.BadParameter('ERROR: Use only alphanumeric characters.')


def parse_lower_alpha(string: str) -> str:
    """Checks if ``string`` consists out of at least of 6 characters.

    Parameters
    ----------
    string : str
        Possible string.

    Returns
    -------
    string : str
        Valid string.

    Raises
    ------
    click.BadParameter
        If string is not sufficiently strong.

    """
    if re.fullmatch(r'[a-z]{6,}', string):
        return string
    else:
        raise click.BadParameter(
            'ERROR: Use at least 6 lower-case characters.')


def parse_host(host: str) -> str:
    """Checks if host is valid.

    Parameters
    ----------
    host : str
        Possible host name.

    Returns
    -------
    host : str
        Valid host name

    Raises
    ------
    click.BadParameter
        If ``host`` is not ``localhost`` or a four digit number not starting
        with zero.

    """
    if host == 'localhost':
        return host
    elif re.fullmatch(r'^[1-9][0-9]{,3}', host):
        return host
    else:
        raise click.BadParameter(
            'ERROR: Use <localhost> or up to four digits not starting with '
            'zero.')


def parse_port(port: str) -> str:
    """Checks if port is valid.

    Parameters
    ----------
    port : str
        Possible port name.

    Returns
    -------
    port : str
        Valid port name

    Raises
    ------
    click.BadParameter
        If ``port`` is not a four-digit number not starting with zero.

    """
    if re.fullmatch(r'^[1-9][0-9]{,3}', port):
        return port
    else:
        raise click.BadParameter(
            'ERROR: Use up to four digits not starting with zero.')


def parse_table_name(table_name: str) -> str:
    """Checks if ``table_name`` is a valid name for a PostgreSQL table.

    Parameters
    ----------
    table_name : str
        Possible table name.

    Returns
    -------
    table_name : str
        Valid table name

    Raises
    ------
    click.BadParameter
        If ``table_name`` is not valid for PSQL.

    """
    if re.fullmatch(r'^[a-z][a-z_]{5,}', table_name):
        return table_name
    else:
        raise click.BadParameter(
            'ERROR: Use only lower-case characters and underscores.')
