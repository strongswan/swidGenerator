
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
            return MockData.rpm_query_packageinfo_name
        if command_argumentlist == ['rpm', "--query", "--package", "--queryformat", "%{version}", "/tmp/docker.pkg"]:
            return MockData.rpm_query_packageinfo_version
        else:
            return False

    @staticmethod
    def run_command_popen(command_argumentlist, stdout=None):
        return True
