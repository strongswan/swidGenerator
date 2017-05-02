import os


def _read_file(file_path):
    print(os.getcwd())
    with open(file_path) as dump:
        data = dump.read()
    return data

# RpmEnvironment
rpm_query_package_list_output = _read_file("tests/dumps/console_output/rpm_package_query.txt")
rpm_query_file_list = _read_file("tests/dumps/console_output/rpm_docker_file_list.txt")
rpm_query_conffile_list = _read_file("tests/dumps/console_output/rpm_docker_conffile_list.txt")

# DpkgEnvironment
dpkg_query_package_list_output = _read_file("tests/dumps/console_output/dpkg_package_query.txt")
dpkg_query_file_list = _read_file("tests/dumps/console_output/dpkg_docker_file_list.txt")
dpkg_query_conffile_list = _read_file("tests/dumps/console_output/dpkg_docker_conffile_list.txt")


