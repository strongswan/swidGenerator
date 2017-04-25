from __future__ import print_function
import subprocess
import sys, os


def _execute_command(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


class IntegrationTestRunner(object):

    WORKING_DIRECTORY_DOCKER = "/home/swid"
    DOCKER_IMAGE_NAMES = [
        {"environment": "dpkg", "image": "davidedegiorgio/swidgenerator:latest"},
        {"environment": "rpm", "image": "rdh"},
        {"environment": "pacman", "image": "arl"}
    ]
    TEST_FILES = ['tests/IntegrationTest.py']
    CMD_TO_EXECUTE = ['tox', "-r", "-c", "tox_integration.ini", "--", "-x"]

    def __init__(self, arguments):
        self.SOURCE_CODE_FOLDER_PATH = arguments[1]
        self.FOLDER_MOUNT = ':'.join((self.SOURCE_CODE_FOLDER_PATH, self.WORKING_DIRECTORY_DOCKER))
        self.CMD_ARGS_DOCKER = ["docker", "run", "-i", "--rm", "-v", self.FOLDER_MOUNT]
        self.ELECTED_ENVIRONMENTS = arguments[2:]

    def run_main(self):

        print("Start all Tests with own Environment")
        print()

        for _, env_image in enumerate(self.DOCKER_IMAGE_NAMES):

            if env_image['environment'] in self.ELECTED_ENVIRONMENTS:

                title = "Tests for Environment with Image: " + env_image['environment']
                underline_title = '=' * len(title)
                print(title)
                print(underline_title)

                cmd_args_specific_env = self.CMD_ARGS_DOCKER
                cmd_args_specific_env.append(env_image['image'])

                for test_file in self.TEST_FILES:

                    self.CMD_TO_EXECUTE.append(test_file)
                    cmd_args_specific_env.extend(self.CMD_TO_EXECUTE)
                    print(cmd_args_specific_env)

                    for path in _execute_command(cmd_args_specific_env):
                        print(path, end="")
                    cmd_args_specific_env.pop()

                cmd_args_specific_env.pop()
                cmd_args_specific_env.pop()
                cmd_args_specific_env.pop()
                cmd_args_specific_env.pop()


if __name__ == '__main__':
    integration_test = IntegrationTestRunner(sys.argv)
    integration_test.run_main()

