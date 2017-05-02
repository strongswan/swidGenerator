# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest
import os

from minimock import Mock

from swid_generator.command_manager import CommandManager
from tests.fixtures.command_manager_mock import CommandManagerMock
from swid_generator.environments.dpkg_environment import DpkgEnvironment
from swid_generator.package_info import PackageInfo, FileInfo
from swid_generator.environments.common import CommonEnvironment


@pytest.fixture
def dpkg_environment():
    return DpkgEnvironment()


def setup():
    CommandManager.run_command_check_output = Mock('CommandManager.run_command_check_output',
                                                   returns_func=CommandManagerMock.run_command_check_output)
    CommonEnvironment._is_file = Mock('CommonEnvironment._is_file', returns=True)

    os.path.getsize = Mock('os.path.getsize', returns=1)


setup()


def test_get_package_list(dpkg_environment):
    result_list = dpkg_environment.get_package_list()
    print(result_list)

    for res in result_list:
        print(res.package)

    return True



def test_get_files_for_package(dpkg_environment):
    return True


def test_get_packageinfo_from_packagefile(dpkg_environment):
    return True
