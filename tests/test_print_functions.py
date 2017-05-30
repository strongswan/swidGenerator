# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import unittest
from tests.fixtures.command_manager_mock import CommandManagerMock
from swid_generator.command_manager import CommandManager
from mock import patch

from swid_generator.print_functions import *


class PrintFunctionsTest(unittest.TestCase):

    def setUp(self):
        self.command_manager_run_command_patch = patch.object(CommandManager, 'run_command_check_output')
        self.command_manager_run_command_mock = self.command_manager_run_command_patch.start()

        self.command_manager_run_command_mock.side_effect = CommandManagerMock.run_command_check_output

    def tearDown(self):
        self.command_manager_run_command_patch.stop()

    def test_sing_xml(self):
        print("test_sing_xml")

        signature_args = {
            'pkcs12_file': "cert.pfx",
            'pkcs12_password': "123"
        }

        result = sign_xml("", signature_args)
        print(result)
        assert result is not None
