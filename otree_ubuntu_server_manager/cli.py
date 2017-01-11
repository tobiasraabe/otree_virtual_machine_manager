# -*- coding: utf-8 -*-

import click


@click.group()
def cli():
    """These scripts help the server admin to perform user related commands."""


@cli.command()
def add_user():
    """Creates an account for an experimenter."""
    from .commands.add_user import add_user as add_usr
    add_usr()


@cli.command()
def backup_user():
    """Creates a database backup for a user."""
    from .commands.backup_user import backup_user as backup_usr
    backup_usr()


@cli.command()
def count_user():
    """Counts all user accounts."""
    from .commands.count_user import count_user as count_usr
    count_usr()


@cli.command()
def delete_user():
    """Deletes an account of an experimenter."""
    from .commands.delete_user import delete_user as delete_usr
    delete_usr()


@cli.command()
def initialise():
    """Prepares for using the scripts."""
    from .commands.initialise import initialise as init
    init()


@cli.command()
def list_user():
    """Lists all user accounts."""
    from .commands.list_user import list_user as list_usr
    list_usr()
