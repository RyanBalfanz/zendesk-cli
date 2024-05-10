import abc
import csv
import json
import typing
from dataclasses import asdict

from zendesk_cli.internal.help_center.models import Article


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


class FilesWriter(OutputWriter):
    def write(
        self,
        fp: typing.IO[str],
        articles: list[Article],
        fieldnames: typing.Collection[str],
    ):
        import pathlib

        for a in articles:
            for k, v in asdict(a).items():
                if k not in fieldnames:
                    continue
                d = pathlib.Path("./articles").resolve()
                fn = (d / f"{a.title}[{a.id}].html".replace("/", ":")).absolute()
                with fn.open(mode="w") as f:
                    f.write(str(v))


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
