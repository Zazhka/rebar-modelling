"""Test cases for the __main__ module."""
from click.testing import CliRunner

from rebar_modelling import __main__


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main, ["top_y.dxf", "--axis=x"])
    assert result.exit_code == 0


def test_main_fails_without_filename(runner: CliRunner) -> None:
    """It exits with a status code of two."""
    result = runner.invoke(__main__.main, ["--axis=x"])
    assert result.exit_code == 2


def test_main_fails_without_axis(runner: CliRunner) -> None:
    """It exits with a status code of two."""
    result = runner.invoke(__main__.main, ["top_y.dxf"])
    assert result.exit_code == 2


def test_main_fails_with_invalid_axis(runner: CliRunner) -> None:
    """It exits with a status code of two."""
    result = runner.invoke(__main__.main, ["top_y.dxf", "--axis=test"])
    assert result.exit_code == 2


def test_main_fails_with_invalid_filename(runner: CliRunner) -> None:
    """It exits with a status code of two."""
    result = runner.invoke(__main__.main, ["invalid_filename", "--axis=y"])
    assert result.exit_code == 2


def test_main_fails_with_invalid_filetype(runner: CliRunner) -> None:
    """It exits with a status code of one."""
    result = runner.invoke(__main__.main, ["license.rst", "--axis=y"])
    assert result.exit_code == 1
