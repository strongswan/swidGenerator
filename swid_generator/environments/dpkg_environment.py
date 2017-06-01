# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import subprocess
import ntpath

from swid_generator.generators.utils import create_temp_folder
from swid_generator.command_manager import CommandManager as CM
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
    conffile_file_name = './conffiles'
    control_archive = 'control.tar.gz'

    installed_states = {
        'install ok installed': True,
        'deinstall ok config-files': False
    }

    required_packages_for_package_file_method = [
        "tar",
        "ar"
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
        result = []
        command_args = [cls.executable_query, '-W', '-f=${Package}\\n${Version}\\n${Status}\\n${conffiles}\\t']

        command_output = CM.run_command_check_output(command_args)

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
        stripped_lines = []

        command_args_normal_files = [cls.executable_query, '-L', package_info.package]
        command_normal_file_output = CM.run_command_check_output(command_args_normal_files)

        lines = command_normal_file_output.rstrip().split('\n')
        normal_files = filter(cls._is_file, lines)

        command_args_config_files = [cls.executable_query, '-W', '-f=${conffiles}\\n', package_info.package]
        command_config_file_output = CM.run_command_check_output(command_args_config_files)

        lines = command_config_file_output.split('\n')

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

        return sorted(result, key=lambda f: f.full_pathname)

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
        save_options = create_temp_folder(file_pathname)

        result = []
        result_help_list = []  # needed to check duplications

        command_args_unpack_package = [cls.executable, '-x', save_options['absolute_package_path'], save_options['save_location']]
        command_args_extract_controlpackage = ["ar", "x", save_options['absolute_package_path'], cls.control_archive]
        command_args_extract_conffile = ["tar", "-zxf", "/".join((save_options['save_location'], cls.control_archive)), cls.conffile_file_name]
        command_args_file_list = [cls.executable, '-c', file_pathname]

        def _add_to_result_list(file_path, actual_path, mutable=False):
            result_help_list.append(file_path)
            file_info = FileInfo(file_path, actual_path=False)
            file_info.set_actual_path(actual_path)
            file_info.mutable = mutable
            result.append(file_info)

        # Extraction of all needed Files (Store Files into tmp folder), extract Configuration-Files entries
        try:
            CM.run_command(command_args_unpack_package)
            CM.run_command(command_args_extract_controlpackage, working_directory=save_options['save_location'])
            CM.run_command(command_args_extract_conffile, working_directory=save_options['save_location'])

            temp_conffile_save_location = "/".join((save_options['save_location'], cls.conffile_file_name))

            with open(temp_conffile_save_location, 'rb') as afile:
                file_content = afile.read().encode('utf-8')

        except(IOError, subprocess.CalledProcessError):
            # If no file extracted from command -> no .conffile-File exists
            file_content = None
            config_file_paths = []

        # Extract Configuration-Files-Entries from output
        if file_content is not None:
            config_file_paths = filter(lambda path: len(path) > 0, file_content.split('\n'))

            for config_file_path in config_file_paths:
                _add_to_result_list(config_file_path, save_options['save_location'] + config_file_path, mutable=True)

        # Extraction of file-list
        output_file_list = CM.run_command_check_output(command_args_file_list)
        line_list = output_file_list.split('\n')

        for line in line_list:

            splitted_line = line.split(' ')
            directory_or_file_path = splitted_line[-1]

            if "->" in splitted_line:
                # symbol-link
                symbol_link = (splitted_line[-3])[1:]
                temp_save_location_symbol_link = "/".join((save_options['save_location'], symbol_link))
                head, _ = ntpath.split(symbol_link)

                if "../" in directory_or_file_path:
                    root, _ = ntpath.split(head)
                    directory_or_file_path = root + directory_or_file_path[2:]
                else:
                    directory_or_file_path = "/".join((head, directory_or_file_path))

                if cls._is_file(temp_save_location_symbol_link):
                    if symbol_link not in config_file_paths and symbol_link not in result_help_list:
                        _add_to_result_list(symbol_link, temp_save_location_symbol_link)
            else:
                directory_or_file_path = directory_or_file_path[1:]

            temp_save_location_file = "/".join((save_options['save_location'], directory_or_file_path))

            if cls._is_file(temp_save_location_file):
                if directory_or_file_path not in config_file_paths and directory_or_file_path not in result_help_list:
                    _add_to_result_list(directory_or_file_path, temp_save_location_file)

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
        package_name = CM.run_command_check_output(command_args_packagename)
        package_version = CM.run_command_check_output(command_args_version)

        package_info = PackageInfo()
        package_info.package = package_name.strip()
        package_info.version = package_version.strip()

        return package_info
