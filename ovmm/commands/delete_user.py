# -*- coding: utf-8 -*-

import os
import sys

import click

from plumbum.cmd import sudo

from ovmm.commands.backup_user import backup_user
from ovmm.commands.list_user import list_user
from ovmm.config.settings import HOME
from ovmm.config.settings import OSF
from ovmm.config.settings import USER_CONFIGS
from ovmm.handlers.nginx import NginxConfigHandler
from ovmm.handlers.postgres import PostgreSQLDatabaseHandler
from ovmm.handlers.samba import SambaConfigHandler
from ovmm.prompts.defaults import get_dummy_user
from ovmm.prompts.parsers import parse_user_name


def delete_user(dict_user: dict = None, instant_del: bool = False):
    """This command removes a user existing in the user database.

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

    if instant_del is True:
        pass
    else:
        if click.confirm('Do you want to see a list of users?', default=True):
            list_user()
        if dict_user is None:
            default = get_dummy_user()
            user_name = click.prompt(
                'Which user do you want to delete?',
                default=default['user_name'], value_proc=parse_user_name)

            dict_user = PostgreSQLDatabaseHandler.get_user(user_name)
            if dict_user is None:
                click.secho(
                    'ERROR: User {} does not exist in database!'
                    .format(user_name), fg='red'
                )
                sys.exit(0)
            else:
                pass
        else:
            pass

        if click.confirm('Do you want a database backup?', default=True):
            backup_user(dict_user['user_name'])
        else:
            pass

    exception_raised = False
    try:
        sudo['pkill', '-u', dict_user['user_name']](retcode=2)
        sudo['userdel', '--remove', dict_user['user_name']](retcode=(0, 6))
        click.secho('SUCCESS: Removed user and home directory.'
                    .format(dict_user['user_name']), fg='green')
    except Exception as e:
        click.secho('ERROR: User could not be deleted.', fg='red')
        click.echo(e)
        exception_raised = True
        pass

    try:
        nch = NginxConfigHandler()
        nch.delete_user(dict_user['user_name'])
    except Exception as e:
        click.secho(
            'ERROR: Nginx configuration could not be deleted.', fg='red')
        click.echo(e)
        exception_raised = True
        pass

    try:
        sudo['ufw', 'deny', dict_user['ssl_port']]()
    except Exception as e:
        click.secho('ERROR: Ports could not be closed.', fg='red')
        click.echo(e)
        exception_raised = True
        pass

    try:
        samba = SambaConfigHandler()
        samba.delete_user(dict_user['user_name'])
    except Exception as e:
        click.secho(
            'ERROR: User could not be deleted from Samba configuration',
            fg='red')
        click.echo(e)
        exception_raised = True
        pass

    try:
        sudo['rm', os.path.join(
            HOME, OSF, USER_CONFIGS,
            '{}.txt'.format(dict_user['user_name']))](retcode=1)
    except Exception as e:
        click.secho(
            'ERROR: User configuration text file could not be deleted.',
            fg='red')
        click.echo(e)
        exception_raised = True
        pass

    if exception_raised:
        click.secho(
            'ERROR: An exception was raised during the deletion process.\n'
            'Please, fix the problem manually. After that, run the command\n'
            'again, so that the user will also be deleted from database.',
            fg='red'
        )
    else:
        PostgreSQLDatabaseHandler.delete_user(dict_user['user_name'])

    click.secho('\nWARNING: The deletion process is completed. If an error\n'
                'occurred, check it manually.\n', fg='yellow')
    click.echo('{:-^60}\n'.format(' Process: End '))
