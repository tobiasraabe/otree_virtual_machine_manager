"""This file contains default values for prompts.

Example
-------
For :dict:`dummy_users` the template looks like this:

``
name = {
    'user_full': 'forename surname',
    'user_name': 'forename',
    'user_email': 'forenamesurname@posteo.de',
    'user_tel': '04387-238742'
}
``

But pull requests to add a new dummy are only accepted if you recognize the
pattern and cite the famous source.

"""

import random


dummy_users = {

    'werner': {
        'user_full': 'Werner Heisenberg',
        'user_name': 'werner',
        'user_email': 'wernerheisenberg@web.de',
        'user_tel': '0049-931-05121901'
    },

    'max': {
        'user_full': 'Max Born',
        'user_name': 'max',
        'user_email': 'maxborn@t-online.de',
        'user_tel': '0048-71-11121882'
    },

    'louis': {
        'user_full': 'Louis Slotin',
        'user_name': 'louis',
        'user_email': 'louisslotin@aol.com',
        'user_tel': '001-204-01121901'
    },

    'samuel': {
        'user_full': 'Samuel Goudsmit',
        'user_name': 'samuel',
        'user_email': 'samuelgoudsmit@hotmail.com',
        'user_tel': '0031-70-11071902'
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
