# -*- coding: utf-8 -*-

import click


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


@click.group(cls=AliasedGroup)
def main():
    """These scripts help the server admin to perform user related commands."""


@main.command()
def add_user():
    """Creates an account for an experimenter."""
    from .commands.add_user import add_user as add_usr
    add_usr()


@main.command()
def backup_user():
    """Creates a database backup for a user."""
    from .commands.backup_user import backup_user as backup_usr
    backup_usr()


@main.command()
def count_user():
    """Counts all user accounts."""
    from .commands.count_user import count_user as count_usr
    count_usr()


@main.command()
def delete_user():
    """Deletes an account of an experimenter."""
    from .commands.delete_user import delete_user as delete_usr
    delete_usr()


@main.command()
def initialise():
    """Prepares for using the scripts."""
    from .commands.initialise import initialise as init
    init()


@main.command()
def list_user():
    """Lists all user accounts."""
    from .commands.list_user import list_user as list_usr
    list_usr()
