"""Tests for ovmm.prompts.parsers

"""

import os

import click
import pytest

from ovmm.prompts import validators

PASSWORD_LENGTH = os.environ.get('OVMM_PASSWORD_LENGTH')


@pytest.mark.parametrize('parse_func,inp', [
    (getattr(validators, 'validate_user_name'), 'usern'),
    (getattr(validators, 'validate_user_name'), '_username'),
    (getattr(validators, 'validate_user_name'), '1username'),
    (getattr(validators, 'validate_user_name'), 'UserName'),
    (getattr(validators, 'validate_user_name'), 'us-ername'),
    (getattr(validators, 'validate_user_name'), 'user name'),
    (getattr(validators, 'validate_email'), 'user@name'),
    (getattr(validators, 'validate_email'), 'user@.de'),
    (getattr(validators, 'validate_email'), 'user.de'),
    (getattr(validators, 'validate_password'), '1234567'),
    (getattr(validators, 'validate_password'), '1234567%'),
    (getattr(validators, 'validate_password'), 'AbCdEf G'),
    (getattr(validators, 'validate_password'), 'password'),
])
def test_parser_error(parse_func, inp):
    with pytest.raises(click.BadParameter):
        parse_func(ctx=None, param=None, value=inp)


@pytest.mark.parametrize('parse_func,inp', [
    (getattr(validators, 'validate_user_name'), 'username'),
    (getattr(validators, 'validate_user_name'), 'user_name'),
    (getattr(validators, 'validate_user_name'), 'user_1'),
    (getattr(validators, 'validate_email'), 'user@name.de'),
    (getattr(validators, 'validate_email'), 'user@name.de.de'),
    (getattr(validators, 'validate_email'), 'user123@name.de'),
    (getattr(validators, 'validate_email'), '1user@na.me'),
    (getattr(validators, 'validate_password'), 'username'),
    (getattr(validators, 'validate_password'), 'user1234'),
    (getattr(validators, 'validate_password'), 'UserName1'),
    (getattr(validators, 'validate_telephone'), '67512635')
])
def test_parser_check(parse_func, inp):
    assert parse_func(ctx=None, param=None, value=inp) == inp
