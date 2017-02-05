# -*- coding: utf-8 -*-
"""This file contains default values for prompts.

Example
-------
For :dict:`dummy_users` the template looks like this:

``
name = {
    'full_name': 'forename surname',
    'user_name': 'forename',
    'email': 'forenamesurname@posteo.de',
    'telephone': '04387-238742'
}
``

But pull requests to add a new dummy are only accepted if you recognize the
pattern and cite the famous source.

"""

import random


dummy_users = {

    'werner': {
        'full_name': 'Werner Heisenberg',
        'user_name': 'werner',
        'email': 'wernerheisenberg@web.de',
        'telephone': '0049-931-05121901'
    },

    'max': {
        'full_name': 'Max Born',
        'user_name': 'max',
        'email': 'maxborn@t-online.de',
        'telephone': '0048-71-11121882'
    },

    'louis': {
        'full_name': 'Louis Slotin',
        'user_name': 'louis',
        'email': 'louisslotin@aol.com',
        'telephone': '001-204-01121901'
    },

    'samuel': {
        'full_name': 'Samuel Goudsmit',
        'user_name': 'samuel',
        'email': 'samuelgoudsmit@hotmail.com',
        'telephone': '0031-70-11071902'
    },
}


def get_dummy_user() -> dict:
    """Returns one of the dummy user in :dict:`dummy_users`.

    Returns
    -------
    dummy_users[key] : dict
        A dictionary of a dummy user

    """
    key = random.choice(list(dummy_users.keys()))
    return dummy_users[key]
