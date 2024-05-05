import argparse
import typing

from zendesk_cli.cmd.codes import ExitCode


def main(argv: typing.Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    _ = parser.parse_args(argv)
    return ExitCode.Ok


if __name__ == "__main__":
    raise SystemExit(main())
