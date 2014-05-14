# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import subprocess

from .common import CommonEnvironment
from ..package_info import PackageInfo, FileInfo


class PacmanEnvironment(CommonEnvironment):
    """
    Environment class for distributions using pacman as package manager (used
    by Arch Linux).

    """
    executable = 'pacman'

    @classmethod
    def get_list(cls):
        """
        Get list of installed packages.

        Returns:
            List of ``PackageInfo`` instances.

        """
        command_args = [cls.executable, '-Q', '--color', 'never']
        data = subprocess.check_output(command_args)
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        lines = filter(None, data.rstrip().split('\n'))
        result = []
        for line in lines:
            split_line = line.split()
            assert len(split_line) == 2, repr(split_line)
            info = PackageInfo()
            info.package = split_line[0]
            info.version = split_line[1]
            result.append(info)
        return result

    @classmethod
    def get_files_for_package(cls, package_name):
        """
        Get list of files related to the specified package.

        Caching could be implemented by using `Ql` without any package name.

        Args:
            package_name (str):
                The package name as string (e.g. ``cowsay``).

        Returns:
            List of ``FileInfo`` instances.

        """
        command_args = [cls.executable, '-Ql', package_name]
        data = subprocess.check_output(command_args)
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        lines = filter(None, data.rstrip().split('\n'))
        result = []
        for line in lines:
            split_line = line.split(' ', 1)
            assert len(split_line) == 2, repr(split_line)
            filepath = split_line[1]
            if cls.is_file(filepath):
                result.append(filepath)
        return [FileInfo(path) for path in result]
