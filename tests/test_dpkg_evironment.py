# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import unittest

from swid_generator.command_manager import CommandManager
from tests.fixtures.command_manager_mock import CommandManagerMock
from swid_generator.environments.dpkg_environment import DpkgEnvironment
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

        self.dpkg_environment = DpkgEnvironment()

    def tearDown(self):
        self.command_manager_run_check_output_patch.stop()
        self.command_manager_run_command_patch.stop()
        self.common_environment_is_file_patch.stop()
        self.os_path_getsize_patch.stop()

    def test_get_package_list(self):
        result_list = self.dpkg_environment.get_package_list()

        expected_package_list = list()

        expected_package_list.append(PackageInfo(package="adduser", version="3.113+nmu3ubuntu4"))
        expected_package_list.append(PackageInfo(package="apt", version="1.2.19"))
        expected_package_list.append(PackageInfo(package="base-files", version="9.4ubuntu4.4"))

        for index, result_package in enumerate(result_list):
            print(result_package.package)
            print(result_package.version)
            assert result_package.package == expected_package_list[index].package
            assert result_package.version == expected_package_list[index].version

    def test_get_package_arch_list(self):
        result_list = self.dpkg_environment.get_package_list({ "dpkg_include_package_arch": True })

        expected_package_list = list()

        expected_package_list.append(PackageInfo(package="adduser", version="3.113+nmu3ubuntu4.all"))
        expected_package_list.append(PackageInfo(package="apt", version="1.2.19.amd64"))
        expected_package_list.append(PackageInfo(package="base-files", version="9.4ubuntu4.4.amd64"))

        for index, result_package in enumerate(result_list):
            print(result_package.package)
            print(result_package.version)
            assert result_package.package == expected_package_list[index].package
            assert result_package.version == expected_package_list[index].version

    def test_get_files_for_package(self):
        package_info = PackageInfo(package="docker")
        result_list = self.dpkg_environment.get_files_for_package(package_info)

        expected_file_list = list()

        expected_file_list.append(FileInfo("/etc/apt/apt.conf.d/01autoremove"))
        expected_file_list.append(FileInfo("/etc/cron.daily/apt-compat"))
        expected_file_list.append(FileInfo("/etc/kernel/postinst.d/apt-auto-removal"))
        expected_file_list.append(FileInfo("/usr/share/doc/docker"))
        expected_file_list.append(FileInfo("/usr/share/doc/docker/changelog.Debian.gz"))
        expected_file_list.append(FileInfo("/usr/share/menu"))
        expected_file_list.append(FileInfo("/usr/share/menu/docker"))

        for index, result_file in enumerate(result_list):
            assert result_file.name == expected_file_list[index].name
            assert result_file.location == expected_file_list[index].location
            if index <= 2:  # These are configuration-files
                assert result_file.mutable is True
            assert result_file.location == expected_file_list[index].location
            assert result_file.full_pathname == expected_file_list[index].full_pathname

    def test_get_packageinfo_from_packagefile(self):
        result_package = self.dpkg_environment.get_packageinfo_from_packagefile("/tmp/docker.pkg")

        print(result_package.package)

        assert result_package.package == 'docker'
        assert result_package.version == '1.0-5'

    def test_get_packageinfo_arch_from_packagefile(self):
        result_package = self.dpkg_environment.get_packageinfo_from_packagefile("/tmp/docker.pkg", { "dpkg_include_package_arch": True })

        print(result_package.package)

        assert result_package.package == 'docker'
        assert result_package.version == '1.0-5.amd64'

    def test_get_files_from_packagefile(self):
        all_files = self.dpkg_environment.get_files_from_packagefile("/tmp/docker.pkg")

        for f in all_files:
            print(f.full_pathname)

        expected_file_list = list()

        expected_file_list.append(FileInfo("/usr/share/bug/docker-bin/control"))
        expected_file_list.append(FileInfo("/usr/share/bug/docker/control"))
        expected_file_list.append(FileInfo("/usr/share/doc/docker/README.backtrace"))
        expected_file_list.append(FileInfo("/usr/share/man/man8/docker.8.gz"))
        expected_file_list.append(FileInfo("/usr/share/man/man8/dockerctl.8.gz"))

        for index, result_file in enumerate(all_files):
            assert result_file.name == expected_file_list[index].name
            assert result_file.location == expected_file_list[index].location
            assert result_file.location == expected_file_list[index].location
            assert result_file.full_pathname == expected_file_list[index].full_pathname

