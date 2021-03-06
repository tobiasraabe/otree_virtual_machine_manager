"""This module contains all tests related to prompt parsers."""

import os

import click
import pytest

from ovmm.prompts import parsers

PASSWORD_LENGTH = os.environ.get('OVMM_PASSWORD_LENGTH')


@pytest.mark.parametrize('parse_func,inp', [
    (getattr(parsers, 'parse_user_name'), 'usern'),
    (getattr(parsers, 'parse_user_name'), '_username'),
    (getattr(parsers, 'parse_user_name'), '1username'),
    (getattr(parsers, 'parse_user_name'), 'UserName'),
    (getattr(parsers, 'parse_user_name'), 'us-ername'),
    (getattr(parsers, 'parse_user_name'), 'user name'),
    (getattr(parsers, 'parse_password'), '1234567'),
    (getattr(parsers, 'parse_password'), '1234567%'),
    (getattr(parsers, 'parse_password'), 'AbCdEf G'),
    (getattr(parsers, 'parse_password'), 'password'),
    (getattr(parsers, 'parse_lower_alpha'), 'abcde'),
    (getattr(parsers, 'parse_lower_alpha'), 'abcdeF'),
    (getattr(parsers, 'parse_lower_alpha'), 'abcde1'),
    (getattr(parsers, 'parse_host'), 'a234'),
    (getattr(parsers, 'parse_host'), '0234'),
    (getattr(parsers, 'parse_host'), 'localhos'),
    (getattr(parsers, 'parse_host'), '12345'),
    (getattr(parsers, 'parse_port'), 'a234'),
    (getattr(parsers, 'parse_port'), '12345'),
    (getattr(parsers, 'parse_table_name'), 'usert'),
    (getattr(parsers, 'parse_table_name'), '_usertable'),
    (getattr(parsers, 'parse_table_name'), 'User_table'),
    (getattr(parsers, 'parse_table_name'), 'user-table'),
])
def test_parser_error(parse_func, inp):
    """Test whether inputs raise errors in parsers."""
    with pytest.raises(click.BadParameter):
        parse_func(inp)


@pytest.mark.parametrize('parse_func,inp', [
    (getattr(parsers, 'parse_user_name'), 'username'),
    (getattr(parsers, 'parse_user_name'), 'user_name'),
    (getattr(parsers, 'parse_user_name'), 'user_1'),
    (getattr(parsers, 'parse_password'), 'username'),
    (getattr(parsers, 'parse_password'), 'user1234'),
    (getattr(parsers, 'parse_password'), 'UserName1'),
    (getattr(parsers, 'parse_lower_alpha'), 'userna'),
    (getattr(parsers, 'parse_host'), 'localhost'),
    (getattr(parsers, 'parse_host'), '1'),
    (getattr(parsers, 'parse_host'), '12'),
    (getattr(parsers, 'parse_host'), '123'),
    (getattr(parsers, 'parse_port'), '1324'),
    (getattr(parsers, 'parse_table_name'), 'user_table'),
])
def test_parser_check(parse_func, inp):
    """Test whether parsers raise no error."""
    assert parse_func(inp) == inp
