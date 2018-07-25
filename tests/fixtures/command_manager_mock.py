# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import tests.fixtures.mock_data as mock_data


class MockStdout():
    def __init__(self):
        self.stdout = {}


class PipeMock(object):
    def __init__(self):
        self.stdout = MockStdout()


class CommandManagerMock(object):

    @staticmethod
    def run_command(command_argumentlist, working_directory=os.getcwd()):
        return True

    @staticmethod
    def run_command_check_output(command_argumentlist, stdin=None, working_directory=os.getcwd()):
        if command_argumentlist == ['rpm', '-qa', '--queryformat', '\t%{name} %{version}-%{release}.%{arch} %{summary}']:
            return mock_data.rpm_query_package_list_output
        if command_argumentlist == ['rpm', '-ql', 'docker']:
            return mock_data.rpm_query_file_list
        if command_argumentlist == ['rpm', '-qa', '--queryformat', '%{name}\n', '-c', 'docker']:
            return mock_data.rpm_query_conffile_list
        if command_argumentlist == ['rpm', "--query", "--package", "--queryformat", "%{name}", "/tmp/docker.pkg"]:
            return "docker"
        if command_argumentlist == ['rpm', "--query", "--package", "--queryformat", "%{version}-%{release}.%{arch}", "/tmp/docker.pkg"]:
            return "1.0-5"
        if command_argumentlist == ['rpm', "--query", "--package", "/tmp/docker.pkg", "-l"]:
            return mock_data.rpm_query_file_list
        if command_argumentlist == ['rpm', "--query", "--package", "/tmp/docker.pkg", "-c"]:
            return mock_data.rpm_query_conffile_list
        if command_argumentlist == ['dpkg-query', '-W', '-f=${Package}\\n${Version}\\n${Status}\\n${binary:Summary}\\n${conffiles}\\t']:
            return mock_data.dpkg_query_package_list_output
        if command_argumentlist == ['dpkg-query', '-W', '-f=${Package}\\n${Version}.${Architecture}\\n${Status}\\n${binary:Summary}\\n${conffiles}\\t']:
            return mock_data.dpkg_query_package_arch_list_output
        if command_argumentlist == ['dpkg-query', '-L', "docker"]:
            return mock_data.dpkg_query_file_list
        if command_argumentlist == ['dpkg-query', '-W', '-f=${conffiles}\\n', "docker"]:
            return mock_data.dpkg_query_conffile_list
        if command_argumentlist == ['dpkg', '-f', '/tmp/docker.pkg', 'Package']:
            return "docker"
        if command_argumentlist == ['dpkg', '-f', '/tmp/docker.pkg', 'Version']:
            return "1.0-5"
        if command_argumentlist == ['dpkg', '-f', '/tmp/docker.pkg', 'Architecture']:
            return "amd64"
        if command_argumentlist == ['dpkg', '-c', '/tmp/docker.pkg']:
            return mock_data.dpkg_query_file_list_package
        if command_argumentlist == ['pacman', '-Q', '--color', 'never']:
            return mock_data.pacman_query_package_list_output
        if command_argumentlist == ['pacman', '-Ql', 'docker']:
            return mock_data.pacman_query_file_list
        if command_argumentlist == ['pacman', '--query', '--file', '/tmp/docker.pkg']:
            return "docker 1:17.04.0-1"
        if command_argumentlist == ['pacman', '-Qlp', '/tmp/docker.pkg']:
            return mock_data.pacman_query_file_list_package

    @staticmethod
    def run_command_popen(command_argumentlist, stdout=None):
        if command_argumentlist == ['rpm2cpio', "/tmp/docker.pkg"]:
            return PipeMock()
        if command_argumentlist == ['cpio', "-id", "--quiet"]:
            return {}
