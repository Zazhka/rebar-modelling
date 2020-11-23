"""Command-line interface."""
import click

from rebar_modelling.dxf_utils import DXFModel


@click.command()
@click.version_option()
def main() -> None:
    """Rebar Modelling."""
    msp = DXFModel(filename="top_y.dxf", axis="x")
    minimal_length = DXFModel.minimal_rebar_length(msp)
    actual_length = DXFModel.rebar_length(msp, minimal_length)
    print(minimal_length, actual_length)
    minimal_width = DXFModel.minimal_zone_width(msp)
    zone_width = DXFModel.zone_width(msp, minimal_width)
    print(minimal_width, zone_width)
    reinforcemen_zone = DXFModel.reinforcement_zone_coordinates(
        msp, actual_length, zone_width
    )
    print(reinforcemen_zone)


if __name__ == "__main__":
    main(prog_name="rebar-modelling")  # pragma: no cover
