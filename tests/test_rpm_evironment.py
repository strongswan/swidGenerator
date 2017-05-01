# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest
import os

from minimock import Mock

from swid_generator.command_manager import CommandManager
from tests.fixtures.command_manager_mock import CommandManagerMock
from swid_generator.environments.rpm_environment import RpmEnvironment
from swid_generator.package_info import PackageInfo, FileInfo
from swid_generator.environments.common import CommonEnvironment


@pytest.fixture
def rpm_environment():
    return RpmEnvironment()


def setup():
    CommandManager.run_command_check_output = Mock('CommandManager.run_command_check_output',
                                                   returns_func=CommandManagerMock.run_command_check_output)
    CommonEnvironment._is_file = Mock('CommonEnvironment._is_file', returns=True)

    os.path.getsize = Mock('os.path.getsize', returns=1)


setup()


def test_get_package_list(rpm_environment):
    result_list = rpm_environment.get_package_list()

    expected_package_list = list()

    expected_package_list.append(PackageInfo(package="perl-Git", version="2.9.3-3.fc25"))
    expected_package_list.append(PackageInfo(package="fedora-repos", version="25-3"))
    expected_package_list.append(PackageInfo(package="perl-IO-Socket-SSL", version="2.038-1.fc25"))
    expected_package_list.append(PackageInfo(package="setup", version="2.10.4-1.fc25"))

    for index, result_package in enumerate(result_list):
        print(result_package.package)
        print(result_package.version)
        assert result_package.package == expected_package_list[index].package
        assert result_package.version == expected_package_list[index].version


def test_get_files_for_package(rpm_environment):

    package_info = PackageInfo(package="docker")

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

    result_list = rpm_environment.get_files_for_package(package_info)

    for res in result_list:
        print(res.name)

    for index, result_file in enumerate(result_list):
        assert result_file.name == expected_file_list[index].name
        assert result_file.location == expected_file_list[index].location
        if index <= 2:
            assert result_file.mutable is True
        assert result_file.location == expected_file_list[index].location
        assert result_file.full_pathname == expected_file_list[index].full_pathname


def test_get_packageinfo_from_packagefile(rpm_environment):
    result_package = rpm_environment.get_packageinfo_from_packagefile("/tmp/docker.pkg")

    assert result_package.package == 'docker'
    assert result_package.version == '1.0-5'
