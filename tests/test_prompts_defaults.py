"""This module contains all tests related to prompts."""

from ovmm.prompts import defaults

from ovmm.prompts.validators import validate_user_name
from ovmm.prompts.validators import validate_email
from ovmm.prompts.validators import validate_telephone


def test_get_dummy_user():
    """Test whether a retrieved user is equal to an imported one."""
    dummy_user = defaults.get_dummy_user()
    user_name = dummy_user['user_name']
    for key in dummy_user.keys():
        assert dummy_user[key] == defaults.DUMMY_USERS[user_name][key]


def test_validate_dummy_users():
    """Test whether the validation works as expected."""
    dummy_users = defaults.DUMMY_USERS
    for key in dummy_users.keys():
        assert dummy_users[key]['user_name'] == validate_user_name(
            ctx=None, param=None, value=dummy_users[key]['user_name'])
        assert dummy_users[key]['email'] == validate_email(
            ctx=None, param=None, value=dummy_users[key]['email'])
        tel_num = ''.join(filter(str.isdigit, dummy_users[key]['telephone']))
        assert tel_num == validate_telephone(
            ctx=None, param=None, value=dummy_users[key]['telephone'])
