import subprocess
import platform
import os
import os.path
import stat

from .common import CommonEnvironment
from ..package_info import PackageInfo, FileInfo


class DpkgEnvironment(CommonEnvironment):
    # http://man7.org/linux/man-pages/man1/dpkg-query.1.html
    installed_states = {
        'install ok installed': True,
        'deinstall ok config-files': False
    }

    @staticmethod
    def is_file(path):
        # if path doesnt start with a /, its not a file.
        # known cases:
        # - 'package diverts to others'
        # - 'Package XY does not contain any files(!)
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
    def get_list(include_files=False):
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
                # TODO check if installed here, before adding to list
                if include_files:
                    info.files = DpkgEnvironment.get_files_for_package(info.package)
                result.append(info)
        return filter(DpkgEnvironment.is_installed, result)

    @staticmethod
    def get_os_string():
        dist = platform.dist()
        return dist[0] + '_' + dist[1]

    @staticmethod
    def is_installed(packet_info):
        # if the installed state cannot be determined with certainty
        # we assume its installed
        return DpkgEnvironment.installed_states.get(packet_info.status, True)
