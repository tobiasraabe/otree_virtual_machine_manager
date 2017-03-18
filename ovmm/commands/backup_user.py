# -*- coding: utf-8 -*-

import os
import sys
import time

import click
import plumbum

from plumbum.cmd import sudo

from ovmm.config.settings import HOME
from ovmm.config.settings import OSF
from ovmm.config.settings import USER_BACKUPS
from ovmm.handlers.postgres import PostgreSQLDatabaseHandler
from ovmm.prompts.defaults import get_dummy_user
from ovmm.prompts.parsers import parse_user_name


def backup_user(strategy: str, user_name: str = None):
    """This command performs a database backup for ``user_name``.

    Parameters
    ----------
    strategy : str
        Specifies the backup strategy. Available options are ``all``, ``db``,
        and ``home``
    user_name : str
        Name of the user whose data is backed up


    .. note::
        The following steps are performed.

        #. If no user_name is provided, ask for it
        #. Check if user exists in database, else exit
        #. If no folder for backups exists, create it
        #. Dependent on strategy, run the desired backup process

    Raises
    ------
    plumbum.ProcessExecutionError
        If database backup for user failed.

    """

    click.echo('{:-^60}\n'.format(' Process: back_user '))
    # Check if user_name was passed
    if user_name is None:
        default = get_dummy_user()
        user_name = click.prompt(
            'Which user do you want to backup?', default=default['user_name'],
            value_proc=parse_user_name)
    # Check if user exists
    postgres_check = PostgreSQLDatabaseHandler.get_user(user_name)
    if postgres_check is None:
        click.secho(
            'ERROR: user {} does not exist in database!'
            .format(user_name), fg='red'
        )
        sys.exit(0)
    # Create necessary directories
    if not os.path.exists(os.path.join(HOME, OSF, USER_BACKUPS)):
        os.makedirs(os.path.join(HOME, OSF, USER_BACKUPS))
    # Define filename strings
    tim = time.strftime('%Y-%m-%d_%H-%M-%S')
    db_file_name = (
        os.path.join(HOME, OSF, USER_BACKUPS, user_name + '_db_dump_' +
                     tim + '.sql.7z'))
    home_file_name = (
        os.path.join(HOME, OSF, USER_BACKUPS, user_name + '_home_dump_' +
                     tim + '.7z'))
    # Run backups
    if strategy in ['home', 'all']:
        try:
            sudo['7z', 'a', home_file_name, os.path.join('/home', user_name)]()
        except plumbum.ProcessExecutionError:
            click.secho(
                'ERROR: {} does not exist in the database!'.format(user_name),
                fg='red'
            )
            raise
    if strategy in ['db', 'all']:
        try:
            (sudo['su', '-', 'postgres', '-c', 'pg_dump', user_name] |
             sudo['7z', 'a', '-si', db_file_name])()
        except plumbum.ProcessExecutionError:
            click.secho(
                'ERROR: {} does not exist in the database!'.format(user_name),
                fg='red'
            )
            raise

    click.secho(
        "A backup of the database was successfully created", fg='green')
    click.echo('{:-^60}\n'.format(' Process: End '))
