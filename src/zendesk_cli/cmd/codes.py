"""
Codes for the exit status of the program.
"""

import enum


class ExitCode(enum.IntEnum):
    """
    >>> ExitCode.OK == 0
    True
    >>> ExitCode.ERROR == 1
    True
    """

    OK = 0
    ERROR = 1
