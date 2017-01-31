#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompts_defaults
---------------------

"""


from ovmm.prompts import defaults


def test_get_dummy_user():
    dummy_user = defaults.get_dummy_user()
    user_name = dummy_user['user_name']
    for key in dummy_user.keys():
        assert dummy_user[key] == defaults.dummy_users[user_name][key]
