# -*- coding: utf-8 -*-

from ..handlers.postgres import PostgreSQLDatabaseHandler


def list_user():
    """This command queries user names from the user database and echoes them
    to shell.

    """

    print('\n{:-^60}'.format(' Process: List Users '))
    postgres = PostgreSQLDatabaseHandler()
    postgres.list_user()
    print('{:-^60}\n'.format(' Process: End '))
