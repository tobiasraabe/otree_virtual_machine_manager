"""This module contains the ``backup_user`` command."""

import os
import sys
import time

import click
import plumbum
from plumbum.cmd import sudo

from ovmm.config.static import HOME, OSF, USER_BACKUPS
from ovmm.handlers.postgres import PostgreSQLDatabaseHandler
from ovmm.prompts.defaults import get_dummy_user
from ovmm.prompts.validators import validate_user_name

DUMMY_USER = get_dummy_user()


@click.command()
@click.option('--user_name', '-u', help='Specify user name.',
              prompt='User name', callback=validate_user_name,
              default=DUMMY_USER['user_name'])
@click.option('--strategy', '-s', help='Specify backup strategy.',
              prompt='Choose a backup strategy',
              type=click.Choice(['full', 'db', 'home']), default='full')
def backup_user(user_name: str, strategy: str):
    r"""Create a backup of an user account.

    \b
    Use --strategy to specify the target.
        - full: Home folder and database
        - db:   Only database
        - home: Only home folder (requires more space)

    \b
    Parameters
    ----------
    user_name : str
        User name
    strategy : str
        Specifies which backup strategy will be used

    \b
    Raises
    ------
    plumbum.ProcessExecutionError
        If database backup for user failed.

    \b
    .. note::
        The following steps are performed.
        \b
        #. If no user_name is provided, ask for it
        #. Check if user exists in database, else exit
        #. If no folder for backups exists, create it
        #. Dependent on strategy, run the desired backup process

    """
    click.echo('{:-^60}\n'.format(' Process: back_user '))

    # Check if user exists
    postgres_check = PostgreSQLDatabaseHandler.get_user(user_name)
    if postgres_check is None:
        click.secho('ERROR: user {} does not exist in database!'
                    .format(user_name), fg='red')
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
    if strategy in ['home', 'full']:
        try:
            sudo['7z', 'a', home_file_name, os.path.join('/home', user_name)]()
        except plumbum.ProcessExecutionError:
            click.secho('ERROR: {} does not exist in the database!'
                        .format(user_name), fg='red')
            raise
    if strategy in ['db', 'full']:
        try:
            (sudo['su', '-', 'postgres', '-c', 'pg_dump', user_name] |
             sudo['7z', 'a', '-si', db_file_name])()
        except plumbum.ProcessExecutionError:
            click.secho('ERROR: {} does not exist in the database!'
                        .format(user_name), fg='red')
            raise

    click.secho('A backup of the database was successfully created',
                fg='green')
    click.echo('{:-^60}\n'.format(' Process: End '))
