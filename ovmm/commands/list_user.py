# -*- coding: utf-8 -*-

import click

from ovmm.handlers.postgres import PostgreSQLDatabaseHandler


@click.command()
def list_user():
    """Lists users managed by ovmm.

    """

    click.echo('\n{:-^60}'.format(' Process: List Users '))

    postgres = PostgreSQLDatabaseHandler()
    user_list = postgres.list_user()

    click.echo('List of user names:')
    for i in user_list:
        click.echo(i)

    click.echo('{:-^60}\n'.format(' Process: End '))
