# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import subprocess

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
    CONFFILE_FILE_NAME = 'conffiles'
    CONTROL_ARCHIVE = 'control.tar.gz'

    @classmethod
    def get_package_list(cls):
        """
        Get list of installed packages.

        Returns:
            List of ``PackageInfo`` instances.

        """

        command_args = [cls.executable, '-qa', '--queryformat', '\t%{name} %{version}-%{release}', '-c']
        data = subprocess.check_output(command_args)
        if isinstance(data, bytes):  # convert to unicode
            data = data.decode('utf-8')

        line_list = data.split('\t')
        result = []

        for line in line_list:
            split_line = line.replace('\n', " ").split()
            if len(split_line) >= 2:
                package_info = PackageInfo()
                package_info.package = split_line[0]
                package_info.version = split_line[1]

                # if Config-Files exists
                if len(split_line) >= 3:
                    config_files = []
                    for file_path in split_line[2:len(split_line)]:
                        if cls._is_file(file_path):
                            file_info = FileInfo(file_path)
                            file_info.mutable = True
                            config_files.append(file_info)

                    package_info.files.extend(config_files)

                result.append(package_info)

        return result

    @classmethod
    def get_files_for_package(cls, package_info):
        command_args = [cls.executable, '-ql', package_info.package]
        data = subprocess.check_output(command_args)
        if isinstance(data, bytes):  # convert to unicode
            data = data.decode('utf-8')
        lines = data.rstrip().split('\n')
        files = filter(cls._is_file, lines)

        result_list = []

        for path in files:
            if not any(file_info.full_pathname.strip() == path for file_info in package_info.files):
                result_list.append(FileInfo(path))

        return result_list

    @classmethod
    def get_files_from_packagefile(cls, file_path):

        def _run_info_query_command(file_type):
            command_args = [cls.executable, "--query", "--package", file_path, file_type, file_path]
            output = subprocess.check_output(command_args)
            if isinstance(output, bytes):
                output = output.decode('utf-8')

            return output

        all_file_info = []
        normal_files = filter(lambda fp: len(fp) > 0, _run_info_query_command("-l").split('\n'))
        config_files = filter(lambda fp: len(fp) > 0, _run_info_query_command("-c").split('\n'))

        save_options = cls._create_temp_folder(file_path)

        # rpm2cpio zsh-5.1.1-4.fc23.x86_64.rpm | cpio -id --quiet

        """
            ps = subprocess.Popen(('ps', '-A'), stdout=subprocess.PIPE)
            output = subprocess.check_output(('grep', 'process_name'), stdin=ps.stdout)
            ps.wait()
        """

        rpm2cpio = subprocess.Popen(["rpm2cpio", file_path], stdout=subprocess.PIPE)
        output = subprocess.check_output(["cpio", "-id", "--quiet"], stdin=rpm2cpio.stdout)

        print(output)


        for file_path in normal_files:
            if cls._is_file(file_path[1:len(file_path)]):
                file_info = FileInfo(file_path)
                all_file_info.append(file_info)

        for file_path in config_files:
            if cls._is_file(file_path):
                file_info = FileInfo(file_path)
                file_info.mutable = True
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
