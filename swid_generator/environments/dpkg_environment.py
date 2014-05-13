# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import subprocess

from .common import CommonEnvironment
from ..package_info import PackageInfo, FileInfo


class DpkgEnvironment(CommonEnvironment):
    """
    Environment class for distributions using dpkg as package manager (e.g.
    Ubuntu, Debian or Mint).

    The packages are retrieved from the database using the ``dpkg-query`` tool:
    http://man7.org/linux/man-pages/man1/dpkg-query.1.html

    """
    executable = 'dpkg-query'

    installed_states = {
        'install ok installed': True,
        'deinstall ok config-files': False
    }

    @classmethod
    def get_list(cls):
        """
        Get list of installed packages.

        Returns:
            List of ``PackageInfo`` instances.

        """
        command_args = [cls.executable, '-W', '-f=${Package}\\t${Version}\\t${Status}\\n']
        data = subprocess.check_output(command_args)
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        line_list = data.split('\n')
        result = []
        for line in line_list:
            split_line = line.split('\t')
            if len(split_line) == 3:
                info = PackageInfo()
                info.package = split_line[0]
                info.version = split_line[1]
                info.status = split_line[2]
                result.append(info)
        return [r for r in result if cls.package_installed(r)]

    @classmethod
    def get_files_for_package(cls, package_name):
        """
        Get list of files related to the specified package.

        Args:
            package_name (str):
                The package name as string (e.g. ``cowsay``).

        Returns:
            List of ``FileInfo`` instances.

        """
        command_args = [cls.executable, '-L', package_name]
        data = subprocess.check_output(command_args)
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        lines = data.rstrip().split('\n')
        files = filter(cls.is_file, lines)
        return [FileInfo(path) for path in files]

    @classmethod
    def package_installed(cls, package_info):
        """
        Try to find out whether the specified package is installed or not.

        If the installed state cannot be determined with certainty we assume
        it's installed.

        Args:
            package_info (package_info.PackageInfo):
                The package to check.

        Returns:
            True or False

        """
        return cls.installed_states.get(package_info.status, True)
