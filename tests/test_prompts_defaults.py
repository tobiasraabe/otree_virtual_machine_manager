#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompts_defaults
---------------------

"""


from ovmm.prompts import defaults


def test_get_dummy_user():
    dummy_user = defaults.get_dummy_user()
    assert dummy_user['user_name'] in defaults.dummy_users
