#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This scripts removes a user from the otree-server configuration. Every step
is written inside a try-except block which continues in case of an error.
The steps are:

    - [X] Look up user name in PSQL database, get http_port for ufw, delete
          entry
    - [X] Remove Ubuntu user with home directory
    - [X] Remove nginx configuration
    - [X] Close open ports
    - [X] Delete Samba configuration

"""

import click

from ..handlers.nginx import NginxConfigHandler
from ..handlers.postgres import PostgreSQLDatabaseHandler
from ..handlers.samba import SambaConfigHandler
from ..prompts.defaults import get_add_default
from .backup_user import backup_user
from plumbum.cmd import sudo
from plumbum.cmd import ufw
from plumbum.cmd import userdel


def delete_user():
    http_port = None

    click.echo('\n{:-^60}'.format(' Process: Delete User '))

    default = get_add_default()
    user_name = click.prompt(
        'Which user do you want to delete?', default=default['user_name'])
    if click.confirm('Do you want a database backup?', default=True):
        backup_user(user_name)

    try:
        postgres = PostgreSQLDatabaseHandler()
        http_port, ssl_port = postgres.delete_user(user_name)
    except:
        pass

    try:
        userdel['--remove', user_name]()
    except:
        pass
    else:
        click.secho('User {} and home directory were successfully removed.'
                    .format(user_name), fg='green')

    try:
        nch = NginxConfigHandler()
        nch.delete_user(user_name)
    except:
        pass

    try:
        sudo[ufw['deny', http_port]]()
        sudo[ufw['deny', ssl_port]]()
    except:
        pass

    try:
        samba = SambaConfigHandler()
        samba.delete_user(user_name)
    except:
        pass

    try:
        sudo['rm', 'user_configs/{}'.format(user_name)]
    except:
        pass

    click.secho('\nThe deletion process is completed. If an error occured,\n'
                'check the failing yourself.', fg='yellow')
    click.echo('{:-^60}\n'.format(' Process: End '))
