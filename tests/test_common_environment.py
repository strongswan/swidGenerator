# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals


import unittest
import platform
import os
import shutil

from mock import patch
from swid_generator.environments.common import CommonEnvironment
from nose_parameterized import parameterized


class CommonEnvironmentTests(unittest.TestCase):

    def setUp(self):
        self.platform_dist_patch = patch.object(platform, 'dist')
        self.platform_system_patch = patch.object(platform, 'system')
        self.platform_os_name_patch = patch.object(platform.os, 'name')

        self.platform_dis_mock = self.platform_dist_patch.start()
        self.platform_system_mock = self.platform_system_patch.start()
        self.platform_os_name_mock = self.platform_os_name_patch.start()
        self._collect_garbage()

    def tearDown(self):
        self.platform_dist_patch.stop()
        self.platform_system_patch.stop()
        self.platform_os_name_patch.stop()
        self._collect_garbage()

    @parameterized.expand([
        [('debian', '7.4', ''), 'Linux', 'posix', 'debian_7.4'],
        [('fedora', '19', 'Schrödinger\'s Cat'), 'Linux', 'posix', 'fedora_19'],
        [('arch', '', ''), 'Linux', 'posix', 'arch'],
        [('', '', ''), 'Linux', 'posix', 'linux'],
        # [('', '', ''), "", 'posix', 'posix'],
        # [('', '', ''), "", "", 'unknown']
    ])
    def test_os_string(self, dist, system, os_name, expected_output):
        self.platform_dis_mock.return_value = dist
        self.platform_system_mock.return_value = system
        self.platform_os_name_mock.return_value = os_name
        os_string = CommonEnvironment.get_os_string()
        assert os_string == expected_output

    @staticmethod
    def test_is_file():
        isfile = CommonEnvironment._is_file

        def _create_folder(file_path):
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            return file_path

        _create_folder("/tmp/sub")
        assert isfile(str("/tmp/sub")) is False, 'A directory is not a file.'

        assert isfile(str("/tmp/sub1")) is False, 'A nonexistant directory is not a file.'

        open("/tmp/sub/file.txt", 'a').close()
        assert isfile(str("/tmp/sub/file.txt")) is True, 'Real file not recognized.'

        assert isfile(str("/tmp/sub/file3.txt")) is False, 'A nonexistant file is not a file.'

        os.symlink("/tmp/sub/file.txt", "/tmp/sub/file_sym.txt")
        assert isfile(str("/tmp/sub/file.txt")) is True, 'A symlink is a file like object.'

    @staticmethod
    def _collect_garbage():
        if os.path.exists("/tmp/sub"):
            shutil.rmtree('/tmp/sub')

