"""Command-line interface."""
import click

from . import __version__
from rebar_modelling.dxf_utils import DXFModel


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--axis",
    "-a",
    required=True,
    type=click.Choice(
        ["x", "y"],
        case_sensitive=False,
    ),
)
@click.version_option(version=__version__)
def main(filename, axis) -> None:
    """Rebar Modelling."""
    msp = DXFModel(filename=filename, axis=axis)
    minimal_length = DXFModel.minimal_rebar_length(msp)
    actual_length = DXFModel.rebar_length(msp, minimal_length)
    # print(minimal_length, actual_length)
    minimal_width = DXFModel.minimal_zone_width(msp)
    zone_width = DXFModel.zone_width(msp, minimal_width)
    # print(minimal_width, zone_width)
    reinforcement_zone = DXFModel.reinforcement_zone_coordinates(
        msp, actual_length, zone_width
    )
    click.echo(reinforcement_zone)


if __name__ == "__main__":
    main(prog_name="rebar-modelling")  # pragma: no cover
