"""Tests for DXF utils."""
from rebar_modelling.dxf_utils import DXFModel


def test_invalid_file_name() -> None:
    """Invalid filename provided to DXFModel class."""
    DXFModel(filename="invalid_name.dxf", axis="x")
    assert "FileNotFoundError"
