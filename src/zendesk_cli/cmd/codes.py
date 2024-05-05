import enum


class ExitCode(enum.IntEnum):
    """
    >>> ExitCode.Ok == 0
    True
    >>> ExitCode.Error == 1
    True
    """

    Ok = 0
    Error = 1
