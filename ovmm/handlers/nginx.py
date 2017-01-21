# -*- coding: utf-8 -*-

import click
import sys

from ..templates.nginx_config import NGINX_CONF
from plumbum.cmd import ln
from plumbum.cmd import nginx
from plumbum.cmd import rm
from plumbum.cmd import sudo


class NginxConfigHandler():
    """This class contains a handler for Nginx configurations.

    """

    def __init__(self):

        self.check_integrity()

    def check_integrity(self):
        """This functions performs an integrity check of the nginx
        configuration by calling ``sudo nginx -s reload``.

        """

        try:
            a = sudo[nginx['-s', 'reload']].run()
        except Exception as e:
            if not a[0] == 0:
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

        - **parameters**::
            :dict_user: A dict of user information containing port number

        """

        with open('/etc/nginx/sites-available/{user_name}'
                  .format(**dict_user), 'w') as file:
            file.write(
                NGINX_CONF.replace('OTREEHOME', '/home/{user_name}/oTree/'
                                   .format(**dict_user))
                .replace('HTTPPORT', str(dict_user['http_port']))
                .replace('SSLPORT', str(dict_user['ssl_port']))
                .replace('DAPHNEPORT', str(dict_user['daphne_port']))
            )
        # enable new page via symlink to sites-enabled
        sudo[ln['-s', '/etc/nginx/sites-available/{user_name}'
                .format(**dict_user), '/etc/nginx/sites-enabled/']]()

        # check
        click.secho('The user was successfully added to nginx configuration.',
                    fg='green')
        self.check_integrity()

    def delete_user(self, user_name):
        """Deletes a user entry from nginx configuration.

        - **parameters**:
            :user_name: Name of a user account

        """

        sudo[rm['/etc/nginx/sites-enabled/{}'.format(user_name)]]()
        sudo[rm['/etc/nginx/sites-available/{}'.format(user_name)]]()

        # check
        self.check_integrity()
        click.secho('User was successfully removed from nginx configuration.',
                    fg='green')
