from __future__ import print_function
import subprocess
import sys

SOURCE_CODE_FOLDER = "/Users/dada/Desktop/HSR/BA/SourceCode/swidGenerator/"
WORKING_DIRECTORY_DOCKER = "/home/swid"

FOLDER_MOUNT = ':'.join((SOURCE_CODE_FOLDER, WORKING_DIRECTORY_DOCKER))

DOCKER_IMAGE_NAMES = [
    {"environment": "dpkg", "image": "ubu"},
    {"environment": "rpm", "image": "rdh"},
    {"environment": "pacman", "image": "arl"},
]

CMD_ARGS_DOCKER = ["docker", "run", "-i", "--rm", "-v", FOLDER_MOUNT]


def main(arguments):

    print("Start all Tests with own Environment")

    for _, env_image in enumerate(DOCKER_IMAGE_NAMES):

        if env_image['environment'] in arguments:
            title = "Tests for Environment with Image: " + env_image['environment']
            underline_title = '=' * len(title)
            print(title)
            print(underline_title)
            cmd_args_specific_env = CMD_ARGS_DOCKER
            cmd_args_specific_env.append(env_image['image'])
            for path in execute_command(cmd_args_specific_env):
                print(path, end="")
            cmd_args_specific_env.pop()


def execute_command(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


if __name__ == '__main__':
    main(sys.argv)
