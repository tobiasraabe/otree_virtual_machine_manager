# -*- coding: utf-8 -*-

import os
import time

import click
import plumbum
from plumbum.cmd import sudo

from ..prompts.defaults import get_dummy_user

HOME = os.path.expanduser('~')


def backup_user(user_name: str = None):
    """This command performs a database backup for ``user_name``.

    Parameters
    ----------
    user_name : str
        Name of the user whose data is backed up


    .. note::
        The following steps are performed.

        #. If no user_name is provided, ask for it
        #. If no folder for backups exists, create it
        #. Save the database to backup folder

    Raises
    ------
    plumbum.ProcessExecutionError
        If database backup for user failed.

    """

    click.echo('{:-^60}\n'.format(' Process: back_user '))

    if user_name is None:
        default = get_dummy_user()
        user_name = click.prompt(
            'Which user do you want to backup?', default=default['user_name'])

    if not os.path.exists(HOME + '/ovmm_sources/user_backups'):
        os.makedirs(HOME + '/ovmm_sources/user_backups')

    tim = time.strftime('%Y-%m-%d_%H-%M-%S')
    file_name = (
        HOME + '/ovmm_sources/user_backups/' + user_name + '_db_dump_'
        + tim + '.sql')
    try:
        (sudo['su', '-', 'postgres', '-c', 'pg_dump', user_name] >
         file_name)()
    except plumbum.ProcessExecutionError:
        click.secho(
            'ERROR: {} does not exist in the database!'.format(user_name),
            fg='red'
        )
        raise
    click.secho(
        "A backup of the database was successfully created", fg='green')
    click.echo('{:-^60}\n'.format(' Process: End '))
