import os


def read_file(file_path):
    print(os.getcwd())
    with open(file_path) as dump:
        data = dump.read()
    return data

# RpmEnvironment
rpm_query_package_list_output = read_file("tests/dumps/console_output/rpm_package_query.txt")
rpm_query_file_list = read_file("tests/dumps/console_output/rpm_docker_file_list.txt")
rpm_query_conffile_list = read_file("tests/dumps/console_output/rpm_docker_conffile_list.txt")
rpm_query_packageinfo_name = read_file("tests/dumps/console_output/rpm_docker_package_name.txt")
rpm_query_packageinfo_version = read_file("tests/dumps/console_output/rpm_docker_package_version.txt")