"""Collection of parsers used for click prompts.

"""

import click
import re

from ovmm.config.settings import PASSWORD_LENGTH


def parse_user_name(user_name):
    if re.fullmatch(r'^[a-z]+[a-z0-9_]*', user_name):
        return user_name
    else:
        raise click.BadParameter(
            'User name is not valid. Use lower case letters, numbers and '
            'underscores.', param=user_name)


def parse_email(email):
    if re.fullmatch(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                    email):
        return email
    else:
        raise click.BadParameter('Email address is not valid.')


def parse_telephone(telephone_raw):
    telephone = ''.join(filter(str.isdigit, telephone_raw))

    if telephone:
        return telephone
    else:
        raise click.BadParameter('Telephone number is not valid.')


def parse_password(password):
    if re.fullmatch(r'[A-Za-z0-9]{{{},}}'.format(PASSWORD_LENGTH), password):
        return password
    else:
        raise click.BadParameter('Password is not valid.')


def parse_integer(integer):
    if isinstance(integer, int):
        return integer
    else:
        raise click.BadParameter('Input is not a valid integer.')


def parse_lower_alpha(string):
    if re.fullmatch(r'[a-z]*', string):
        return string
    else:
        raise click.BadParameter('Input is not lower case string.')


def parse_host(host):
    if (host == 'localhost'):
        return host
    elif re.fullmatch(r'^[1-9][0-9]{,4}', host):
        return host
    else:
        raise click.BadParameter('Input is not a valid host.')


def parse_port(port):
    if re.fullmatch(r'^[1-9][0-9]{,4}', port):
        return port
    else:
        raise click.BadParameter('Input is not a valid port.')


def parse_table_name(table_name):
    if re.fullmatch(r'^[a-z]+[a-z_]*', table_name):
        return table_name
    else:
        raise click.BadParameter('Table name is not valid.')
