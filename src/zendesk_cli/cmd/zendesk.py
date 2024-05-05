"""
Provides a command-line interface to the Zendesk API.
"""

import argparse
import typing

from zendesk_cli.cmd.codes import ExitCode


def main(argv: typing.Sequence[str] | None = None) -> int:
    """
    The entry point for the command-line interface.
    """
    parser = argparse.ArgumentParser()
    _ = parser.parse_args(argv)
    return ExitCode.OK


if __name__ == "__main__":
    raise SystemExit(main())
