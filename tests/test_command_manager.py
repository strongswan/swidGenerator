import unittest

from swid_generator.command_manager import *


class CommandManagerTests(unittest.TestCase):

    def test_run_command_check_output(self):
        output = CommandManager.run_command_check_output(['echo', 'test'])
        assert output == "test\n"

    def test_run_command_popen(self):
        return_pipe = CommandManager.run_command_popen(['echo', 'test'])
        assert isinstance(return_pipe, subprocess.Popen)
