# -*- coding: utf-8 -*-

import click

from ovmm.handlers.postgres import PostgreSQLDatabaseHandler


def count_user():
    """This command gives you information about the current number of accounts
    and the limit of additional accounts.

    It subtracts the minimum number of available ports of all ports
    (Daphne, Http, SSL, Redis) with the current number of user accounts in the
    user database.

    """

    click.echo('\n{:-^60}'.format(' Process: Count User '))
    postgres = PostgreSQLDatabaseHandler()
    number_free_ports, number_max_ports = postgres.count_user()

    click.echo('Number of user accounts: {}'
               .format(number_max_ports - number_free_ports))
    click.echo('Limit of additional accounts: {}'.format(number_free_ports))
    if number_free_ports == 0:
        click.secho('It is not possible to add more users!', fg='red')

    click.echo('{:-^60}\n'.format(' Process: End '))
