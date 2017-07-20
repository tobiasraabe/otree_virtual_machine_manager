# -*- coding: utf-8 -*-

import os

import click
from plumbum import ProcessExecutionError
from plumbum.cmd import sudo

# from ovmm.config.settings import
HOME = os.path.expanduser('~')
OSF = 'ovmm_sources'


class NginxConfigHandler:
    """This class contains a handler for Nginx configurations.

    For each user a Nginx configuration file is created with distinct values
    for ports, etc.

    Attributes
    ----------
    self.path : str
        Path to ``nginx_template`` in the administrator's directory

    """

    path = os.path.join(HOME, OSF, 'nginx_template')
    nginx_default = os.path.join(HOME, OSF, 'nginx_default_template')

    def __init__(self):
        self.check_integrity()

    @staticmethod
    def check_integrity():
        """This functions performs an integrity check of the Nginx
        configuration by calling ``sudo nginx -s reload``.

        """

        try:
            sudo['nginx', '-s', 'reload']()
        except ProcessExecutionError:
            click.secho(
                'ERROR: nginx configuration is corrupt. Run\n'
                '"sudo nginx -s reload" to locate the error.', fg='red')
        else:
            click.secho('SUCCESS: nginx configuration works.', fg='green')

    def add_user(self, dict_user: dict):
        """This functions adds a new user to the Nginx configuration.

        This function creates a configuration file in
        ``/etc/nginx/sites-available/`` and symlinks the file to
        ``/etc/nginx/sites-enabled/``. After that, it calls
        ``def check_integrity``.

        Parameters
        ----------
        dict_user : dict
            A dictionary containing user information

        """

        with open('/etc/nginx/sites-available/{user_name}'
                  .format(**dict_user), 'w') as file_out:
            with open(self.path) as file_in:
                file_out.write(
                    file_in.read()
                    .replace('OTREEHOME',
                             os.path.join('/home', dict_user['user_name'],
                                          '.oTree'))
                    .replace('SSLPORT', str(dict_user['ssl_port']))
                    .replace('DAPHNEPORT', str(dict_user['daphne_port']))
                )
        # Enable new page via symlink to sites-enabled
        sudo['ln', '-s', '/etc/nginx/sites-available/{user_name}'
             .format(**dict_user), '/etc/nginx/sites-enabled/']()

        # Check integrity after insertion
        click.secho('SUCCESS: Added user to nginx configuration.',
                    fg='green')
        self.check_integrity()

    def delete_user(self, user_name: str):
        """Deletes a user entry from Nginx configuration.

        The Nginx configuration file in
        ``/etc/nginx/sites_available/<user_name>`` and its symlink is removed.

        Parameters
        ----------
        user_name : str
            Name of a user account

        """

        sudo['rm', '/etc/nginx/sites-enabled/{}'
             .format(user_name)](retcode=(0, 1))
        sudo['rm', '/etc/nginx/sites-available/{}'
             .format(user_name)](retcode=(0, 1))

        # Check integrity after deletion
        self.check_integrity()
        click.secho(
            'SUCCESS: Removed user from nginx configuration.', fg='green')

    def route_main_port(self, dict_user: dict):
        """This functions adds a new user to the Nginx configuration.

        This function creates a configuration file in
        ``/etc/nginx/sites-available/`` and symlinks the file to
        ``/etc/nginx/sites-enabled/``. After that, it calls
        ``def check_integrity``.

        Parameters
        ----------
        dict_user : dict
            A dictionary containing user information

        """

        with open('/opt/nginx_default/default'
                  .format(**dict_user), 'w') as file_out:
            with open(self.nginx_default) as file_in:
                file_out.write(
                    file_in.read()
                    .replace('OTREEHOME',
                             os.path.join('/home', dict_user['user_name'],
                                          '.oTree'))
                    .replace('DAPHNEPORT', str(dict_user['daphne_port']))
                )
        # Check integrity after insertion
        self.check_integrity()
