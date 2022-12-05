#!/usr/bin/env python3

"""Test interception of os.system calls."""

from tests import mocks
import unittest
from things_cli import thingsconnection


class CallShell(unittest.TestCase):
    """Class documentation goes here."""

    def test_main(self):
        exitcode = thingsconnection.open_todo_in_things(4711)
        self.assertEqual(exitcode, 42)


if __name__ == "__main__":
    unittest.main()
