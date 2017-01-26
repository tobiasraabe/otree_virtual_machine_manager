#!/usr/bin/env python3

"""This document contains everything related to Samba operations.

"""

import click

from plumbum import ProcessExecutionError
from plumbum.cmd import sudo


class SambaConfigHandler:
    """This class contains all operations related to Samba configuration.

    Attributes
    ----------
    path : str
        Path to samba config

    """

    path = '/etc/samba/smb.conf'

    def __init__(self):
        """Checks integrity and performs a backup of current smb.conf in
        advance of further actions.

        """

        self.check_integrity()
        self.make_backup()

    def check_integrity(self):
        """Checks integrity after transaction.

        """

        try:
            sudo['testparm']()
        except ProcessExecutionError:
            self.restore_backup()
            click.secho(
                'Unfortunately, smb.conf was corrupt after the change.\n'
                'The former configuration was restored.', fg='red')
        except Exception as e:
            raise e
        else:
            click.secho('The smb.conf is working properly.', fg='green')

    def make_backup(self):
        """Creates a backup of ``smb.conf`` named ``smb.conf.bak``.

        """

        try:
            click.secho('Make backup of current smb.conf.', fg='yellow')
            sudo['cp', self.path, self.path + '.bak']()
        except Exception as e:
            raise e
        else:
            click.secho(
                'A backup of smb.conf was successfully created.', fg='green')

    def restore_backup(self):
        """Restores the current backup of the ``smb.conf`` named
        ``smb.conf.bak``.

        """

        try:
            sudo['cp', self.path + '.bak', self.path]()
        except Exception as e:
            click.secho(
                'Something went wrong during restoration of smb.conf. Upps.',
                fg='red')
            raise e
        else:
            click.secho('The backup of smb.conf was successfully restored.',
                        fg='green')

    def add_user(self, dict_user: dict):
        """Adds a user entry at the end of smb.conf.

        Examples
        --------
        A user entry looks like the following:

        ``
        [user_name]
            path = /home/user_name
            valid users = user_name
            read only = no
        ``

        Parameters
        ----------
        dict_user : dict
            A dict of user information containing port number

        """

        try:
            with open(self.path, 'a') as file:
                file.write('\n[{user_name}]\n'.format(**dict_user))
                file.write('\tpath = /home/{user_name}/\n'.format(**dict_user))
                file.write('\tvalid users = {user_name}\n'.format(**dict_user))
                file.write('\tread only = no\n')
        except Exception as e:
            self.restore_backup()
            raise e
        else:
            self.check_integrity()
            click.secho(
                'The user was successfully added to smb.conf.', fg='green')

    def delete_user(self, user_name: str):
        """Deletes a user entry from smb.conf by writing a new file which skips
        all lines related to distinct ``user_name``.

        Parameters
        ----------
        user_name : str
            Name of user account

        """

        arr = []
        with open(self.path, 'r') as input_file:
            with open(self.path + '_temp', 'w') as output_file:
                for i, line in enumerate(input_file):
                    if line.startswith('[{}]'.format(user_name)):
                        arr.extend([i + j for j in range(5)])
                        pass
                    elif i in arr:
                        pass
                    else:
                        output_file.write(line)
        sudo['mv', self.path + '_temp', self.path]()
        click.secho('User was successfully removed from smb.conf.', fg='green')
