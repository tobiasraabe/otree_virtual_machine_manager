#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This script should be executed *in advance* to any use of `admin.py` on a
new system. It checks whether all dependencies are satisfied. *An internet
connection is needed.*

"""

import click
import os
from plumbum.cmd import sudo
from otree_ubuntu_server_manager.prompts.user_prompts import get_password
from otree_ubuntu_server_manager.templates.ousm_settings import OUSM_SETTINGS

try:
    HOME = os.environ['HOME']
except Exception as e:
    raise e
    exit(0)


def initialise():
    """Initial steps"""

    click.echo('\n{:-^60}'.format(' Process: Init '))

    click.echo('Installing ubuntu dependencies...')
    try:
        click.echo('--> Installing 7z')
        sudo['apt-get', 'install', 'p7zip-full']()
    except Exception as e:
        raise e
        pass
    else:
        click.echo('Requirement satisfied.')

    click.echo('Installing OUSM related content.')
    try:
        click.echo('--> The content folder will be created under {}/ousm'
                   .format(HOME))
        for folder in ['', '/user_configs', '/user_backups']:
            if os.path.isdir('{}/ousm{}'.format(HOME, folder)):
                click.confirm('{}/ousm{} already exists. Do you want to '
                              'continue?'.format(HOME, folder), abort=True)
            else:
                os.mkdir('{}/ousm'.format(HOME))

        click.echo('--> Set information for the postgres database.')
        psql_user = click.prompt('Enter postgres user with user database '
                                 'access', default='postgres')
        psql_database = click.prompt('Enter a database name',
                                     default='postgres')
        psql_host = click.prompt('Enter the host', default='localhost')
        psql_port = str(click.prompt('Enter the port', default=5432))
        psql_table = click.prompt('Enter a name for the user table',
                                  default='user_table')
        click.echo('Enter the password for the user.')
        psql_password = get_password()
        if ((psql_user == 'posgres') &
            click.confirm('Since you chose the default user, should the '
                          'password be set automatically?')):
            sudo['-u', 'postgres', 'psql', '-c',
                 "ALTER ROLE postgres PASSWORD '{}'".format(psql_password)]
        with open(HOME + '/ousm/ousm_settings.py', 'w') as file:
            file.write(OUSM_SETTINGS.replace('_USER_', psql_user)
                                    .replace('_PASSWORD_', psql_password)
                                    .replace('_DATABASE_', psql_database)
                                    .replace('_HOST_', psql_host)
                                    .replace('_PORT_', psql_port)
                                    .replace('_TABLE_', psql_table))
    except Exception as e:
        raise e
        pass

    click.echo('End of initialisation. Fix possible errors before running '
               'anything else!')
    click.echo('{:-^60}\n'.format(' Process: End '))
