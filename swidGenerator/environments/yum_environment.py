import subprocess
import platform
import os.path

from swidGenerator.package_info import PackageInfo, FileInfo
from .common import CommonEnvironment


class YumEnvironment(CommonEnvironment):
    command_args = ['yum', 'list', 'installed']

    @staticmethod
    def get_list(include_files=False):
        data = subprocess.check_output(YumEnvironment.command_args)
        line_list = data.split('\n')
        result = []

        for line in line_list:
            split_line = filter(len, line.split(' '))
            if len(split_line) == 3:
                info = PackageInfo()
                info.package = split_line[0]
                info.version = split_line[1]
                if include_files:
                    info.files = YumEnvironment.get_files_for_package(info.package)
                result.append(info)

        return result

    @staticmethod
    def is_file(path):
        #TODO there are some not existent directories, what to do with them?
        return os.path.isfile(path) or (os.path.islink(path) and not os.path.isdir(path))

    @staticmethod
    def get_files_for_package(package_name):
        command_args = ['rpm', '-ql', package_name]
        data = subprocess.check_output(command_args)
        lines = data.rstrip().split('\n')
        files = filter(YumEnvironment.is_file, lines)
        return [FileInfo(path) for path in files]

    @staticmethod
    def get_os_string():
        dist = platform.dist()
        return dist[0] + '_' + dist[1]