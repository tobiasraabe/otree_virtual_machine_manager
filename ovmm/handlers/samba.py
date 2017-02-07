# -*- coding: utf-8 -*-

"""This document contains everything related to Samba operations.

"""

import click
import plumbum

# Added for testing
try:
    from plumbum.cmd import sudo
except ImportError:
    pass


class SambaConfigHandler:
    """This class contains all operations related to Samba configuration.

    Attributes
    ----------
    self.path : str
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
        except plumbum.ProcessExecutionError as ee:
            self.restore_backup()
            click.secho(
                'ERROR: Unfortunately, smb.conf was corrupt after the change.'
                '\nThe former configuration was restored.', fg='red')
            raise ee
        else:
            click.secho('SUCCESS: smb.conf works.', fg='green')

    def make_backup(self):
        """Creates a backup of ``smb.conf`` named ``smb.conf.bak``.

        """

        try:
            sudo['cp', self.path, self.path + '.bak']()
        except plumbum.ProcessExecutionError as e:
            raise e
        else:
            click.secho(
                'SUCCESS: Created backup of smb.conf.', fg='green')

    def restore_backup(self):
        """Restores the current backup of the ``smb.conf`` named
        ``smb.conf.bak``.

        """

        try:
            sudo['cp', self.path + '.bak', self.path]()
        except Exception as e:
            click.secho(
                'ERROR: Restoration of smb.conf failed.', fg='red')
            raise e
        else:
            click.secho(
                'SUCCESS: Restored smb.conf backup.', fg='green')

    def add_user(self, dict_user: dict):
        """Adds a user entry at the end of smb.conf.

        Examples
        --------
        A user entry looks like the following:

        ````
        [user_name]
            path = /home/user_name
            valid users = user_name
            read only = no
        ````

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
                'SUCCESS: Added user to smb.conf.', fg='green')

    def delete_user(self, user_name: str):
        """Deletes a user entry from smb.conf by writing a new file which skips
        all lines related to distinct ``user_name``.

        Parameters
        ----------
        user_name : str
            Name of user account

        """

        arr = []
        with open(self.path) as input_file:
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
        click.secho('SUCCESS: Removed user from smb.conf.', fg='green')
