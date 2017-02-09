# -*- coding: utf-8 -*-

import os
import random
import string
import sys
import traceback

import click
import pkg_resources
from plumbum.cmd import printf
from plumbum.cmd import sudo

from ovmm.commands.delete_user import delete_user
from ovmm.config.settings import HOME, OSF, ADMIN_PASSWORD, PASSWORD_LENGTH
from ovmm.handlers.nginx import NginxConfigHandler
from ovmm.handlers.postgres import PostgreSQLDatabaseHandler
from ovmm.handlers.samba import SambaConfigHandler
from ovmm.prompts.defaults import get_dummy_user


def add_user():
    """This command creates a new user.

    .. note::
        The following steps are performed.

        #. User information is generated
        #. Add user to PSQL database (checks whether user already exists)
        #. Create user and home directory, set password expiration date to now
        #. Unpack additional files to user's home directory
        #. Create otree project folder
        #. Set database information in settings.py
        #. Set nginx configuration file
        #. Allow access to ports via ufw
        #. Create samba configuration
        #. Add alias to .profile
        #. Set user's default shell to bash
        #. Write user_config to ``ovmm_sources/user_configs/``

    """

    click.echo('\n{:-^60}'.format(' Process: Add User '))

    # Generate user information
    default = get_dummy_user()
    dict_user = {}
    dict_user['user_name'] = click.prompt(
        'User name', default=default['user_name'])
    dict_user['full_name'] = click.prompt(
        'Full name', default=default['full_name'])
    dict_user['email'] = click.prompt(
        'Email', default=default['email'])
    dict_user['telephone'] = click.prompt(
        'Telephone', default=default['telephone'])
    dict_user['password'] = ''.join(random.SystemRandom().choice(
        string.ascii_lowercase + string.digits) for _ in range(PASSWORD_LENGTH)
    )
    postgres_check = PostgreSQLDatabaseHandler.get_user(dict_user['user_name'])
    if postgres_check is not None:
        click.secho(
            'ERROR: user {} already exists in database!'
            .format(dict_user['user_name']), fg='red'
        )
        sys.exit(0)
    else:
        path_user = os.path.join('/home', dict_user['user_name'])

    try:
        # Calls the postgres user database
        postgres = PostgreSQLDatabaseHandler()
        dict_user = postgres.create_user(dict_user)

        # Add user with password
        sudo['useradd', dict_user['user_name'], '--create-home']()
        (printf['{}:{}'.format(
            dict_user['user_name'], dict_user['password'])] |
         sudo['chpasswd'])()

        # Force password change at first login
        sudo['chage', '-d', '0', dict_user['user_name']]()

        # Unpack additional files to user directory
        data = pkg_resources.resource_filename(
            'ovmm', 'static/exp_env.7z')
        sudo['-u', '{user_name}'.format(**dict_user), '7z', 'x', data,
             '-o' + path_user, '-y']()
        sudo['-u', dict_user['user_name'], 'ln', '-s',
             os.path.join(path_user, 'Projects', 'first_project'),
             os.path.join(path_user, '.oTree')]()

        # Create virtualenv in user's home folder
        sudo['-u', dict_user['user_name'], 'python3', '-m', 'venv',
             '/home/{user_name}/.oTree/venv'.format(**dict_user)]()

        # Creates standardized otree-project folder !!! (name change)
        # (printf['n'] |
        #  sudo['su', '-', dict_user['user_name'], '-c',
        #       'otree startproject oTree'])()

        # nginx
        nch = NginxConfigHandler()
        nch.add_user(dict_user)

        # firewall - open new port to the web
        sudo['ufw', 'allow', dict_user['http_port']]()
        sudo['ufw', 'allow', dict_user['ssl_port']]()
        sudo['nginx', '-s', 'reload']()

        # samba
        samba = SambaConfigHandler()
        samba.add_user(dict_user)

        # environment variables
        temp = dict_user.copy()
        temp.update({'admin_password': ADMIN_PASSWORD})
        otree_env_path = pkg_resources.resource_filename(
            'ovmm', 'static/otree_environ_config')
        with open(otree_env_path) as file_input:
            with open(os.path.join(path_user, 'otree_environ_config'),
                      'w') as file_output:
                file_output.write(file_input.read().format(**temp))
        sudo['chown', '{0}:{0}'.format(dict_user['user_name']),
             os.path.join(path_user, 'otree_environ_config')]()

        # .profile
        path_profile = pkg_resources.resource_filename(
            'ovmm', 'static/.profile')
        with open(path_profile) as file_input:
            with open(os.path.join('/home', dict_user['user_name'],
                                   '.profile'), 'w') as file_output:
                file_output.write(
                    file_input.read().format(**dict_user)
                )

        # set user's default shell to bash
        sudo['usermod', '-s', '/bin/bash', dict_user['user_name']]()

        # create output
        path = os.path.join(HOME, OSF, 'user_configs')
        if not os.path.exists(path):
            os.makedirs(path)
        path_ext = os.path.join(path, '{user_name}.txt'.format(**dict_user))
        with open(path_ext, 'w') as file:
            file.write('[{user_name}]'.format(**dict_user))
            file.write('\n\tname:\t\t{full_name}'.format(**dict_user))
            file.write('\n\temail:\t\t{email}'.format(**dict_user))
            file.write('\n\ttelephone:\t{telephone}'.format(**dict_user))
            file.write('\n\tpassword:\t{password}'.format(**dict_user))
            file.write('\n\tdaphne_port:\t{daphne_port}'.format(**dict_user))
            file.write('\n\thttp_port:\t{http_port}'.format(**dict_user))
            file.write('\n\tssl_port:\t{ssl_port}'.format(**dict_user))
            file.write('\n\tredis_port:\t{redis_port}'.format(**dict_user))
    except Exception:
        click.secho(
            'ERROR: An error occurred while creating the user.\n'
            'The system is rolled back to the previous state.\n', fg='red')
        click.secho(str(traceback.format_exc()), fg='red')
        delete_user(dict_user=dict_user, instant_del=True)
    else:
        click.secho(
            'SUCCESS: {user_name} was created!'.format(**dict_user),
            fg='green')

    click.echo('{:-^60}\n'.format(' Process: End '))
