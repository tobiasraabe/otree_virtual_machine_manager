"""Test the cli."""

from click.testing import CliRunner

from ovmm import cli


def test_command_line_interface():
    """Check whether the cli can be reached and the help string is shown."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Usage: main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
