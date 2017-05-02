
import os
import tests.fixtures.mock_data as MockData

class CommandManagerMock(object):

    @staticmethod
    def run_command(command_argumentlist, working_directory=os.getcwd()):
        return True

    @staticmethod
    def run_command_check_output(command_argumentlist, stdin=None, working_directory=os.getcwd()):
        if command_argumentlist == ['rpm', '-qa', '--queryformat', '\t%{name} %{version}-%{release}']:
            return MockData.rpm_query_package_list_output
        if command_argumentlist == ['rpm', '-ql', 'docker']:
            return MockData.rpm_query_file_list
        if command_argumentlist == ['rpm', '-qa', '--queryformat', '%{name}\n', '-c', 'docker']:
            return MockData.rpm_query_conffile_list
        if command_argumentlist == ['rpm', "--query", "--package", "--queryformat", "%{name}", "/tmp/docker.pkg"]:
            return "docker"
        if command_argumentlist == ['rpm', "--query", "--package", "--queryformat", "%{version}", "/tmp/docker.pkg"]:
            return "1.0-5"
        if command_argumentlist == ['dpkg-query','-W', '-f=${Package}\\n${Version}\\n${Status}\\n${conffiles}\\t']:
            return MockData.dpkg_query_package_list_output
        if command_argumentlist == ['dpkg-query', '-L', "docker"]:
            return MockData.dpkg_query_file_list
        if command_argumentlist == ['dpkg-query', '-W', '-f=${conffiles}\\n', "docker"]:
            return MockData.dpkg_query_conffile_list
        if command_argumentlist == ['dpkg' '-f', "/tmp/docker.pkg", 'Package']:
            return "docker"
        if command_argumentlist == ['dpkg' '-f', "/tmp/docker.pkg", 'Version']:
            return "1.0-5"
        else:
            return False

    @staticmethod
    def run_command_popen(command_argumentlist, stdout=None):
        return True
