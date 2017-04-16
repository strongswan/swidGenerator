# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import subprocess

from .common import CommonEnvironment
from ..package_info import PackageInfo, FileInfo
from .command_manager import CommandManager


class RpmEnvironment(CommonEnvironment):
    """
    Environment class for distributions using RPM as package manager (e.g.
    Fedora, Red Hat or OpenSUSE).

    The packages are retrieved from the database directly using the ``rpm``
    command.

    """
    executable = 'rpm'
    CONFFILE_FILE_NAME = 'conffiles'
    CONTROL_ARCHIVE = 'control.tar.gz'

    @classmethod
    def get_package_list(cls):
        """
        Get list of installed packages.

        Returns:
            List of ``PackageInfo`` instances.

        """

        command_args_package_list = [cls.executable, '-qa', '--queryformat', '\t%{name} %{version}-%{release}']
        package_list_output = CommandManager.run_command_check_output(command_args_package_list)

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

        result = []

        command_args_file_list = [cls.executable, '-ql', package_info.package]
        file_list_output = CommandManager.run_command_check_output(command_args_file_list)
        lines_file_list = file_list_output.rstrip().split('\n')
        files = filter(cls._is_file, lines_file_list)

        command_args_package_list = [cls.executable, '-qa', '--queryformat', '%{name}\n', '-c', package_info.package]
        config_file_list_output = CommandManager.run_command_check_output(command_args_package_list)
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

        def _run_info_query_command(file_type):
            command_args = [cls.executable, "--query", "--package", file_path, file_type]
            output = subprocess.check_output(command_args)
            if isinstance(output, bytes):
                output = output.decode('utf-8')

            return output

        all_file_info = []

        normal_files = filter(lambda fp: len(fp) > 0, _run_info_query_command("-l").split('\n'))
        config_files = filter(lambda fp: len(fp) > 0, _run_info_query_command("-c").split('\n'))

        save_options = cls._create_temp_folder(file_path)

        rpm2cpio = subprocess.Popen(["rpm2cpio", file_path], stdout=subprocess.PIPE)
        subprocess.check_output(["cpio", "-id", "--quiet"], stdin=rpm2cpio.stdout, cwd=save_options[
            'save_location'])

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

        def _run_info_query_command(field):
            command_args = [cls.executable, "--query", "--package", "--queryformat", "%{" + field + "}",
                            file_path]
            output = subprocess.check_output(command_args)
            if isinstance(output, bytes):
                output = output.decode('utf-8')
            return output

        package_info = PackageInfo()
        package_info.package = _run_info_query_command("name")
        package_info.version = _run_info_query_command("version")

        return package_info
