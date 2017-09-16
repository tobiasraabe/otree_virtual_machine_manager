# -*- coding: utf-8 -*-

import os
import sys

import click

from .commands.add_user import add_user
from .commands.backup_user import backup_user
from .commands.count_user import count_user
from .commands.delete_user import delete_user
from .commands.initialise import initialise
from .commands.list_user import list_user
from .commands.route_port import route_port
from .commands.upgrade_statics import upgrade_statics

# Add multiple help options
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# Add shorter aliases for commands
class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.version_option()
def main():
    """These scripts help the server admin to perform user related tasks."""
    if os.geteuid() != 0:
        click.secho(
            'ERROR: Start the program with sudo or otherwise commands\n'
            'would fail. Forced exit.', fg='red')
        sys.exit(0)


main.add_command(add_user)
main.add_command(backup_user)
main.add_command(count_user)
main.add_command(delete_user)
main.add_command(initialise)
main.add_command(list_user)
main.add_command(route_port)
main.add_command(upgrade_statics)
