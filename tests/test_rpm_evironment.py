# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import unittest

from swid_generator.command_manager import CommandManager
from tests.fixtures.command_manager_mock import CommandManagerMock
from swid_generator.environments.rpm_environment import RpmEnvironment
from swid_generator.package_info import PackageInfo, FileInfo
from swid_generator.environments.common import CommonEnvironment
from mock import patch


class RpmEnvironmentTests(unittest.TestCase):

    def setUp(self):

        self.command_manager_run_check_output_patch = patch.object(CommandManager, 'run_command_check_output')
        self.command_manager_run_popen_patch = patch.object(CommandManager, 'run_command_popen')
        self.common_environment_is_file_patch = patch.object(CommonEnvironment, '_is_file')
        self.os_path_getsize_patch = patch.object(os.path, 'getsize')

        self.command_manager_run_check_output_mock = self.command_manager_run_check_output_patch.start()
        self.command_manager_run_popen_mock = self.command_manager_run_popen_patch.start()
        self.common_environment_is_file_mock = self.common_environment_is_file_patch.start()
        self.os_path_getsize_mock = self.os_path_getsize_patch.start()

        self.command_manager_run_check_output_mock.side_effect = CommandManagerMock.run_command_check_output
        self.command_manager_run_popen_mock.side_effect = CommandManagerMock.run_command_popen
        self.common_environment_is_file_mock.return_value = True
        self.os_path_getsize_mock.return_value = 1

        self.rpm_environment = RpmEnvironment()

    def tearDown(self):
        self.command_manager_run_check_output_patch.stop()
        self.common_environment_is_file_patch.stop()
        self.os_path_getsize_patch.stop()
        self.command_manager_run_popen_patch.stop()

    def test_get_package_list(self):
        result_list = self.rpm_environment.get_package_list()

        expected_package_list = list()

        expected_package_list.append(PackageInfo(package="perl-Git", version="2.9.3-3.fc25.noarch"))
        expected_package_list.append(PackageInfo(package="fedora-repos", version="25-3.noarch"))
        expected_package_list.append(PackageInfo(package="perl-IO-Socket-SSL", version="2.038-1.fc25.noarch"))
        expected_package_list.append(PackageInfo(package="setup", version="2.10.4-1.fc25.noarch"))

        for index, result_package in enumerate(result_list):
            print(result_package.package)
            print(result_package.version)
            assert result_package.package == expected_package_list[index].package
            assert result_package.version == expected_package_list[index].version

    def test_get_files_for_package(self):

        package_info = PackageInfo(package="docker")
        result_list = self.rpm_environment.get_files_for_package(package_info)
        self._check_rpm_result_list(result_list)

    def test_get_packageinfo_from_packagefile(self):
        result_package = self.rpm_environment.get_packageinfo_from_packagefile("/tmp/docker.pkg")

        assert result_package.package == 'docker'
        assert result_package.version == '1.0-5'

    def test_get_files_from_packagefile(self):
        all_files = self.rpm_environment.get_files_from_packagefile("/tmp/docker.pkg")
        self._check_rpm_result_list(all_files)

    @staticmethod
    def _check_rpm_result_list(list_to_check):

        expected_file_list = list()

        # configuration-files
        expected_file_list.append(FileInfo("/etc/sysconfig/docker-network"))
        expected_file_list.append(FileInfo("/etc/sysconfig/docker-storage"))
        expected_file_list.append(FileInfo("/etc/sysconfig/docker-storage-setup"))

        # normal-files
        expected_file_list.append(FileInfo("/etc/docker"))
        expected_file_list.append(FileInfo("/etc/docker/certs.d"))
        expected_file_list.append(FileInfo("/etc/docker/certs.d/redhat.com"))
        expected_file_list.append(FileInfo("/var/lib/docker"))

        for index, result_file in enumerate(list_to_check):
            assert result_file.name == expected_file_list[index].name
            assert result_file.location == expected_file_list[index].location
            if index <= 2:  # These are configuration-files
                assert result_file.mutable is True
            assert result_file.location == expected_file_list[index].location
            assert result_file.full_pathname == expected_file_list[index].full_pathname
