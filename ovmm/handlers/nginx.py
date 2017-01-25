# -*- coding: utf-8 -*-

import click
import sys

from ..templates.nginx_config import NGINX_CONF
from plumbum.cmd import sudo


class NginxConfigHandler:
    """This class contains a handler for Nginx configurations.

    """

    def __init__(self):
        self.check_integrity()

    @staticmethod
    def check_integrity():
        """This functions performs an integrity check of the nginx
        configuration by calling ``sudo nginx -s reload``.

        """

        try:
            nginx_reload_command = sudo['nginx', '-s', 'reload'].run()
        except Exception as e:
            if nginx_reload_command[0] != 0:
                sys.exit('Unfortunately, nginx configuration is corrupt. Run'
                         '"nginx -s reload" to locate the error.\n{}'
                         .format(e))
        else:
            click.secho('The nginx configuration is fine.', fg='green')

    def add_user(self, dict_user):
        """This functions adds a new user to the nginx configuration.

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
                  .format(**dict_user), 'w') as file:
            file.write(
                NGINX_CONF
                .replace('OTREEHOME', '/home/{user_name}/oTree/'
                         .format(**dict_user))
                .replace('HTTPPORT', str(dict_user['http_port']))
                .replace('SSLPORT', str(dict_user['ssl_port']))
                .replace('DAPHNEPORT', str(dict_user['daphne_port']))
            )
        # Enable new page via symlink to sites-enabled
        sudo['ln', '-s', '/etc/nginx/sites-available/{user_name}'
             .format(**dict_user), '/etc/nginx/sites-enabled/']()

        # Check integrity after insertion
        click.secho('The user was successfully added to nginx configuration.',
                    fg='green')
        self.check_integrity()

    def delete_user(self, user_name):
        """Deletes a user entry from nginx configuration.

        Parameters
        ----------
        user_name : str
            Name of a user account

        """

        sudo['rm', '/etc/nginx/sites-enabled/{}'.format(user_name)]()
        sudo['rm', '/etc/nginx/sites-available/{}'.format(user_name)]()

        # Check integrity after deletion
        self.check_integrity()
        click.secho('User was successfully removed from nginx configuration.',
                    fg='green')
