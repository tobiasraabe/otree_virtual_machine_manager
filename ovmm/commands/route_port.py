"""This module contains the ``route_port`` command."""

import sys

import click

from ovmm.handlers.nginx import NginxConfigHandler
from ovmm.handlers.postgres import PostgreSQLDatabaseHandler
from ovmm.prompts.defaults import get_dummy_user
from ovmm.prompts.validators import validate_user_name

DUMMY_USER = get_dummy_user()


@click.command()
@click.option('--user_name', '-u', help='Specify user name.', prompt=True,
              callback=validate_user_name, default=DUMMY_USER['user_name'])
def route_port(user_name: str):
    """Reroute main port 80 to other user.

    This option is needed for networks which restrict access to standard ports.
    The admin has the possibility to assign ports to the experimenter who
    wants to run an experiment.

    Parameter
    ---------
    user_name : str
        User name

    """
    click.echo('\n{:-^60}'.format(' Process: Route Main Port'))

    dict_user = PostgreSQLDatabaseHandler.get_user(user_name)
    if dict_user is None:
        click.secho(
            'ERROR: User {} does not exist in database!'
            .format(user_name), fg='red')
        sys.exit(0)
    else:
        nch = NginxConfigHandler()
        nch.route_main_port(dict_user)
