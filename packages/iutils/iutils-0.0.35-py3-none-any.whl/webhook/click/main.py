from ..sites import CircleCI
from iutils.utils import remove_last_n_chars
import click
import sys


@click.command()
@click.option(
    "-n",
    "n_characters_to_remove",
    default=1,
    show_default=True,
    help="The last n characters to remove.",
)
def main(*args, **kwargs):
    """Read from STDIN and then calculate a CircleCI webhook signatures of the read content."""
    data = sys.stdin.read()
    data = remove_last_n_chars(data, kwargs["n_characters_to_remove"])

    circleci = CircleCI()
    circleci.print_signature(bytes(data, "utf-8"))
