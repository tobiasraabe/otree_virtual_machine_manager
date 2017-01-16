# -*- coding: utf-8 -*-

import click
import os

from . import HOME
from ..templates.ousm_settings import OUSM_SETTINGS
from plumbum.cmd import sudo


def initialise():
    """This command should be executed *in advance* to any use of
    ``otree_ubuntu_server_manager`` on a new system. It checks whether all
    dependencies are satisfied. *An internet connection is needed.*

    - The following steps are performed::
        :1: Installing Ubuntu dependencies
        :2: Installing OUSM related content
            - write ``ousm_settings.py``

    """

    click.echo('\n{:-^60}'.format(' Process: Init '))

    click.echo('Installing ubuntu dependencies...')
    try:
        click.echo('--> Installing 7z')
        sudo['apt-get', 'install', 'p7zip-full']()
    except Exception as e:
        click.secho(e, fg='red')
        pass
    else:
        click.secho('Requirement satisfied.', fg='green')

    click.echo('Installing OUSM related content.')
    try:
        click.echo('--> Set information for the postgres database.')
        psql_user = click.prompt('Enter postgres user with user database '
                                 'access', default='postgres')
        psql_database = click.prompt('Enter a database name',
                                     default='postgres')
        psql_host = click.prompt('Enter the host', default='localhost')
        psql_port = str(click.prompt('Enter the port', default=5432))
        psql_table = click.prompt('Enter a name for the user table',
                                  default='user_table')
        psql_password = click.prompt(
            'Enter the password for the user', hide_input=True,
            confirmation_prompt=True)

        if click.confirm('If the psql role exist, the password can be set for '
                         'you?'):
            sudo['-u', 'postgres', 'psql', '-c',
                 "ALTER ROLE postgres PASSWORD '{}';".format(psql_password)]()

        click.echo('--> The content folder will be created under {}/ousm'
                   .format(HOME))

        if os.path.isdir('{}/ousm'.format(HOME)):
            click.confirm(
                '{}/ousm already exists. You could overwrite important '
                'files. You Do you want to continue?'
                .format(HOME), abort=True)
        else:
            os.mkdir('{}/ousm'.format(HOME))
        for folder in ['/user_configs', '/user_backups']:
            if not os.path.isdir('{}/ousm{}'.format(HOME, folder)):
                os.mkdir('{}/ousm{}'.format(HOME, folder))

        with open(HOME + '/ousm/ousm_settings.py', 'w') as file:
            file.write(OUSM_SETTINGS.replace('_USER_', psql_user)
                                    .replace('_PASSWORD_', psql_password)
                                    .replace('_DATABASE_', psql_database)
                                    .replace('_HOST_', psql_host)
                                    .replace('_PORT_', psql_port)
                                    .replace('_TABLE_', psql_table))
    except Exception as e:
        click.secho(e, 'red')
        pass
    else:
        click.secho('Requirement satisfied.', fg='green')

    click.echo('End of initialisation. Fix possible errors before running '
               'anything else!')
    click.echo('{:-^60}\n'.format(' Process: End '))
