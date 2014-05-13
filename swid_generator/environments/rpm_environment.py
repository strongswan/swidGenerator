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
    def get_list(cls):
        """
        Get list of installed packages.

        Returns:
            List of ``PackageInfo`` instances.

        """
        command_args = [cls.executable, '-qa', '--queryformat', '%{name}\t%{version}-%{release}\n']
        data = subprocess.check_output(command_args)
        if isinstance(data, bytes):  # convert to unicode
            data = data.decode('utf-8')
        line_list = data.split('\n')
        result = []

        for line in line_list:
            split_line = list(filter(len, line.split()))
            if len(split_line) == 2:
                info = PackageInfo()
                info.package = split_line[0]
                info.version = split_line[1]
                result.append(info)

        return result

    @classmethod
    def get_files_for_package(cls, package_name):
        command_args = [cls.executable, '-ql', package_name]
        data = subprocess.check_output(command_args)
        if isinstance(data, bytes):  # convert to unicode
            data = data.decode('utf-8')
        lines = data.rstrip().split('\n')
        files = filter(cls.is_file, lines)
        return [FileInfo(path) for path in files]
