#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_otree_virtual_machine_manager
----------------------------------

Tests for ``ovmm`` module.

"""

from click.testing import CliRunner

from ovmm import cli


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Usage: main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
