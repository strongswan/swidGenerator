
class IntegrationTestRunnerConfiguration(object):

    def __init__(self, working_directory_docker, docker_image_list, test_files):
        self.working_directory_docker = working_directory_docker
        self.docker_image_list = docker_image_list
        self.test_files = test_files
