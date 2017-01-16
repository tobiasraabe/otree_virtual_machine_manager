# -*- coding: utf-8 -*-

import click
import os
import time

from . import HOME
from ..prompts.defaults import get_add_default
from plumbum.cmd import pg_dump
from plumbum.cmd import sudo


def backup_user(user_name=None):
    """This command performs a database backup for ``user_name``.

    - *parameters*::
        :user_name: Name of the user whose data is backed up

    - The following steps are performed::
        :1: If no user_name is provided, ask for it
        :2: If no folder for backups exists, create it
        :3: Save the database to backup folder

    """

    click.echo('{:-^60}\n'.format(' Process: back_user '))

    if user_name is None:
        default = get_add_default()
        user_name = click.prompt(
            'Which user do you want to backup?', default=default['user_name'])

    if not os.path.exists(HOME + '/ousm/user_backups'):
        os.makedirs(HOME + '/ousm/user_backups')

    tim = time.strftime('%Y-%m-%d_%H-%M-%S')
    (sudo['u-', 'postgres', '-c', pg_dump[user_name]] >
     (HOME + '/ousm/user_backups/' + user_name + '_db_dump_' + tim + '.sql'))()

    click.secho(
        "A backup of user's database was successfully created", fg='green')
    click.echo('{:-^60}\n'.format(' Process: End '))
