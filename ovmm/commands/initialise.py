"""This module contains the ``initialise`` command."""

import os
from getpass import getuser

import click
import pkg_resources
import plumbum
from plumbum.cmd import sudo

from ovmm.config.static import HOME, OSF
from ovmm.handlers.nginx import NginxConfigHandler
from ovmm.prompts.parsers import parse_host
from ovmm.prompts.parsers import parse_lower_alpha
from ovmm.prompts.parsers import parse_password
from ovmm.prompts.parsers import parse_port
from ovmm.prompts.parsers import parse_table_name
from ovmm.prompts.parsers import parse_user_name

ADMIN = os.path.expanduser('~').split('/')[-1]


@click.command()  # noqa: C901
@click.option('--optional-packages/--no-optional-packages', default=False)
def initialise(optional_packages: bool):
    """Set system up for ovmm.

    This initialisation of the environment is necessary since some of the
    commands communicate with other parts of the system (e.g.
    PostgreSQL database) or need information about the infrastructure
    (e.g. port handling).

    Parameter
    ---------
    optional : bool
        Flag for optional packages

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

    click.echo('Installing Ubuntu dependencies...')
    try:
        software = ['p7zip-full']
        if optional_packages:
            software += [
                'ftp', 'nginx', 'samba', 'screen', 'mailutils', 'ssh',
                'ufw', 'postgresql', 'git', 'postgresql-server-dev-all',
                'python3-pip', 'zenity', 'python3-venv', 'redis-server',
                'xterm', 'pgadmin3']
        with click.progressbar(software,
                               label='Installing programs') as bar:
            for program in bar:
                sudo['apt-get', 'install', '-y', program]()
    except plumbum.ProcessExecutionError as e:
        click.secho(e, fg='red')
    else:
        click.secho('SUCCESS: Requirement satisfied.', fg='green')

    click.echo('Installing OVMM related content.')
    try:
        click.echo("--> Get administrator's password.")
        admin_password = click.prompt(
            "Enter oTree GUI administrator's password", hide_input=True,
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
            'Enter PostgreSQL administrator password', hide_input=True,
            confirmation_prompt=True, value_proc=parse_password)

        if click.confirm('If the PostgreSQL superuser exists, set password?',
                         default=True):
            sudo['-u', 'postgres', 'psql', '-c',
                 "ALTER ROLE {} PASSWORD '{}';"
                 .format(psql_user, psql_password)]()

        click.echo('--> The content folder will be created under {}'
                   .format(os.path.join(HOME, OSF)))

        try:
            os.mkdir(os.path.join(HOME, OSF))
        except FileExistsError:
            pass

        for folder in ['user_configs', 'user_backups']:
            try:
                os.mkdir(os.path.join(HOME, OSF, folder))
            except FileExistsError:
                pass

        for nginx_template in ['nginx_template', 'nginx_default_template']:
            path_nginx_template = pkg_resources.resource_filename(
                'ovmm', 'static/{}'.format(nginx_template))
            path_nginx_user = os.path.join(HOME, OSF, nginx_template)
            if os.path.isfile(os.path.join(HOME, OSF, nginx_template)):
                if click.confirm('WARNING: {} exists. Overwrite?'.format(
                                 nginx_template), default=False):
                    sudo['cp', path_nginx_template, path_nginx_user]()
                else:
                    pass
            else:
                sudo['cp', path_nginx_template, path_nginx_user]()

        # Add ovmm_conf.yml
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
        # Add ovmm_conf.yml to admin
        with open(os.path.join(HOME, '.bashrc'), 'a') as profile:
            profile.write('\n')
            profile.write('source ' + os.path.join(HOME, OSF, 'ovmm_conf.yml'))

        sudo['chown', '-R', '{0}:{0}'.format(ADMIN),
             os.path.join(HOME, OSF)]()

        # add default nginx config directory create and reroute default port
        # config to port 8000 and current user symlink
        # /opt/nginx_default/default to /etc/nginx_sites-available
        nginx_default = os.path.join(HOME, OSF, 'nginx_default_template')
        current_user = getuser()

        if os.path.isdir('/opt/nginx_default'):
            pass
        else:
            os.mkdir('/opt/nginx_default')
            with open('/opt/nginx_default/default', 'w') as file_out:
                with open(nginx_default) as file_in:
                    file_out.write(
                        file_in.read()
                        .replace('OTREEHOME', os.path.join(
                            '/home', current_user, '.oTree'))
                        .replace('DAPHNEPORT', '8000'))

            # move stdrd nginx config to backup & symlink new one
            sudo['mv', '/etc/nginx/sites-available/default',
                 '/etc/nginx/sites-available/_bkp_default']()
            sudo['ln', '-s', '/opt/nginx_default/default',
                 '/etc/nginx/sites-available/default']()
            # Check integrity after insertion
            NginxConfigHandler.check_integrity()

        # Open ports 80, 443 on initialisation
        sudo['ufw', 'allow', 'ftp']()
        sudo['ufw', 'allow', 'samba']()
        sudo['ufw', 'allow', 'Nginx Full']()
        sudo['service', 'ufw', 'restart']()

    except Exception as e:
        click.secho(e, 'red')
    else:
        click.secho('SUCCESS: Requirement satisfied.', fg='green')

    click.secho(
        'WARNING: End of initialisation. Fix possible errors before\n'
        'running anything else!', fg='yellow')
    click.echo('{:-^60}\n'.format(' Process: End '))
