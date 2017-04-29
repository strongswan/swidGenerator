from __future__ import print_function, division, absolute_import, unicode_literals
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


def _compose_test_files(test_files):
    result = ""
    for file_name in test_files:
        result += " " + '/'.join(("tests", file_name))
    return result.lstrip()


class IntegrationTestRunner(object):

    # Command separated with commas because of split in docker_command_args variable and ENV variable composition
    docker_command = "docker,run,-i,--rm,-e,TOX_TEST_FILES={TOX_FILES},-v,{FOLDER_MOUNT},{DOCKER_IMAGE_NAME}"

    def __init__(self, arguments, test_configuration):
        self.test_configuration = test_configuration
        self.source_code_folder_path = arguments[1]
        self.selected_environments = arguments[2:]

    def run_main(self):

        for _, env_image in enumerate(self.test_configuration.docker_image_list):

            if env_image['environment'] in self.selected_environments:

                args = {
                    "TOX_FILES": _compose_test_files(self.test_configuration.test_files),
                    "FOLDER_MOUNT": ':'.join((self.source_code_folder_path, self.test_configuration.working_directory_docker)),
                    "DOCKER_IMAGE_NAME": env_image['image']
                }

                docker_command_args = self.docker_command.format(**args).split(',')

                title = "Tests for Environment with Image: " + env_image['environment']
                underline_title = '=' * len(title)
                print(title)
                print(underline_title)

                for path in _execute_command(docker_command_args):
                    print(path, end="")


class IntegrationTestRunnerConfiguration(object):
    def __init__(self, working_dir_docker, docker_image_list, testing_files):
        self.working_directory_docker = working_dir_docker
        self.docker_image_list = docker_image_list
        self.test_files = testing_files


if __name__ == '__main__':

    working_directory_docker = "/home/swid"

    docker_image_names = [
        {"environment": "dpkg", "image": "davidedegiorgio/swidgenerator-dockerimages:debian"},
        {"environment": "rpm", "image": "davidedegiorgio/swidgenerator-dockerimages:redhat"},
        {"environment": "pacman", "image": "davidedegiorgio/swidgenerator-dockerimages:archlinux"}
    ]


    # Relative names of Test-files in working_directory_docker/tests. Multiple Files can be appended.
    test_files = ['integration_test.py']

    integration_test_configuration = IntegrationTestRunnerConfiguration(docker_image_list=docker_image_names,
                                                                        testing_files=test_files,
                                                                        working_dir_docker=working_directory_docker)

    integration_test = IntegrationTestRunner(sys.argv, integration_test_configuration)
    integration_test.run_main()
