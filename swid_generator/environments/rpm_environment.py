# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import subprocess

from .common import CommonEnvironment
from ..package_info import PackageInfo, FileInfo


class RpmEnvironment(CommonEnvironment):
    """
    Environment class for distributions using RPM as package manager (e.g.
    Fedora, Red Hat or OpenSUSE).

    The packages are retrieved from the database directly using the ``rpm``
    command.

    """
    executable = 'rpm'

    @classmethod
    def get_package_list(cls):
        """
        Get list of installed packages.

        Returns:
            List of ``PackageInfo`` instances.

        """

        command_args = [cls.executable, '-qa', '--queryformat', '\t%{name} %{version}-%{release}', '-c']
        data = subprocess.check_output(command_args)
        if isinstance(data, bytes):  # convert to unicode
            data = data.decode('utf-8')

        line_list = data.split('\t')
        result = []

        for line in line_list:
            split_line = line.replace('\n', " ").split()
            if len(split_line) >= 2:
                package_info = PackageInfo()
                package_info.package = split_line[0]
                package_info.version = split_line[1]

                # if Config-Files exists
                if len(split_line) >= 3:
                    config_files = []
                    for file_path in split_line[2:len(split_line)]:
                        file_info = FileInfo(file_path)
                        file_info.mutable = True
                        config_files.append(file_info)

                    package_info.files.extend(config_files)

                result.append(package_info)

        return result

    @classmethod
    def get_files_for_package(cls, package_info):
        command_args = [cls.executable, '-ql', package_info.package]
        data = subprocess.check_output(command_args)
        if isinstance(data, bytes):  # convert to unicode
            data = data.decode('utf-8')
        lines = data.rstrip().split('\n')
        files = filter(cls._is_file, lines)

        result_list = []

        for path in files:
            if not any(file_info.full_pathname.strip() == path for file_info in package_info.files):
                result_list.append(FileInfo(path))

        return result_list
