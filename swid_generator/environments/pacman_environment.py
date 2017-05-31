# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from swid_generator.generators.utils import create_temp_folder
from swid_generator.command_manager import CommandManager as CM
from .common import CommonEnvironment
from ..package_info import PackageInfo, FileInfo


class PacmanEnvironment(CommonEnvironment):
    """
    Environment class for distributions using pacman as package manager (used
    by Arch Linux).

    """
    executable = 'pacman'

    required_packages_for_package_file_method = [
        "tar"
    ]

    required_packages_for_sign_method = [
        "xmlsec1"
    ]

    @classmethod
    def get_package_list(cls):
        """
        Get list of installed packages.

        Returns:
            List of ``PackageInfo`` instances.

        """

        command_args_packages = [cls.executable, '-Q', '--color', 'never']
        packages_output = CM.run_command_check_output(command_args_packages)
        lines = filter(None, packages_output.rstrip().split('\n'))
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
    def get_files_for_package(cls, package_info):
        """
        Get list of files related to the specified package.

        Caching could be implemented by using `Ql` without any package name.

        Args:
            package_name (str):
                The package name as string (e.g. ``cowsay``).

        Returns:
            List of ``FileInfo`` instances.

        """
        command_args_files = [cls.executable, '-Ql', package_info.package]
        files_output = CM.run_command_check_output(command_args_files)
        lines = filter(None, files_output.rstrip().split('\n'))
        result = []
        for line in lines:
            split_line = line.split(' ', 1)
            assert len(split_line) == 2, repr(split_line)
            file_path = split_line[1]
            if cls._is_file(file_path):
                file_info = FileInfo(file_path)
                # With the assumption that files in the '/etc'-Folders are mostly Configuration-Files
                if file_path.startswith("/etc/"):
                    file_info.mutable = True
                result.append(file_info)
        return result

    @classmethod
    def get_files_from_packagefile(cls, file_fullpathname):
        """
        Extract all information of a .pkg.tar.xz package.
        - List of all files
        - List of all Configuration-files

        This Method extract all the information in a temporary directory. The Debian package
        is extracted to the temporary directory, this because the files are needed to compute the File-Hash.

        :param file_pathname: Path to the .pkg.tar.xz package
        :return: Lexicographical sorted List of FileInfo()-Objects (Conffiles and normal Files)
        """
        all_files = []

        save_options = create_temp_folder(file_fullpathname)

        command_args_extract_package = ['tar', '-xf', save_options['absolute_package_path']]
        command_args_files = [cls.executable, '-Qlp', file_fullpathname]

        files_output = CM.run_command_check_output(command_args_files)

        lines = files_output.split('\n')
        lines = filter(lambda l: len(l) > 0, lines)

        CM.run_command(command_args_extract_package, working_directory=save_options['save_location'])

        for line in lines:
            path = line.split(' ')[1]
            temporary_path = save_options['save_location'] + path
            if cls._is_file(temporary_path):
                file_info = FileInfo(path, actual_path=False)
                file_info.set_actual_path(temporary_path)
                # With the assumption that files in the '/etc'-Folders are mostly Configuration-Files
                if path.startswith("/etc/"):
                    file_info.mutable = True
                all_files.append(file_info)

        return all_files

    @classmethod
    def get_packageinfo_from_packagefile(cls, file_path):
        """
        Extract the Package-Name and the Package-Version from the Pacman-Package.

        :param file_path: Path to the Pacman-Package
        :return: A PackageInfo()-Object with Package-Version and Package-Name.
        """
        command_args_packageinfo = [cls.executable, '--query', '--file', file_path]
        package_info_output = CM.run_command_check_output(command_args_packageinfo)
        line_split = package_info_output.split(' ')

        package_info = PackageInfo()
        package_info.package = line_split[0]
        package_info.version = line_split[1].rstrip()

        return package_info
