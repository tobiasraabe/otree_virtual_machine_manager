"""Collection of parsers used for click prompts.

"""

import click
import re

try:
    from ovmm.config.settings import PASSWORD_LENGTH
except KeyError:
    PASSWORD_LENGTH = 8


def parse_user_name(user_name):
    if re.fullmatch(r'^[a-z][a-z0-9_]{5,}', user_name):
        return user_name
    else:
        raise click.BadParameter(
            'ERROR: Use at least six lower-case characters, '
            'digits and underscores.', param=user_name)


def parse_email(email):
    if re.fullmatch(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                    email):
        return email
    else:
        raise click.BadParameter('ERROR: Email address is not valid.')


def parse_telephone(telephone_raw):
    return ''.join(filter(str.isdigit, telephone_raw))


def parse_password(password):
    if password == 'password':
        raise click.BadParameter('ERROR: You are kidding, right?')
    elif re.fullmatch(r'[A-Za-z0-9]{{{},}}'.format(PASSWORD_LENGTH), password):
        return password
    else:
        raise click.BadParameter('ERROR: Use only alphanumeric characters.')


def parse_lower_alpha(string):
    if re.fullmatch(r'[a-z]{6,}', string):
        return string
    else:
        raise click.BadParameter(
            'ERROR: Use at least 6 lower-case characters.')


def parse_host(host):
    if (host == 'localhost'):
        return host
    elif re.fullmatch(r'^[1-9][0-9]{,3}', host):
        return host
    else:
        raise click.BadParameter(
            'ERROR: Use <localhost> or up to four digits.')


def parse_port(port):
    if re.fullmatch(r'^[1-9][0-9]{,3}', port):
        return port
    else:
        raise click.BadParameter('ERROR: Use up to four digits.')


def parse_table_name(table_name):
    if re.fullmatch(r'^[a-z][a-z_]{5,}', table_name):
        return table_name
    else:
        raise click.BadParameter(
            'ERROR: Use only lower-case characters and underscores.')
