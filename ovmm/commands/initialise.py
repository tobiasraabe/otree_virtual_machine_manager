# -*- coding: utf-8 -*-

import os
import pwd

import click
import pkg_resources
import plumbum

from ovmm.prompts.parsers import parse_host
from ovmm.prompts.parsers import parse_lower_alpha
from ovmm.prompts.parsers import parse_password
from ovmm.prompts.parsers import parse_port
from ovmm.prompts.parsers import parse_table_name
from ovmm.prompts.parsers import parse_user_name
from plumbum.cmd import sudo


HOME = os.path.expanduser('~')
OSF = 'ovmm_sources'
ADMIN = os.environ.get('SUDOUSER', pwd.getpwuid(os.getuid())[0])


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
        #. Installing OVMM related content (e.g. ``ovmm_conf.yml``)

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
        click.echo("--> Get administrator's password.")
        admin_password = click.prompt(
            "Enter administrator's password.", hide_input=True,
            confirmation_prompt=True, value_proc=parse_password)
        click.echo('--> Set information for the postgres database.')
        psql_user = click.prompt(
            'Enter PostgreSQL superuser name', default='postgres',
            value_proc=parse_user_name)
        psql_database = click.prompt(
            'Enter a database name', default='postgres',
            value_proc=parse_lower_alpha)
        psql_host = click.prompt(
            'Enter the host', default='localhost', value_proc=parse_host)
        psql_port = click.prompt(
            'Enter the port', default='5432', value_proc=parse_port)
        psql_table = click.prompt(
            'Enter a name for the user table', default='user_table',
            value_proc=parse_table_name)
        psql_password = click.prompt(
            'Enter the password for the user', hide_input=True,
            confirmation_prompt=True, value_proc=parse_password)

        if click.confirm('If the PostgreSQL superuser exists, set password?',
                         default=True):
            sudo['-u', 'postgres', 'psql', '-c',
                 "ALTER ROLE {} PASSWORD '{}';"
                 .format(psql_user, psql_password)]()

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
        sudo['cp', nginx_template_path, os.path.join(HOME, 'nginx_template')]()

        ovmm_env_path = pkg_resources.resource_filename(
            'ovmm', 'static/ovmm_conf.yml')
        with open(ovmm_env_path) as file_input:
            with open(os.path.join(HOME, OSF, 'ovmm_conf.yml'),
                      'w') as file_output:
                file_output.write(
                    file_input.read().replace('__USER__', psql_user)
                                     .replace('__PASSWORD__', psql_password)
                                     .replace('__DBNAME__', psql_database)
                                     .replace('__HOST__', psql_host)
                                     .replace('__PORT__', psql_port)
                                     .replace('__TABLE__', psql_table)
                                     .replace('__ADMIN__', admin_password))

        sudo['chown', '-R', '{0}:{0}'.format(ADMIN),
             os.path.join(HOME, 'nginx_template'),
             os.path.join(HOME, OSF)]()

    except Exception as e:
        click.secho(e, 'red')
        pass
    else:
        click.secho('SUCCESS: Requirement satisfied.', fg='green')

    click.secho(
        'WARNING: End of initialisation. Fix possible errors before\n'
        'running anything else!', fg='yellow')
    click.echo('{:-^60}\n'.format(' Process: End '))
