# -*- coding: utf-8 -*-

import click

from otree_ubuntu_server_manager import commands


@click.group()
def cli():
    """These scripts help the server admin to perform user related commands."""
    pass


@cli.command()
def add_user(args=None):
    """Creates an account for an experimenter."""
    commands.add_user.add_user()


@cli.command()
def backup_user(args=None):
    """Creates a database backup for a user."""
    commands.backup_user.backup_user()


@cli.command()
def count_user(args=None):
    """Counts all user accounts."""
    commands.count_user.count_user()


@cli.command()
def delete_user(args=None):
    """Deletes an account of an experimenter."""
    commands.delete_user.delete_user()


@cli.command()
def initialise(args=None):
    """Prepares for using the scripts."""
    commands.initialise.initialise()


@cli.command()
def list_user(args=None):
    """Lists all user accounts."""
    commands.list_user.list_user()
