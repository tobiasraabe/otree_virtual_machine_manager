#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This script adds a new user to the otree-ubuntu-server configuration. The
following steps are executed:

    - [X] User information is generated
    - [X] Add user to PSQL database (checks whether user already exists)
    - [X] Create user and home directory, set password expiration date to now
    - [X] Unpack additional files to user's home directory
    - [X] Create otree project folder
    - [X] Set database information in settings.py
    - [X] Set nginx configuration file
    - [X] Allow access to ports via ufw
    - [X] Create samba configuration
    - [X] Add alias to .profile

"""

import click
import os
import plumbum
import random
import string

from ..handlers.nginx import NginxConfigHandler
from ..handlers.postgres import PostgreSQLDatabaseHandler
from ..handlers.samba import SambaConfigHandler
from ..prompts.defaults import get_add_default
from ..templates.settings_py import SETTINGS_PY
from plumbum.cmd import chage
from plumbum.cmd import chpasswd
from plumbum.cmd import nginx
from plumbum.cmd import printf
from plumbum.cmd import su
from plumbum.cmd import sudo
from plumbum.cmd import ufw
from plumbum.cmd import useradd
from plumbum.cmd import usermod

__docformat__ = 'reStructuredText'


PASSWORD_LENGTH = 12
EXP_ENV = 'exp_env.7z'

zipper = plumbum.local['7z']


def add_user():
    """ This function lets you add a new user account.

    ..note::
        A check to evaluate whether the selected user account exists is not
        included in the function since it is already covert by `useradd`
        itself.

    """

    click.echo('\n{:-^60}'.format(' Process: Add User '))

    # Generate user information
    default = get_add_default()
    dict_user = {}
    dict_user['user_name'] = click.prompt(
        'User name', default=default['user_name'])
    dict_user['user_full'] = click.prompt(
        'Full name', default=default['user_full'])
    dict_user['user_email'] = click.prompt(
        'Email', default=default['user_email'])
    dict_user['user_tel'] = click.prompt(
        'Telephone', default=default['user_tel'])
    dict_user['password'] = ''.join(random.SystemRandom().choice(
        string.ascii_lowercase + string.digits) for _ in range(PASSWORD_LENGTH)
    )

    # Calls the postgres user database
    postgres = PostgreSQLDatabaseHandler()
    dict_user = postgres.create_user(dict_user)

    # Add user with password
    useradd[dict_user['user_name'], '--create-home']()
    chain = (printf['{}:{}'.format(dict_user['user_name'],
                                   dict_user['password'])] | chpasswd)
    chain()

    # Force password change at first login
    chage['-d', '0', dict_user['user_name']]()

    # Create virtualenv in user's home folder
    sudo['-u', '{user_name}'.format(**dict_user), 'python3', '-m', 'venv',
         '/home/{user_name}/venv_otree'.format(**dict_user)]()

    # Unpack additional files to user directory
    sudo['-u', '{user_name}'.format(**dict_user), '7z', 'x', EXP_ENV,
         '-o/home/{user_name}'.format(**dict_user), '-y']()

    # Creates standardized otree-project folder and executes
    chain = printf['n'] | sudo[su['-', dict_user['user_name'], '-c',
                                  'otree startproject oTree']]
    chain()

    # settings.py
    path_settingspy = '/home/{user_name}/oTree/settings.py'
    with open(path_settingspy.format(**dict_user), 'w') as file:
        file.write(SETTINGS_PY.format(**dict_user))

    # nginx
    nch = NginxConfigHandler()
    nch.add_user(dict_user)

    # firewall - open new port to the web
    sudo[ufw['allow', dict_user['http_port']]]()
    sudo[ufw['allow', dict_user['ssl_port']]]()
    sudo[nginx['-s', 'reload']]()

    # samba
    samba = SambaConfigHandler()
    samba.add_user(dict_user)

    # .profile
    try:
        path = '/home/{user_name}/.profile'.format(**dict_user)
        with open(path, 'a') as file:
            file.write('\n# Aliases')
            file.write(
                '\nalias run_prodserver="screen -S otree -m otree '
                'runprodserver -p {daphne_port}"'.format(**dict_user))
    except Exception as e:
        raise e
        click.secho('The alias for running a session could not be set.\n'
                    'Please check manually', fg='red')

    # set user's default shell to bash
    sudo[usermod['-s', '/bin/bash', '{user_name}'.format(**dict_user)]]()

    # create output
    if not os.path.exists('user_configs'):
        os.makedirs('user_configs')
    with open('user_configs/{user_name}.txt'.format(**dict_user), 'w') as file:
        file.write('[{user_name}]'.format(**dict_user))
        file.write('\n\tname:\t\t{user_full}'.format(**dict_user))
        file.write('\n\temail:\t\t{user_email}'.format(**dict_user))
        file.write('\n\ttelephone:\t{user_tel}'.format(**dict_user))
        file.write('\n\tpassword:\t{password}'.format(**dict_user))
        file.write('\n\tdaphne_port:\t{daphne_port}'.format(**dict_user))
        file.write('\n\thttp_port:\t{http_port}'.format(**dict_user))
        file.write('\n\tssl_port:\t{ssl_port}'.format(**dict_user))
        file.write('\n\tredis_port:\t{redis_port}'.format(**dict_user))

    click.secho(
        'Success! {user_name} was created!'.format(**dict_user), fg='green')
    click.echo('{:-^60}\n'.format(' Process: End '))
