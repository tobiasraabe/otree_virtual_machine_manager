# -*- coding: utf-8 -*-

import click

from . import HOME
from ..handlers.nginx import NginxConfigHandler
from ..handlers.postgres import PostgreSQLDatabaseHandler
from ..handlers.samba import SambaConfigHandler
from ..prompts.defaults import get_dummy_user
from .backup_user import backup_user
from plumbum.cmd import sudo


def delete_user():
    """This command removes a user existing in the user database.

    .. note::
        The following steps are performed.

        #. Look up a user name in the user database
        #. Ask whether a backup should be made (calls ``def backup_user``)
        #. Remove Ubuntu user with home directory
        #. Remove Nginx configuration
        #. Close open ports
        #. Delete Samba configuration
        #. Remove user config in ``/ovmm/user_configs/``

    """

    http_port = None

    click.echo('\n{:-^60}'.format(' Process: Delete User '))

    default = get_dummy_user()
    user_name = click.prompt(
        'Which user do you want to delete?', default=default['user_name'])
    if click.confirm('Do you want a database backup?', default=True):
        backup_user(user_name)

    try:
        http_port, ssl_port = PostgreSQLDatabaseHandler.delete_user(user_name)
    except:
        pass

    try:
        sudo['userdel', '--remove', user_name]()
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
        sudo['ufw', 'deny', http_port]()
        sudo['ufw', 'deny', ssl_port]()
    except:
        pass

    try:
        samba = SambaConfigHandler()
        samba.delete_user(user_name)
    except:
        pass

    try:
        sudo['rm', HOME + '/ovmm/user_configs/{}'.format(user_name)]
    except:
        pass

    click.secho('\nThe deletion process is completed. If an error occured,\n'
                'check the failing yourself.', fg='yellow')
    click.echo('{:-^60}\n'.format(' Process: End '))
