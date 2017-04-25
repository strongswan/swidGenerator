from __future__ import print_function, division, absolute_import, unicode_literals
from tests.integration_test_runner_configuration import IntegrationTestRunnerConfiguration
import subprocess
import sys


def _execute_command(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        # On error fail Build-process. Break with exit of program.
        raise sys.exit(1)


class IntegrationTestRunner(object):

    tox_command_args = ['tox', "-r", "-c", "tox_integration.ini", "--", "-x"]
    docker_command_args = ["docker", "run", "-i", "--rm", "-v"]

    def __init__(self, arguments, test_configuration):
        self.test_configuration = test_configuration
        self.source_code_folder_path = arguments[1]
        self.folder_mount = ':'.join((self.source_code_folder_path, self.test_configuration.working_directory_docker))
        self.docker_command_args.append(self.folder_mount)
        self.selected_environments = arguments[2:]

    def run_main(self):

        print("Start all Tests with own Environment")

        for _, env_image in enumerate(self.test_configuration.docker_image_list):

            if env_image['environment'] in self.selected_environments:

                title = "Tests for Environment with Image: " + env_image['environment']
                underline_title = '=' * len(title)
                print(title)
                print(underline_title)

                cmd_args_specific_env = self.docker_command_args[:]
                cmd_args_specific_env.append(env_image['image'])

                for test_file in self.test_configuration.test_files:
                    cmd_args_specific_env_tox = self.tox_command_args[:]
                    cmd_args_specific_env_tox.append(test_file)
                    cmd_args_specific_env.extend(cmd_args_specific_env_tox)

                    print(cmd_args_specific_env)

                    for path in _execute_command(cmd_args_specific_env):
                        print(path, end="")
                    cmd_args_specific_env.pop()

if __name__ == '__main__':

    working_directory_docker = "/home/swid"

    docker_image_names = [
        {"environment": "dpkg", "image": "davidedegiorgio/swidgenerator-dockerimages:debian"},
        {"environment": "rpm", "image": "davidedegiorgio/swidgenerator-dockerimages:redhat"},
        {"environment": "pacman", "image": "davidedegiorgio/swidgenerator-dockerimages:archlinux"}
    ]

    test_files = ['tests/integration_test.py']

    integration_test_configuration = IntegrationTestRunnerConfiguration(docker_image_list=docker_image_names,
                                                                        test_files=test_files,
                                                                        working_directory_docker=working_directory_docker)

    integration_test = IntegrationTestRunner(sys.argv, integration_test_configuration)
    integration_test.run_main()

