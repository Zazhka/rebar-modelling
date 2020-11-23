"""Command-line interface."""
import click

from rebar_modelling.dxf_utils import DXFModel


@click.command()
@click.version_option()
def main() -> None:
    """Rebar Modelling."""
    msp = DXFModel(filename="top_y.dxf")

    x_max = DXFModel.find_border_coordinate(msp, axis="x", extrema="max")
    y_max = DXFModel.find_border_coordinate(msp, axis="y", extrema="max")
    x_min = DXFModel.find_border_coordinate(msp, axis="x", extrema="min")
    y_min = DXFModel.find_border_coordinate(msp, axis="y", extrema="min")
    DXFModel.print_all_entities(msp)
    print(f"Max X: {x_max}")
    print(f"Max Y: {y_max}")
    print(f"Min X: {x_min}")
    print(f"Min Y: {y_min}")


if __name__ == "__main__":
    main(prog_name="rebar-modelling")  # pragma: no cover
