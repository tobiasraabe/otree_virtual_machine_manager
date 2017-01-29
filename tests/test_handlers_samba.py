#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_handlers_samba
-------------------

"""

import pytest

from ovmm.handlers import samba
from ovmm.prompts.defaults import dummy_users


@pytest.fixture(autouse=True)
def patching(monkeypatch, tmpdir):
    monkeypatch.setattr(
        samba.SambaConfigHandler, 'path', str(tmpdir.join('smb.conf'))
    )
    monkeypatch.setattr(
        samba.SambaConfigHandler, 'check_integrity', lambda x: 1
    )
    monkeypatch.setattr(
        samba.SambaConfigHandler, 'make_backup', lambda x: 1
    )
    monkeypatch.setattr(
        samba.SambaConfigHandler, 'restore_backup', lambda x: 1
    )


def test_add_user(tmpdir):
    # with open(tmpdir.join('smb.conf'), 'w') as file:
    #     file.write('')
    dummy_user_1 = dummy_users['werner']

    smb = samba.SambaConfigHandler()
    smb.add_user(dummy_user_1)

    with open(str(tmpdir.join('smb.conf'))) as file:
        text = file.read()

    statement = (
        '\n[werner]\n\tpath = /home/werner/\n\tvalid users = werner\n'
        '\tread only = no\n')
    assert statement == text
