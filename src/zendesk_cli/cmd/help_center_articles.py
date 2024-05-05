"""
Provides a command-line interface to retrieve articles from a Zendesk Help Center.
"""

import argparse
import contextlib
import csv
import sys
import typing
from dataclasses import asdict, dataclass

from zendesk_cli.cmd.codes import ExitCode
from zendesk_cli.internal.help_center.api import HelpCenterClient
from zendesk_cli.internal.help_center.models import Article


@contextlib.contextmanager
def dummy_context(w: typing.IO[str]):
    """
    A dummy context manager that yields the given file-like object.
    """
    yield w


def get_articles_for_url(url: str) -> list[Article]:
    """
    Returns a list of articles from the given Help Center URL.
    """
    c = HelpCenterClient(url)
    return list(Article(**a) for a in c.get_articles())


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

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Help Center URL")

    n = N()
    _ = parser.parse_args(argv, namespace=n)

    articles = get_articles_for_url(n.url)

    fieldnames = ["id", "title"]
    with dummy_context(sys.stderr) as buf:
        writer = csv.DictWriter(
            buf,
            fieldnames=fieldnames,
            dialect=csv.excel_tab,
            quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writeheader()
        for a in articles:
            writer.writerow(
                {k: v for k, v in asdict(a).items() if k in writer.fieldnames}
            )

    all_fieldnames = Article.get_field_names()
    with contextlib.closing(sys.stdout) as buf:
        writer = csv.DictWriter(
            buf,
            fieldnames=all_fieldnames,
            dialect=csv.excel_tab,
            quoting=csv.QUOTE_ALL,
            quotechar="`",
        )
        writer.writeheader()
        for a in articles:
            writer.writerow(
                {k: v for k, v in asdict(a).items() if k in writer.fieldnames}
            )

    return ExitCode.OK


if __name__ == "__main__":
    raise SystemExit(main())
