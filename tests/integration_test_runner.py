# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import subprocess
import sys


class IntegrationTestRunner(object):
    """
    Class to run the integration tests on docker-containers.
    The run_main method, builds the docker-command for each environment and Python version and starts a subprocess.

    """

    # Command separated with commas because of split in TOX_FILES and TOXENV variable
    docker_command = "docker,run,-i,--rm,-e,TOX_TEST_FILES={TOX_FILES},-e,TOXENV={TOXENV},-v,{FOLDER_MOUNT},{DOCKER_IMAGE_NAME}"

    def __init__(self, arguments, test_configuration):
        self.test_configuration = test_configuration
        self.source_code_folder_path = arguments[1]
        self.python_version = arguments[2]
        self.selected_environments = arguments[3:]

    def run_main(self):

        for _, env_image in enumerate(self.test_configuration.docker_image_list):

            if env_image['environment'] in self.selected_environments:

                args = {
                    "TOXENV": self.python_version,
                    "TOX_FILES": self._compose_test_files(self.test_configuration.test_files),
                    "FOLDER_MOUNT": ':'.join((self.source_code_folder_path, self.test_configuration.working_directory_docker)),
                    "DOCKER_IMAGE_NAME": env_image['image']
                }

                docker_command_args = self.docker_command.format(**args).split(',')

                print(docker_command_args)

                title = "Tests for Environment with Image: " + env_image['environment']
                underline_title = '=' * len(title)

                print(title)
                print(underline_title)

                for line in self._execute_command(docker_command_args):
                    print(line, end="")

    @staticmethod
    def _execute_command(cmd):
        """
        Executes command and yields the output-line from the command.
        If a the command returns a retrun_code the integration-test fails.
        :param cmd: Command-Args as array.
        :return: Output of the command.
        """
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            sys.exit(return_code)

    @staticmethod
    def _compose_test_files(testing_files):
        """
        Compose the testing files defined in IntegrationTestRunnerConfiguration.
        The testing_files is an array of paths, which must be converted to a string of following format:
        "tests/integration_test.py tests/integration_test_2.py"
        :param testing_files: Array of Strings
        :return: String of paths.
        """
        result = ""
        for file_name in testing_files:
            result += " " + file_name
        return result.lstrip()


class IntegrationTestRunnerConfiguration(object):
    """
    Configuration Wrapper for the IntegrationTestRunner.
    """
    def __init__(self, working_dir_docker, docker_image_list, testing_files):
        self.working_directory_docker = working_dir_docker
        self.docker_image_list = docker_image_list
        self.test_files = testing_files


if __name__ == '__main__':

    working_directory_docker = "/home/swid"

    # Define environment names and images
    docker_image_names = [
        {"environment": "dpkg", "image": "strongswan/swidgenerator-dockerimages:debian"},
        {"environment": "rpm", "image": "strongswan/swidgenerator-dockerimages:fedora"},
        {"environment": "pacman", "image": "strongswan/swidgenerator-dockerimages:archlinux"}
    ]

    # Relative paths to testing files in 'working_directory_docker'.
    # Multiple Files can be appended.
    test_files = ['tests/integration_test.py']

    # Define Configuration for IntegrationTestRunner
    integration_test_configuration = IntegrationTestRunnerConfiguration(working_directory_docker, docker_image_names, test_files)

    # Run
    integration_test = IntegrationTestRunner(sys.argv, integration_test_configuration)
    integration_test.run_main()
