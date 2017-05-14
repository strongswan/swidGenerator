# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import stat
import platform
from distutils.spawn import find_executable
from swid_generator.exceptions import RequirementsNotInstalledError


class CommonEnvironment(object):
    """
    The common base for all environment classes.
    """
    executable = None
    CONFFILE_FILE_NAME = None
    required_packages_package_file_method = None
    required_packages_sign_method = None

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
        dist = '_'.join(filter(None, platform.dist()[:2]))
        system = platform.system().lower()
        return dist or system or platform.os.name or 'unknown'

    @staticmethod
    def _is_file(path):
        """
        Determine whether the specified path is an existing file.

        This is needed because some package managers don't list only regular
        files, but also directories and message strings.

        It's also possible that the file/directory/symlink entries returned by
        the package manager don't actually exist in the filesystem.

        Args:
            path (str):
                The path to check.

        Returns:
            True or False

        """
        if path[0] != '/':
            return False

        try:
            mode = os.stat(path.encode('utf-8')).st_mode
        except OSError:
            return False

        if stat.S_ISDIR(mode):
            return False

        return True

    @classmethod
    def is_installed(cls):
        assert cls.executable is not None, 'Executable may not be None'
        return find_executable(cls.executable)

    @classmethod
    def check_package_installed(cls, package_name):
        return find_executable(package_name)

    @classmethod
    def check_requirements(cls, package_file_execution=False, sign_tag_execution=False):

        assert cls.required_packages_package_file_method is not None, 'List of required packages for package file execution may not be None'
        assert cls.required_packages_sign_method is not None, 'List of required packages for sing execution may not be None'

        not_installed_packages = list()

        required_packages = list()

        if package_file_execution is True:
            required_packages.extend(cls.required_packages_package_file_method)

        if sign_tag_execution is True:
            required_packages.extend(cls.required_packages_sign_method)

        for package in required_packages:
            is_installed = cls.check_package_installed(package)

            if is_installed is None:
                not_installed_packages.append(package)

        if len(not_installed_packages) != 0:
            raise RequirementsNotInstalledError("Please install following packages: " + ",".join(not_installed_packages))
