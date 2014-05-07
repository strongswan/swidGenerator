# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import stat
import platform
from distutils.spawn import find_executable

from ..settings import DEFAULT_ENCODING


class CommonEnvironment(object):
    """
    The common base for all environment classes.
    """
    executable = None

    @staticmethod
    def get_architecture():
        """
        Return machine type, e.g. 'x86_64 or 'i386'.
        """
        return platform.machine()

    @staticmethod
    def get_os_string():
        """
        Return distribution string, e.g. 'debian_7.4'.
        """
        return '{dist[0]}_{dist[1]}'.format(dist=platform.dist())

    @staticmethod
    def is_file(path):
        """
        Determine whether the specified path is an existing file.

        This is needed because the package manager does not list only regular
        files, but also directories and message strings.

        It's also possible that the file/directory/symlink entries returned by
        DPKG don't exist in the filesystem.

        Known messages for dpkg:

        - 'package diverts to others'
        - 'Package XY does not contain any files(!)

        Args:
            path (str):
                The path to check.

        Returns:
            True or False

        """
        if path[0] != '/':
            return False

        try:
            mode = os.stat(path.encode(DEFAULT_ENCODING)).st_mode
        except OSError:
            return False

        if stat.S_ISDIR(mode):
            return False

        return True

    @classmethod
    def is_installed(cls):
        assert cls.executable is not None, 'Executable may not be None'
        return find_executable(cls.executable)
