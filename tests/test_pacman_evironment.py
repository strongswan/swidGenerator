# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import unittest

from swid_generator.command_manager import CommandManager
from tests.fixtures.command_manager_mock import CommandManagerMock
from swid_generator.environments.pacman_environment import PacmanEnvironment
from swid_generator.package_info import PackageInfo, FileInfo
from swid_generator.environments.common import CommonEnvironment
from mock import patch


class DpkgEnvironmentTests(unittest.TestCase):
    def setUp(self):

        self.command_manager_run_check_output_patch = patch.object(CommandManager, 'run_command_check_output')
        self.command_manager_run_command_patch = patch.object(CommandManager, 'run_command')
        self.common_environment_is_file_patch = patch.object(CommonEnvironment, '_is_file')
        self.os_path_getsize_patch = patch.object(os.path, 'getsize')

        self.command_manager_run_check_output_mock = self.command_manager_run_check_output_patch.start()
        self.common_environment_is_file_mock = self.common_environment_is_file_patch.start()
        self.os_path_getsize_mock = self.os_path_getsize_patch.start()
        self.command_manager_run_command_mock = self.command_manager_run_command_patch.start()

        self.command_manager_run_check_output_mock.side_effect = CommandManagerMock.run_command_check_output
        self.command_manager_run_command_mock.side_effect = CommandManagerMock.run_command
        self.common_environment_is_file_mock.return_value = True
        self.os_path_getsize_mock.return_value = 1

        self.pacman_environment = PacmanEnvironment()

    def tearDown(self):
        self.command_manager_run_check_output_patch.stop()
        self.command_manager_run_command_patch.stop()
        self.common_environment_is_file_patch.stop()
        self.os_path_getsize_patch.stop()

    def test_get_package_list(self):
        result_list = self.pacman_environment.get_package_list()

        expected_package_list = list()

        expected_package_list.append(PackageInfo(package="acl", version="2.2.52-3"))
        expected_package_list.append(PackageInfo(package="arch-install-scripts", version="17-1"))
        expected_package_list.append(PackageInfo(package="archlinux-keyring", version="20170320-1"))

        for index, result_package in enumerate(result_list):
            print(result_package.package)
            print(result_package.version)
            assert result_package.package == expected_package_list[index].package
            assert result_package.version == expected_package_list[index].version

    def test_get_files_for_package(self):
        package_info = PackageInfo(package="docker")
        result_list = self.pacman_environment.get_files_for_package(package_info)

        expected_file_list = list()

        expected_file_list.append(FileInfo("/usr/bin/docker"))
        expected_file_list.append(FileInfo("/usr/bin/docker-containerd"))
        expected_file_list.append(FileInfo("/usr/bin/docker-containerd-ctr"))
        expected_file_list.append(FileInfo("/usr/bin/docker-containerd-shim"))
        expected_file_list.append(FileInfo("/etc/docker.ini"))

        for index, result_file in enumerate(result_list):
            assert result_file.name == expected_file_list[index].name
            assert result_file.location == expected_file_list[index].location
            if index >= 4:  # These are configuration-files
                assert result_file.mutable is True
            assert result_file.location == expected_file_list[index].location
            assert result_file.full_pathname == expected_file_list[index].full_pathname

    def test_get_packageinfo_from_packagefile(self):
        result_package = self.pacman_environment.get_packageinfo_from_packagefile("/tmp/docker.pkg")

        print(result_package.package)

        assert result_package.package == 'docker'
        assert result_package.version == '1:17.04.0-1'

    def test_get_files_from_packagefile(self):
        all_files = self.pacman_environment.get_files_from_packagefile("/tmp/docker.pkg")

        expected_file_list = list()

        expected_file_list.append(FileInfo("/usr/bin/docker.ini"))
        expected_file_list.append(FileInfo("/usr/bin/docker"))
        expected_file_list.append(FileInfo("/usr/bin/docker-containerd"))

        for index, result_file in enumerate(all_files):
            assert result_file.name == expected_file_list[index].name
            assert result_file.location == expected_file_list[index].location
            assert result_file.location == expected_file_list[index].location
            assert result_file.full_pathname == expected_file_list[index].full_pathname

