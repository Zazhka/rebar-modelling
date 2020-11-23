"""Command-line interface."""
import click

from rebar_modelling.dxf_utils import DXFModel


@click.command()
@click.version_option()
def main() -> None:
    """Rebar Modelling."""
    msp = DXFModel(filename="top_y.dxf")
    minimal_length = DXFModel.minimal_rebar_length(msp, axis="y")
    actual_length = DXFModel.rebar_length(msp, minimal_length)
    print(minimal_length, actual_length)


if __name__ == "__main__":
    main(prog_name="rebar-modelling")  # pragma: no cover
