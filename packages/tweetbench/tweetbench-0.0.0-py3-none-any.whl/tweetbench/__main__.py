"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """tweetbench."""


if __name__ == "__main__":
    main(prog_name="tweetbench")  # pragma: no cover
