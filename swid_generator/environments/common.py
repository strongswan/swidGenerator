# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import stat
import platform
from distutils.spawn import find_executable
import random
import string


class CommonEnvironment(object):
    """
    The common base for all environment classes.
    """
    executable = None
    TEMP_FOLDER_NAME = '/tmp'
    FOLDER_PREFIX = 'swid_'
    CONFFILE_FILE_NAME = None

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
    def _create_temp_folder(cls, package_path):
        """
        It creates a folder in the directory /tmp of the client/server.
        This folder has the prefix "swid_". To this prefix a random generated String is appended to
        prevent collisions of foldernames.

        :param package_path: Path to the package
        :return: A dictionary with the save options of the temporary folder.
        """

        random_string = ''.join(random.choice(string.ascii_letters) for _ in range(5))

        if package_path[0] is not '/':
            absolute_package_path = '/'.join((os.getcwd(), package_path))
        else:
            absolute_package_path = package_path

        save_location_pathname = '/'.join((cls.TEMP_FOLDER_NAME, cls.FOLDER_PREFIX + random_string))

        if not os.path.exists(save_location_pathname):
            os.makedirs(save_location_pathname)

        folder_information = {
            'absolute_package_path': absolute_package_path,
            'save_location': save_location_pathname
        }

        return folder_information

    @classmethod
    def is_installed(cls):
        assert cls.executable is not None, 'Executable may not be None'
        return find_executable(cls.executable)
