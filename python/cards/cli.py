"""Command Line Interface."""

import argparse
import typing

from rich import print

#

def setup(argv: typing.Sequence[str] | None = None) -> int:
    """CLI main."""
    parser = argparse.ArgumentParser()
    # parser.add_argument("name", required=False)
    args = parser.parse_args(argv)
    print(args)
    return 0




