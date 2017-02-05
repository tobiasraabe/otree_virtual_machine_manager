# -*- coding: utf-8 -*-

import os

import click
import pkg_resources
import plumbum
from plumbum.cmd import sudo


OSF = os.environ.get('OVMM_SOURCE_FOLDER', 'ovmm_sources')
HOME = os.path.expanduser('~')


def initialise():
    """This command prepares the environment for further commands.

    This initialisation of the environment is necessary since some of the
    commands communicate with other parts of the system (e.g.
    PostgreSQL database) or need information about the infrastructure
    (e.g. port handling).

    Warning
    -------
    This command should be executed **in advance** to any use of
    ``ovmm`` on a new system. It checks whether all
    dependencies are satisfied. **An internet connection is needed.**

    .. note::
        The following steps are performed.

        #. Installing Ubuntu dependencies
        #. Installing OVMM related content (e.g. ``.ovmm_env``)

    """

    click.echo('\n{:-^60}'.format(' Process: Init '))

    click.echo('Installing ubuntu dependencies...')
    try:
        click.echo('--> Installing 7z')
        sudo['apt-get', 'install', 'p7zip-full']()
    except plumbum.ProcessExecutionError as e:
        click.secho(e, fg='red')
        pass
    else:
        click.secho('SUCCESS: Requirement satisfied.', fg='green')

    click.echo('Installing OVMM related content.')
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

        click.echo('--> The content folder will be created under {}'
                   .format(os.path.join(HOME, OSF)))

        if os.path.isdir(os.path.join(HOME, OSF)):
            click.confirm(
                'WARNING: {} already exists. You could overwrite important'
                '\nfiles. You Do you want to continue?'
                .format(os.path.join(HOME, OSF)), abort=True)
        else:
            os.mkdir(os.path.join(HOME, OSF))
        for folder in ['user_configs', 'user_backups']:
            if not os.path.isdir(os.path.join(HOME, OSF, folder)):
                os.mkdir(os.path.join(HOME, OSF, folder))

        nginx_template_path = pkg_resources.resource_filename(
            'ovmm', 'static/nginx_template')
        sudo['cp', nginx_template_path, os.path.join(HOME, OSF, '.ovmm_env')]()

        ovmm_env_path = pkg_resources.resource_filename(
            'ovmm', 'static/.ovmm_env')
        with open(ovmm_env_path) as file_input:
            with open(os.path.join(HOME, OSF, '.ovmm_env'),
                      'w') as file_output:
                file_output.write(
                    file_input.read().replace('_USER_', psql_user)
                                     .replace('_PASSWORD_', psql_password)
                                     .replace('_DBNAME_', psql_database)
                                     .replace('_HOST_', psql_host)
                                     .replace('_PORT_', psql_port)
                                     .replace('_TABLE_', psql_table))
        with open(os.path.join(HOME, '.profile'), 'a') as file:
            file.write('\n')
            file.write('\n# Source environmental variables for OVMM')
            file.write('\nsource ovmm_sources/.ovmm_env')
        sudo['source', os.path.join(HOME + '.profile')]()
    except Exception as e:
        click.secho(e, 'red')
        pass
    else:
        click.secho('SUCCESS: Requirement satisfied.', fg='green')

    click.echo('WARNING: End of initialisation. Fix possible errors before\n'
               'running anything else!')
    click.echo('{:-^60}\n'.format(' Process: End '))
