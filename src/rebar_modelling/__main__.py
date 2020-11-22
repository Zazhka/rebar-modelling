"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Rebar Modelling."""


if __name__ == "__main__":
    main(prog_name="rebar-modelling")  # pragma: no cover
