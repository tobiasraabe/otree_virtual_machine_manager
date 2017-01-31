# -*- coding: utf-8 -*-
# !/usr/bin/env python

"""This module comprises input functions for user information.

    The function are::

        :_get_user_tel: Asks for telephone number and filters digits
        :_get_user_email: Asks for email and checks for valid pattern
        :_get_user_name: Asks for user name and checks for valid pattern
        :_get_full_name: Asks for full name, no check
        :_get_user_info: Calls all other functions and returns dict of answers

"""

import re


def _get_user_tel():
    """This function asks for the telephone number of the user and checks the
    input via regular expression.

    """

    while True:
        try:
            user_tel_raw = input('Enter a telephone number -> ')
        except ValueError:
            print('Make a valid input!')
            continue
        telephone = ''.join(filter(str.isdigit, user_tel_raw))
        break

    return telephone


def _get_user_email():
    """This function asks for the email address of the user and checks the
    input via regular expression.

    """

    while True:
        try:
            email = input('Enter an email address -> ')
        except ValueError:
            print('Make a valid input!')
            continue
        if re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                    email):
            break
        else:
            print('Enter a valid email address!')
            continue

    return email


def _get_user_name():
    """This function asks for the user name and checks the input via a
    regular expression.

    """

    while True:
        try:
            user_name = input('Enter a short user name -> ')
        except ValueError:
            print('Make a valid input!')
            continue
        if re.match(r'[a-z0-9_-]*', user_name):
            break
        else:
            print('Enter a valid user name which consists of lower case '
                  'letters, hyphens and underscores')
            continue

    return user_name


def _get_user_full_name():
    full_name = input("Enter user's full name -> ")
    return full_name


def get_user_info():
    """Calls function which ask for user information and returns output as a
    dict.

    """

    dict_user = {}
    dict_user['full_name'] = _get_user_full_name()
    dict_user['user_name'] = _get_user_name()
    dict_user['email'] = _get_user_email()
    dict_user['telephone'] = _get_user_tel()

    return dict_user


def get_backup_choice():
    """This function asks whether the user would like to have a database
    backup.

    """

    while True:
        try:
            answer = input('Do you want a database backup? (Y/n) -> ')
        except ValueError:
            print('Make a valid input!')
            continue
        if answer in ['y', 'Y']:
            return True
        elif answer in ['n', 'N']:
            return False
        else:
            print('Your answer is invalid. Answer with y/n!')
            continue
