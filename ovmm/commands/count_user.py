# -*- coding: utf-8 -*-

import click

from ..handlers.postgres import PostgreSQLDatabaseHandler


def count_user():
    """This command gives you information about the current number of accounts
    and the limit of additional accounts.

    It subtracts the minimum number of available ports of all ports
    (Daphne, Http, SSL, Redis) with the current number of user accounts in the
    user database.

    """

    click.echo('\n{:-^60}'.format(' Process: Count User '))
    postgres = PostgreSQLDatabaseHandler()
    postgres.count_user()
    click.echo('{:-^60}\n'.format(' Process: End '))
