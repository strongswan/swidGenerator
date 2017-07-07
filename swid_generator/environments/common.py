# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import stat
import platform
from distutils.spawn import find_executable
from swid_generator.package_info import FileInfo
from swid_generator.exceptions import RequirementsNotInstalledError
from swid_generator.patches import unicode_patch


class CommonEnvironment(object):
    """
    The common base for all environment classes.
    """
    executable = None
    conffile_file_name = None
    control_archive = None
    required_packages_for_package_file_method = None
    required_packages_for_sign_method = None

    @staticmethod
    def get_architecture():
        """
        Return machine type, e.g. 'x86_64 or 'i386'.
        """
        return platform.machine()

    @staticmethod
    def get_os_string():
        """
        Return distribution string, e.g. 'Debian_7.4'.
        """
        dist = '_'.join(filter(None, platform.dist()[:2])).capitalize()
        system = platform.system().capitalize()
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
    def get_files_from_folder(cls, evidence_path, new_root_path):
        """
        Get all files from a path on the filesystem

        :param evidence_path: Path on the filesystem
        :return: Lexicographical sorted List of FileInfo()-Objects
        """
        result_files = []
        for dirpath, _, files in os.walk(evidence_path):
            for file in files:
                actual_path = '/'.join([unicode_patch(dirpath), unicode_patch(file)])
                if new_root_path is not None:
                    path_for_tag = actual_path.replace(unicode_patch(evidence_path), unicode_patch(new_root_path), 1)
                    path_for_tag = path_for_tag.replace('//', '/')
                    file_info = FileInfo(path_for_tag, actual_path=False)
                    file_info.set_actual_path(actual_path)
                else:
                    file_info = FileInfo(actual_path)

                result_files.append(file_info)
        return result_files

    @classmethod
    def check_package_installed(cls, package_name):
        """
        Checks if the Package is installed on System
        :param package_name: Name of the Package.
        :return: None if the package is not installed and the executable if package is installed.
        """
        return find_executable(package_name)

    @classmethod
    def check_requirements(cls, package_file_execution=False, sign_tag_execution=False):
        """
        Checks if all the Linux-commands are installed for the required operations (e.g: get_files_from_packagefile or signxml).
        If the Requirements are not met, a RequirementsNotInstalledError raises.
        :param package_file_execution: Default: False. Choice between get_files_from_packagefile or signxml operation.
        :param sign_tag_execution:
        """
        assert cls.required_packages_for_package_file_method is not None, 'List of required packages for package file execution may not be None'
        assert cls.required_packages_for_sign_method is not None, 'List of required packages for sing execution may not be None'

        not_installed_packages = list()

        required_packages = list()

        if package_file_execution is True:
            required_packages.extend(cls.required_packages_for_package_file_method)

        if sign_tag_execution is True:
            required_packages.extend(cls.required_packages_for_sign_method)

        for package in required_packages:
            is_installed = cls.check_package_installed(package)

            if is_installed is None:
                not_installed_packages.append(package)

        if len(not_installed_packages) != 0:
            raise RequirementsNotInstalledError("Please install following packages: " + ",".join(not_installed_packages))
