"""
Provides a command-line interface to retrieve articles from a Zendesk Help Center.
"""

import argparse
import functools
import os
import sys
import typing
from dataclasses import dataclass

from zendesk_cli.cmd.codes import ExitCode
from zendesk_cli.cmd.writers import JSONLOutputWriter, TSVOutputWriter
from zendesk_cli.internal.help_center.api import HelpCenterClient
from zendesk_cli.internal.help_center.models import Article


# pylint: disable-next=invalid-name
def handle_broken_pipe_error[R, **P](f: typing.Callable[P, R]):
    """
    A decorator that handles a BrokenPipeError (e.g. piping to head can cause a SIGPIPE signal).
    See: https://docs.python.org/3/library/signal.html#note-on-sigpipe
    """

    @functools.wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        try:
            f(*args, **kwargs)
        except BrokenPipeError:
            # pylint: disable-next=line-too-long
            # Python flushes standard streams on exit; redirect remaining output to devnull to avoid another BrokenPipeError at shutdown.
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
            sys.exit(ExitCode.ERROR)  # Python exits with error code 1 on EPIPE.

    return wrapper


@handle_broken_pipe_error
def main(argv: typing.Sequence[str] | None = None) -> int:
    """
    The entry point for the command-line interface.
    """

    @dataclass
    class N:
        """
        The namespace for the command-line interface arguments.
        """

        url: str = ""
        format: typing.Literal["tsv", "jsonl"] = "tsv"
        include_fields: list[str] | None = None
        exclude_fields: list[str] | None = None

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Help Center URL")
    parser.add_argument(
        "--format", help="Output format", choices=["tsv", "jsonl"], default="tsv"
    )
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--include-fields", help="Include fields in output", nargs="+")
    g.add_argument("--exclude-fields", help="Exclude fields from output", nargs="+")

    n = N()
    _ = parser.parse_args(argv, namespace=n)

    fieldnames: typing.Collection[str] = []
    if n.include_fields:
        fieldnames = n.include_fields
    elif n.exclude_fields:
        fieldnames = [f for f in Article.get_field_names() if f not in n.exclude_fields]
    else:
        fieldnames = Article.get_field_names()

    match n.format:
        case "tsv":
            w = TSVOutputWriter()
        case "jsonl":
            w = JSONLOutputWriter()
        case _:
            raise ValueError(f"Unknown format: {n.format}")
    articles = (
        Article(**{k: v for k, v in a.items() if k in Article.get_field_names()})
        for a in HelpCenterClient(n.url).get_articles()
    )
    w.write(sys.stdout, list(articles), fieldnames)

    return ExitCode.OK


if __name__ == "__main__":
    raise SystemExit(main())
