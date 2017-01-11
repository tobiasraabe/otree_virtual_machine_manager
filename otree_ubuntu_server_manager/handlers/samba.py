#!/usr/bin/env python3

"""This document contains everything related to Samba operations.

"""

import click
import sys

from plumbum.cmd import cp
from plumbum.cmd import mv
from plumbum.cmd import testparm


class SambaConfigHandler():
    """This class contains all operations related to Samba configuration.

        The functions are::

            :__init__:          Verifies integrity of existing smb.conf and
                                creates backup
            :check_integrity:   Verifies integrity of existing smb.conf
            :make_backup:       Makes backup of smb.conf
            :restore_backup:    Restores backup from smb.conf.bak
            :add_user:          Adds new user to smb.conf
            :delete_user:       Deletes a user from smb.conf

    """

    path = '/etc/samba/smb.conf'

    def __init__(self):
        """Checks integrity and performs a backup of current smb.conf in
        advance of further actions."""

        self.check_integrity()
        self.make_backup()

    def check_integrity(self):
        """Checks integrity after transaction."""

        try:
            a = testparm.run()
        except Exception as e:
            raise e
            self.restore_backup()
            sys.exit(0)
        if not a[0] == 0:
            sys.exit('Unfortunately, smb.conf is corrupt. Run "testparm" to '
                     'check validity or inspect file manually.')
            self.restore_backup()
        else:
            click.secho('The smb.conf is working properly.', fg='green')

    def make_backup(self):
        """Creates a backup of `smb.conf` named `smb.conf.bak`"""

        try:
            print('Make backup of current smb.conf.')
            cp.run((self.path, self.path + '.bak'))
        except Exception as e:
            raise e
            sys.exit(0)
        else:
            click.secho(
                'A backup of smb.conf was successfully created.', fg='green')

    def restore_backup(self):
        """Restores the current backup of the `smb.conf` named
        `smb.conf.bak`"""

        try:
            mv.run((self.path + '.bak', self.path))
        except Exception:
            click.secho(
                'Something went wrong during restoring. Upps.', fg='red')
            sys.exit(0)
        else:
            click.secho('The backup of smb.conf was successfully restored.',
                        fg='green')

    def add_user(self, dict_user):
        """Adds a user entry at the end of smb.conf"""

        try:
            with open('/etc/samba/smb.conf', 'a') as file:
                file.write('\n[{user_name}]\n'.format(**dict_user))
                file.write('\tpath = /home/{user_name}/\n'.format(**dict_user))
                file.write('\tvalid users = {user_name}\n'.format(**dict_user))
                file.write('\tread only = no\n')
        except Exception as e:
            raise e
            self.restore_backup()
            sys.exit(0)
        else:
            self.check_integrity()
            click.secho(
                'The user was successfully added to smb.conf.', fg='green')

    def delete_user(self, user_name):
        """Deletes a user entry from smb.conf"""

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
        mv.run((self.path + '_temp', self.path))
        click.secho('User was successfully removed from smb.conf.', fg='green')
