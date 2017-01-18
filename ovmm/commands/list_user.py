# -*- coding: utf-8 -*-

"""This script executes the function `list_user()` of
`PostgreSQLDatabaseHandler` in `postgres.py`. The user names of all accounts
are displayed.

"""

from ..handlers.postgres import PostgreSQLDatabaseHandler


def list_user():
    """This command queries user names from the user database and echoes them
    to shell.

    """

    print('\n{:-^60}'.format(' Process: List Users '))
    postgres = PostgreSQLDatabaseHandler()
    postgres.list_user()
    print('{:-^60}\n'.format(' Process: End '))
