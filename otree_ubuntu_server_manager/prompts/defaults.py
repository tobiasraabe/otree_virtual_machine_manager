"""This file contains default values for prompts

For ``add_user_defaults`` the template looks like this:

``
name = {
    'user_full': 'forename surname',
    'user_name': 'forename',
    'user_email': 'forenamesurname@posteo.de',
    'user_tel': '04387-238742'
}

"""

import random

add_user_defaults = {

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


def get_add_default():
    key = random.choice(list(add_user_defaults.keys()))
    return add_user_defaults[key]
