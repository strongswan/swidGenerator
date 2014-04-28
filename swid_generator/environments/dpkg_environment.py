# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import subprocess
import platform
import os
import os.path
import stat
from distutils.spawn import find_executable


from .common import CommonEnvironment
from ..package_info import PackageInfo, FileInfo


class DpkgEnvironment(CommonEnvironment):
    # http://man7.org/linux/man-pages/man1/dpkg-query.1.html
    installed_states = {
        'install ok installed': True,
        'deinstall ok config-files': False
    }

    executable = 'dpkg-query'

    @staticmethod
    def is_file(path):
        """
        Determine if the path is a file. Need because Packagemanager not only lists regular files.
        Also directories (which could be non existent), symbolic links (which could point to non existent files)
        and even Messages.
        Known messages for dpkg:
         - 'package diverts to others'
         - 'Package XY does not contain any files(!)

         Args:
            path (str)
                The path to check

        Returns:
            Boolean

         """
        if path[0] != '/':
            return False

        try:
            mode = os.stat(path).st_mode
        except OSError:
            return False

        if stat.S_ISDIR(mode):
            return False

        return True

    @staticmethod
    def get_files_for_package(package_name):
        command_args = ['dpkg-query', '-L', package_name]
        data = subprocess.check_output(command_args)
        lines = data.rstrip().split('\n')
        files = filter(DpkgEnvironment.is_file, lines)
        return [FileInfo(path) for path in files]

    @staticmethod
    def get_list():
        command_args = ['dpkg-query', '-W', '-f=${Package}\\t${Version}\\t${Status}\\n']
        data = subprocess.check_output(command_args)
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
        return filter(DpkgEnvironment.package_installed, result)

    @staticmethod
    def get_os_string():
        dist = platform.dist()
        return dist[0] + '_' + dist[1]

    @staticmethod
    def package_installed(packet_info):
        # if the installed state cannot be determined with certainty
        # we assume its installed
        return DpkgEnvironment.installed_states.get(packet_info.status, True)

    @staticmethod
    def is_installed():
        return find_executable(DpkgEnvironment.executable)
