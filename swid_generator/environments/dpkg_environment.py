# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import subprocess

from swid_generator.command_manager import CommandManager
from .common import CommonEnvironment
from ..package_info import PackageInfo, FileInfo


class DpkgEnvironment(CommonEnvironment):
    """
    Environment class for distributions using dpkg as package manager (e.g.
    Ubuntu, Debian or Mint).

    The packages are retrieved from the database using the ``dpkg-query`` tool:
    http://man7.org/linux/man-pages/man1/dpkg-query.1.html

    """
    executable_query = 'dpkg-query'
    executable = 'dpkg'
    md5_hash_length = 32
    CONFFILE_FILE_NAME = 'conffiles'
    CONTROL_ARCHIVE = 'control.tar.gz'

    installed_states = {
        'install ok installed': True,
        'deinstall ok config-files': False
    }

    @classmethod
    def get_package_list(cls):
        """
        Get list of installed packages.

        Returns:
            List of ``PackageInfo`` instances.

        """
        result = []
        command_args = [cls.executable_query,
                        '-W', '-f=${Package}\\n${Version}\\n${Status}\\n${conffiles}\\t']

        command_output = CommandManager.run_command_check_output(command_args)

        line_list = command_output.split('\t')

        for line in line_list:
            split_line = line.split('\n')

            if len(split_line) >= 4:
                package_info = PackageInfo()
                package_info.package = split_line[0]
                package_info.version = split_line[1]
                package_info.status = split_line[2]

                result.append(package_info)

        return [r for r in result if cls._package_installed(r)]

    @classmethod
    def get_files_for_package(cls, package_info):
        """
        Get list of files related to the specified package.

        Args:
            package_info (PackageInfo):
                The ``PackageInfo`` instance for the query.

        Returns:
            List of ``FileInfo`` instances.

        """
        result = []

        command_args_normal_files = [cls.executable_query, '-L', package_info.package]
        command_normal_file_output = CommandManager.run_command_check_output(command_args_normal_files)

        lines = command_normal_file_output.rstrip().split('\n')
        normal_files = filter(cls._is_file, lines)

        command_args_config_files = [cls.executable_query, '-W', '-f=${conffiles}\\n', package_info.package]
        command_config_file_output = CommandManager.run_command_check_output(command_args_config_files)

        lines = command_config_file_output.split('\n')
        stripped_lines = []

        for line in lines:
            if len(line) != 0:
                path_without_md5 = line.strip()[:len(line.strip()) - cls.md5_hash_length].strip()
                stripped_lines.append(path_without_md5)

        config_files = filter(cls._is_file, stripped_lines)

        for config_file_path in config_files:
            file_info = FileInfo(config_file_path)
            file_info.mutable = True
            result.append(file_info)

        for file_path in normal_files:
            if file_path not in config_files:
                result.append(FileInfo(file_path))

        return result

    @classmethod
    def _package_installed(cls, package_info):
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

    @classmethod
    def get_files_from_packagefile(cls, file_pathname):
        """
        Extract all information of a .deb package.
        - List of all files
        - List of all Configuration-files

        This Method extract all the information in a temporary directory. The Debian package
        is extracted to the temporary directory, this because the files are needed to compute the File-Hash.

        :param file_pathname: Path to the .deb package
        :return: Lexicographical sorted List of FileInfo()-Objects (Conffiles and normal Files)
        """
        save_options = cls._create_temp_folder(file_pathname)
        result = []

        command_args_unpack_package = [cls.executable, '-x', save_options['absolute_package_path'],
                                       save_options['save_location']]

        command_args_extract_controlpackage = ["ar", "x", save_options['absolute_package_path'],
                                               cls.CONTROL_ARCHIVE]

        command_args_extract_conffile = ["tar", "-zxf", "/".join((save_options['save_location'],
                                                                  cls.CONTROL_ARCHIVE)), "./conffiles"]

        CommandManager.run_command(command_args_unpack_package)

        try:
            CommandManager.run_command(command_args_extract_controlpackage,
                                       working_directory=save_options['save_location'])
            CommandManager.run_command(command_args_extract_conffile,
                                       working_directory=save_options['save_location'])

            conffile_save_location = "/".join((save_options['save_location'], cls.CONFFILE_FILE_NAME))

            with open(conffile_save_location, 'rb') as afile:
                file_content = afile.read().encode('utf-8')

            config_file_paths = filter(lambda path: len(path) > 0, file_content.split('\n'))

            for config_file_path in config_file_paths:
                file_info = FileInfo(config_file_path, actual_path=False)
                file_info.set_actual_path(save_options['save_location'] + config_file_path)
                file_info.mutable = True
                result.append(file_info)

        except(IOError, subprocess.CalledProcessError):
            config_file_paths = []

        command_args_file_list = [cls.executable, '-c', file_pathname]
        command_output_list = CommandManager.run_command_check_output(command_args_file_list)

        line_list = command_output_list.split('\n')

        for line in line_list:
            splitted_line_array = line.split(' ')

            if '->' in splitted_line_array:
                # symbol-link
                directory_or_file_path = splitted_line_array[-3]
            else:
                # Last-Entry from Array is File-Path
                directory_or_file_path = splitted_line_array[-1]

            path_without_leading_point = directory_or_file_path[1:]

            temp_save_location = str("/".join((save_options['save_location'], path_without_leading_point)))

            if cls._is_file(temp_save_location):
                if path_without_leading_point not in config_file_paths:
                    file_info = FileInfo(path_without_leading_point, actual_path=False)
                    file_info.set_actual_path(temp_save_location)
                    result.append(file_info)

        return sorted(result, key=lambda f: f.full_pathname)

    @classmethod
    def get_packageinfo_from_packagefile(cls, file_path):
        """
        Extract the Package-Name and the Package-Version from the Debian-Package.

        :param file_path: Path to the Debian-Package
        :return: A PackageInfo()-Object with Package-Version and Package-Name.
        """
        command_args_packagename = [cls.executable, '-f', file_path, 'Package']
        command_args_version = [cls.executable, '-f', file_path, 'Version']
        package_name = CommandManager.run_command_check_output(command_args_packagename)
        package_version = CommandManager.run_command_check_output(command_args_version)

        package_info = PackageInfo()
        package_info.package = package_name.strip()
        package_info.version = package_version.strip()

        return package_info
