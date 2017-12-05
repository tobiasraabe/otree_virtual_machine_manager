# -*- coding: utf-8 -*-

"""This module contains the ``delete_user`` command.

"""

import os
import sys

import click
from plumbum.cmd import sudo

from ovmm.commands.backup_user import backup_user
from ovmm.config.static import HOME, OSF, USER_CONFIGS
from ovmm.handlers.nginx import NginxConfigHandler
from ovmm.handlers.postgres import PostgreSQLDatabaseHandler
from ovmm.handlers.samba import SambaConfigHandler
from ovmm.prompts.defaults import get_dummy_user
from ovmm.prompts.validators import validate_user_name

DUMMY_USER = get_dummy_user()


@click.command()
@click.option('--user_name', '-u', help='Specify user name.', prompt=True,
              callback=validate_user_name, default=DUMMY_USER['user_name'])
@click.pass_context
def delete_user(ctx, user_name: str):
    """Removes a user.

    Parameter
    ---------
    user_name : str
        User name

    .. note::
        The following steps are performed.

        #. Look up a user name in the user database
        #. Ask whether a backup should be made (calls ``def backup_user``)
        #. Remove Ubuntu user with home directory
        #. Remove Nginx configuration
        #. Close open ports
        #. Delete Samba configuration
        #. Remove user config in ``/ovmm_sources/user_configs/``
        #. Remove entry from PostgreSQL table

    """

    click.echo('\n{:-^60}'.format(' Process: Delete User '))

    dict_user = PostgreSQLDatabaseHandler.get_user(user_name)
    if dict_user is None:
        click.secho(
            'ERROR: User {} does not exist in database!'
            .format(user_name), fg='red'
        )
        sys.exit(0)

    if click.confirm('Do you want a database backup?', default=True):
        ctx.invoke(backup_user, user_name=user_name)

    exception_raised = False
    try:
        # retcode 0: unknown, retcode 1: unkown, retcode 2: invalid user name
        sudo['pkill', '-u', dict_user['user_name']](retcode=(0, 1, 2))
        sudo['userdel', '--remove', dict_user['user_name']](retcode=(0, 6))
        click.secho('SUCCESS: Removed user {} and home directory.'
                    .format(user_name), fg='green')
    except Exception as e:
        click.secho('ERROR: User could not be deleted.', fg='red')
        click.echo(e)
        exception_raised = True

    try:
        nch = NginxConfigHandler()
        nch.delete_user(user_name)
    except Exception as e:
        click.secho(
            'ERROR: Nginx configuration could not be deleted.', fg='red')
        click.echo(e)
        exception_raised = True

    try:
        sudo['ufw', 'deny', dict_user['ssl_port']]()
    except Exception as e:
        click.secho('ERROR: Ports could not be closed.', fg='red')
        click.echo(e)
        exception_raised = True

    try:
        samba = SambaConfigHandler()
        samba.delete_user(user_name)
    except Exception as e:
        click.secho(
            'ERROR: User could not be deleted from Samba configuration',
            fg='red')
        click.echo(e)
        exception_raised = True

    try:
        # retcode 0: everythings fine, retcode 1: file not found
        sudo['rm', os.path.join(
            HOME, OSF, USER_CONFIGS,
            '{}.txt'.format(dict_user['user_name']))](retcode=(0, 1))
        click.secho('SUCCESS: Removed user config.', fg='green')
    except Exception as e:
        click.secho(
            'ERROR: User configuration text file could not be deleted.',
            fg='red')
        click.echo(e)
        exception_raised = True

    if exception_raised:
        click.secho(
            'ERROR: An exception was raised during the deletion process.\n'
            'Please, fix the problem manually. After that, run the command\n'
            'again, so that the user will also be deleted from database.',
            fg='red'
        )
    else:
        PostgreSQLDatabaseHandler.delete_user(user_name)

    click.secho('\nWARNING: The deletion process is complete. If an error\n'
                'occurred, check it manually.\n', fg='yellow')
    click.echo('{:-^60}\n'.format(' Process: End '))
