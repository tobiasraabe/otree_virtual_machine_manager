# -*- coding: utf-8 -*-

import click

from ovmm.handlers.postgres import PostgreSQLDatabaseHandler


@click.command()
def count_user():
    """Prints current/possible number of accounts.

    It subtracts the minimum number of available ports of all ports
    (Daphne, SSL, Redis) with the current number of user accounts in the
    user database and prints the results.

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
