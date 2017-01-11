#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This script makes a database backup for a specific user. The
following steps are executed:

    - [X] Create directory in otree-admin
    - [X] Output database in ``user_db_backups/``

"""

import click
import os
import time
from ..prompts.defaults import get_add_default
from plumbum import local
from plumbum.cmd import pg_dump
from plumbum.cmd import su
from plumbum.cmd import sudo


zipper = local['7z']

ADMIN_DIRECTORY = 'user_db_backups/'


def backup_user(user_name=None):
    """For a given user name, the function backups the user's database to a
    folder in the administrator's directory."""

    click.echo('{:-^60}\n'.format(' Process: back_user '))

    if user_name is None:
        default = get_add_default()
        user_name = click.prompt(
            'Which user do you want to backup?', default=default['user_name'])

    if not os.path.exists(ADMIN_DIRECTORY):
        os.makedirs(ADMIN_DIRECTORY)

    timestr = time.strftime('%Y-%m-%d_%H-%M-%S')
    (sudo[su['-', 'postgres', '-c', pg_dump[user_name]]] >
     'user_db_backups/' + user_name + '_db_dump_' + timestr + '.sql')()

    click.secho(
        "A backup of user's database was successfully created", fg='green')
    click.echo('{:-^60}\n'.format(' Process: End '))
