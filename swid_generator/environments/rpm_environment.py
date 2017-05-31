# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import subprocess

from swid_generator.generators.utils import create_temp_folder
from swid_generator.command_manager import CommandManager as CM
from .common import CommonEnvironment
from ..package_info import PackageInfo, FileInfo


class RpmEnvironment(CommonEnvironment):
    """
    Environment class for distributions using RPM as package manager (e.g.
    Fedora, Red Hat or OpenSUSE).

    The packages are retrieved from the database directly using the ``rpm``
    command.

    """
    executable = 'rpm'
    conffile_file_name = 'conffiles'
    control_archive = 'control.tar.gz'

    required_packages_for_package_file_method = [
        "rpm2cpio",
        "cpio"
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

        command_args_package_list = [cls.executable, '-qa', '--queryformat',
                                     '\t%{name} %{version}-%{release}']
        package_list_output = CM.run_command_check_output(command_args_package_list)

        line_list = package_list_output.split('\t')
        result = []

        for line in line_list:
            split_line = line.replace('\n', " ").split()
            if len(split_line) >= 2:
                package_info = PackageInfo()
                package_info.package = split_line[0]
                package_info.version = split_line[1]
                result.append(package_info)
        return result

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

        command_args_file_list = [cls.executable, '-ql', package_info.package]
        command_args_package_list = [cls.executable, '-qa', '--queryformat', '%{name}\n', '-c', package_info.package]

        file_list_output = CM.run_command_check_output(command_args_file_list)
        lines_file_list = file_list_output.rstrip().split('\n')
        files = filter(cls._is_file, lines_file_list)

        config_file_list_output = CM.run_command_check_output(command_args_package_list)
        config_files = config_file_list_output.split('\n')
        config_files = (filter(lambda f: len(f) > 0, config_files))

        for conf_file_path in config_files:
            if cls._is_file(conf_file_path):
                file_info = FileInfo(conf_file_path)
                file_info.mutable = True
                result.append(file_info)

        for file_path in files:
            if cls._is_file(file_path) and file_path not in config_files:
                file_info = FileInfo(file_path)
                result.append(file_info)

        return result

    @classmethod
    def get_files_from_packagefile(cls, file_path):
        """
        Extract all information of a .rpm package.
        - List of all files
        - List of all Configuration-files

        This Method extract all the information in a temporary directory. The Rpm package
        is extracted to the temporary directory, this because the files are needed to compute the File-Hash.

        :param file_pathname: Path to the .rpm package
        :return: Lexicographical sorted List of FileInfo()-Objects (Conffiles and normal Files)
        """
        all_file_info = []

        save_options = create_temp_folder(file_path)

        command_args_file_list = [cls.executable, "--query", "--package", file_path, '-l']
        command_args_conffile_list = [cls.executable, "--query", "--package", file_path, '-c']
        command_args_rpm2cpio = ["rpm2cpio", file_path]
        command_args_cpio = ["cpio", "-id", "--quiet"]

        file_list_output = CM.run_command_check_output(command_args_file_list)
        conffile_list_output = CM.run_command_check_output(command_args_conffile_list)

        normal_files = filter(lambda fp: len(fp) > 0, file_list_output.split('\n'))
        config_files = filter(lambda fp: len(fp) > 0, conffile_list_output.split('\n'))

        rpm2cpio = CM.run_command_popen(command_args_rpm2cpio, stdout=subprocess.PIPE)
        CM.run_command_check_output(command_args_cpio, stdin=rpm2cpio.stdout, working_directory=save_options['save_location'])

        for file_path in config_files:
            temporary_path = save_options['save_location'] + file_path
            if cls._is_file(temporary_path):
                file_info = FileInfo(file_path, actual_path=False)
                file_info.set_actual_path(temporary_path)
                file_info.mutable = True
                all_file_info.append(file_info)

        for file_path in normal_files:
            temporary_path = save_options['save_location'] + file_path
            if cls._is_file(temporary_path) and file_path not in config_files:
                file_info = FileInfo(file_path, actual_path=False)
                file_info.set_actual_path(temporary_path)
                all_file_info.append(file_info)

        return all_file_info

    @classmethod
    def get_packageinfo_from_packagefile(cls, file_path):
        """
        Extract the Package-Name and the Package-Version from the Debian-Package.

        :param file_path: Path to the Rpm-Package
        :return: A PackageInfo()-Object with Package-Version and Package-Name.
        """
        command_args_package_name = [cls.executable, "--query", "--package", "--queryformat", "%{name}", file_path]
        command_args_package_version = [cls.executable, "--query", "--package", "--queryformat", "%{version}", file_path]

        package_name_output = CM.run_command_check_output(command_args_package_name)
        package_version_output = CM.run_command_check_output(command_args_package_version)

        package_info = PackageInfo()
        package_info.package = package_name_output
        package_info.version = package_version_output

        return package_info
