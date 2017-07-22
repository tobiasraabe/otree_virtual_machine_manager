# -*- coding: utf-8 -*-

import click
import sys

from ovmm.commands.list_user import list_user
from ovmm.handlers.nginx import NginxConfigHandler
from ovmm.handlers.postgres import PostgreSQLDatabaseHandler
from ovmm.prompts.defaults import get_dummy_user
from ovmm.prompts.parsers import parse_user_name


def route_port(dict_user: dict = None, instant_route: bool = False):
    """This command reroutes the main port 80 to one of the user otrees. This
    option is needed for networks which restrict access to standard ports.

    """

    click.echo('\n{:-^60}'.format(' Process: Route Main Port'))

    if instant_route is True:
        pass
    else:
        if click.confirm('Do you want to see a list of user accounts?',
                         default=True):
            list_user()
        if dict_user is None:
            default = get_dummy_user()
            user_name = click.prompt(
                'Provide the user account to route port 80 to?',
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

    nch = NginxConfigHandler()
    nch.route_main_port(dict_user)
