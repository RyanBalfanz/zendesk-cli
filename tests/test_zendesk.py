"""
Test the zendesk command.
"""

import contextlib
import io
from unittest import TestCase

from zendesk_cli.cmd.zendesk import main


class TestZendeskCommand(TestCase):
    """
    Test the zendesk command.
    """

    def test_basic(self):
        """
        Test the zendesk command basic behavior.
        """
        with contextlib.redirect_stdout(io.StringIO()) as f:
            r = main()
            self.assertEqual(r, 0)
            self.assertEqual(f.getvalue(), "")
