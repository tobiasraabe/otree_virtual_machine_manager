#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This script makes a database backup for a specific user. The
following steps are executed:

    - [X] Create directory in otree-admin
    - [X] Output database in ``user_db_backups/``

"""

import os
import time

from plumbum import local
from plumbum.cmd import pg_dump
from plumbum.cmd import su
from plumbum.cmd import sudo
from prompt.user_prompt import _get_user_name as get_user_name


zipper = local['7z']

ADMIN_DIRECTORY = 'user_db_backups/'


def backup_user():
    """For a given user name, the function backups the user's database to a
    folder in the administrator's directory."""

    print('{:-^60}\n'.format(' Process: back_user '))

    user_name = get_user_name()

    if not os.path.exists(ADMIN_DIRECTORY):
        os.makedirs(ADMIN_DIRECTORY)

    timestr = time.strftime('%Y-%m-%d_%H-%M-%S')
    (sudo[su['-', 'postgres', '-c', pg_dump[user_name]]] >
     'user_db_backups/' + user_name + '_db_dump_' + timestr + '.sql')()

    print("A backup of user's database was successfully created")
    print('{:-^60}\n'.format(' Process: End '))
