"""Tests for DXF utils."""
from click.testing import CliRunner

from rebar_modelling.dxf_utils import DXFModel


def test_invalid_file_name(runner: CliRunner) -> None:
    """Invalid filename provided to DXFModel class."""
    DXFModel(filename="invalid_name.dxf", axis="x")
    assert "FileNotFoundError"
