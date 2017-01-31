# -*- coding: utf-8 -*-

import sys

import click
from plumbum.cmd import sudo

from . import HOME
from .backup_user import backup_user
from ..handlers.nginx import NginxConfigHandler
from ..handlers.postgres import PostgreSQLDatabaseHandler
from ..handlers.samba import SambaConfigHandler
from ..prompts.defaults import get_dummy_user


def delete_user(dict_user: dict = None):
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

    if dict_user is None:
        default = get_dummy_user()
        user_name = click.prompt(
            'Which user do you want to delete?', default=default['user_name'])

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

    try:
        sudo['userdel', '--remove', dict_user['user_name']](retcode=(0, 6))
        click.secho('SUCCESS: Removed user and home directory.'
                    .format(dict_user['user_name']), fg='green')

        nch = NginxConfigHandler()
        nch.delete_user(dict_user['user_name'])

        sudo['ufw', 'deny', dict_user['http_port']]()
        sudo['ufw', 'deny', dict_user['ssl_port']]()

        samba = SambaConfigHandler()
        samba.delete_user(dict_user['user_name'])

        sudo['rm', HOME + '/ovmm_sources/user_configs/{}'
             .format(dict_user['user_name'])](retcode=1)
    except Exception as e:
        click.secho(
            'ERROR: An exception was raised during the deletion process.\n'
            'Please, fix the problem manually. After that, run the command\n'
            'again, so that the user will also be deleted from database.',
            fg='red'
        )
        raise e
    else:
        PostgreSQLDatabaseHandler.delete_user(dict_user['user_name'])

    click.secho('\nWARNING: The deletion process is completed. If an error\n'
                'occurred, check it manually.\n', fg='yellow')
    click.echo('{:-^60}\n'.format(' Process: End '))
