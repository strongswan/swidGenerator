
def _read_file(file_path):
    with open(file_path) as dump:
        data = dump.read()
    return data

# RpmEnvironment
rpm_query_package_list_output = _read_file("tests/dumps/console_output/rpm_package_query.txt")
rpm_query_file_list = _read_file("tests/dumps/console_output/rpm_file_list.txt")
rpm_query_conffile_list = _read_file("tests/dumps/console_output/rpm_conffile_list.txt")

# DpkgEnvironment
dpkg_query_package_list_output = _read_file("tests/dumps/console_output/dpkg_package_query.txt")
dpkg_query_file_list = _read_file("tests/dumps/console_output/dpkg_file_list.txt")
dpkg_query_conffile_list = _read_file("tests/dumps/console_output/dpkg_conffile_list.txt")
dpkg_query_file_list_package = _read_file("tests/dumps/console_output/dpkg_file_list_package.txt")

#PacmanEnvironment
pacman_query_package_list_output = _read_file("tests/dumps/console_output/pacman_package_query.txt")
pacman_query_file_list = _read_file("tests/dumps/console_output/pacman_file_list.txt")
pacman_query_file_list_package = _read_file("tests/dumps/console_output/pacman_file_list_package.txt")
pacman_query_conffile_list = _read_file("tests/dumps/console_output/rpm_conffile_list.txt")