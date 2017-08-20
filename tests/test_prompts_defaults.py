#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompts_defaults
---------------------

"""


from ovmm.prompts import defaults

from ovmm.prompts.validators import validate_user_name
from ovmm.prompts.validators import validate_email
from ovmm.prompts.validators import validate_telephone


def test_get_dummy_user():
    dummy_user = defaults.get_dummy_user()
    user_name = dummy_user['user_name']
    for key in dummy_user.keys():
        assert dummy_user[key] == defaults.dummy_users[user_name][key]


def test_validate_dummy_users():
    dummy_users = defaults.dummy_users
    for key in dummy_users.keys():
        assert dummy_users[key]['user_name'] == validate_user_name(
            dummy_users[key]['user_name'])
        assert dummy_users[key]['email'] == validate_email(
            dummy_users[key]['email'])
        assert dummy_users[key]['telephone'] == validate_telephone(
            dummy_users[key]['telephone'])
