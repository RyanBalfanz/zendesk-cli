"""
Provides a command-line interface to retrieve articles from a Zendesk Help Center.
"""

import abc
import argparse
import csv
import functools
import json
import os
import sys
import typing
from dataclasses import asdict, dataclass

from zendesk_cli.cmd.codes import ExitCode
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


# pylint: disable-next=too-few-public-methods
class OutputWriter(abc.ABC):
    """
    An abstract base class for output writers.
    """

    @abc.abstractmethod
    # pylint: disable-next=missing-function-docstring
    def write(
        self,
        fp: typing.IO[str],
        articles: list[Article],
        fieldnames: typing.Collection[str],
    ): ...


# pylint: disable-next=too-few-public-methods
class TSVOutputWriter(OutputWriter):
    """
    An output writer described by the usual properties of Excel-generated TAB-delimited files.
    """

    def write(
        self,
        fp: typing.IO[str],
        articles: list[Article],
        fieldnames: typing.Collection[str],
    ):
        """Writes articles to a file-like object."""
        writer = csv.DictWriter(fp, fieldnames, dialect=csv.excel_tab)
        writer.writeheader()
        for a in articles:
            writer.writerow(
                {k: v for k, v in asdict(a).items() if k in writer.fieldnames}
            )


# pylint: disable-next=too-few-public-methods
class JSONLOutputWriter(OutputWriter):
    """
    An output writer that uses JSON Lines text file format (newline-delimited JSON).
    """

    def write(
        self,
        fp: typing.IO[str],
        articles: list[Article],
        fieldnames: typing.Collection[str],
    ):
        """Writes articles to a file-like object."""
        for a in articles:
            json.dump({k: v for k, v in asdict(a).items() if k in fieldnames}, fp)
            fp.write("\n")


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

    if n.format == "tsv":
        w = TSVOutputWriter()
    elif n.format == "jsonl":
        w = JSONLOutputWriter()
    else:
        raise ValueError(f"Unknown format: {n.format}")
    articles = (
        Article(**{k: v for k, v in a.items() if k in Article.get_field_names()})
        for a in HelpCenterClient(n.url).get_articles()
    )
    w.write(sys.stdout, list(articles), fieldnames)

    return ExitCode.OK


if __name__ == "__main__":
    raise SystemExit(main())
