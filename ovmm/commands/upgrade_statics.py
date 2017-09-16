# -*- coding: utf-8 -*-

import os

import click
import pkg_resources
from plumbum.cmd import sudo

from ovmm.handlers.postgres import PostgreSQLDatabaseHandler


@click.command()
def upgrade_statics():
    """Upgrades static files for all users.

    This command helps to equip all existing user accounts with updated
    versions of ovmm's desktop helpers, etc..

    """

    click.echo('\n{:-^60}'.format(' Process: Upgrade Statics '))

    # Collect all user names
    postgres = PostgreSQLDatabaseHandler()
    user_list = postgres.list_user()

    # Create path to statics archive
    archive = pkg_resources.resource_filename(
        'ovmm', 'static/exp_env.7z')

    # Extract and overwrite statics for each user
    for user in user_list:
        sudo['-u', user, '7z', 'x', archive,
             '-o' + os.path.join('/home', user), '-y']()
        click.secho('SUCCESS: Updated statics for {}'.format(user), fg='green')

    click.echo('{:-^60}\n'.format(' Process: End '))
