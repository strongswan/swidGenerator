
import sys
from swid_generator.command_manager import *

if sys.version_info < (2, 7):
    # We need the skip decorators from unittest2 on Python 2.6.
    import unittest2 as unittest
else:
    import unittest


class CommandManagerTests(unittest.TestCase):

    def test_run_command_check_output(self):
        output = CommandManager.run_command_check_output(['echo', 'test'])
        assert output == "test\n"

    def test_run_command_popen(self):
        return_pipe = CommandManager.run_command_popen(['echo', 'test'])
        assert isinstance(return_pipe, subprocess.Popen)
