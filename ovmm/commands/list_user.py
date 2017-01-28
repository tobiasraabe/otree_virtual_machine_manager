# -*- coding: utf-8 -*-

import click

from ..handlers.postgres import PostgreSQLDatabaseHandler


def list_user():
    """This command queries user names from the user database and echoes them
    to shell.

    """

    click.echo('\n{:-^60}'.format(' Process: List Users '))
    postgres = PostgreSQLDatabaseHandler()
    user_list = postgres.list_user()

    click.echo('\nList of user names:\n')
    for i in user_list:
        click.echo(i)
    click.echo('\n')
    click.echo('{:-^60}\n'.format(' Process: End '))
