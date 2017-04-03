import platform
from functools import partial
from xml.etree import cElementTree as ET

import pytest

from swid_generator.generators import swid_generator
from swid_generator.package_info import PackageInfo
from swid_generator.settings import DEFAULT_REGID, DEFAULT_ENTITY_NAME
from swid_generator.environments.common import CommonEnvironment
from swid_generator.generators.swid_generator import software_id_matcher, package_name_matcher


class FileInfoMock(object):
    def __init__(self, name, location, size, mutable, full_pathname):
        self.name = name
        self.location = location
        self.size = size
        self.mutable = mutable
        self.full_pathname = full_pathname


class TestEnvironment(CommonEnvironment):
    executable = 'asdfasdfa_env'
    os_string = 'SomeTestOS'

    def __init__(self, packages):
        self.packages = packages
        self.installed_states = {
            'install ok installed': True,
            'deinstall ok config-files': False
        }

    def get_package_list(self, include_files=False):
        return filter(self.package_installed, self.packages)

    def package_installed(self, package):
        return self.installed_states.get(package.status, True)

    @staticmethod
    def get_os_string():
        return TestEnvironment.os_string

    @staticmethod
    def get_architecture():
        return 'i686'

    def get_files_for_package(self, package):
        return []


@pytest.fixture
def packages():
    cowsay_file1 = FileInfoMock('cowsay', 'tests/dumps/package_files/cowsay','4421', False, 'tests/dumps/package_files/cowsay/cowsay')
    cowsay_file2 = FileInfoMock('pony-smaller.cow', 'tests/dumps/package_files/cowsay', '305', True, 'tests/dumps/package_files/cowsay/pony-smaller.cow')
    cowsay_file3 = FileInfoMock('copyright.txt', 'tests/dumps/package_files/cowsay/etc', '12854', True, 'tests/dumps/package_files/cowsay/etc/copyright.txt')

    fortune_file1 = FileInfoMock('fortune', 'tests/dumps/package_files/fortune', '1234', False, 'tests/dumps/package_files/fortune/fortune')
    fortune_file2 = FileInfoMock('copyright', 'tests/dumps/package_files/fortune', '3333', False, 'tests/dumps/package_files/fortune/copyright')
    fortune_file3 = FileInfoMock('config.txt', 'tests/dumps/package_files/fortune/usr', '45986', True, 'tests/dumps/package_files/fortune/usr/config.txt')

    openssh_file1 = FileInfoMock('ssh.conf', '/etc/init/', '555', True, '/etc/init/ssh.conf')
    openssh_file2 = FileInfoMock('sshd', '/usr/sbin/', '89484', False, '/usr/sbin/sshd')

    infos = [
        PackageInfo('cowsay', '1.0', [cowsay_file1, cowsay_file2, cowsay_file3], 'install ok installed'),
        PackageInfo('fortune', '2.0', [fortune_file1, fortune_file2, fortune_file3], 'install ok installed'),
        PackageInfo('openssh-server', '7000', [openssh_file1, openssh_file2], 'deinstall ok config-files')
    ]

    return infos


@pytest.fixture
def swid_tag_generator(packages):
    env = TestEnvironment(packages)
    kwargs = {
        'environment': env,
        'entity_name': DEFAULT_ENTITY_NAME,
        'regid': DEFAULT_REGID,
    }
    return partial(swid_generator.create_swid_tags, **kwargs)


def test_package_rc_state(swid_tag_generator):
    output = swid_tag_generator(full=False)
    assert len(list(output)) == 2


def test_non_pretty_output(swid_tag_generator, packages):
    output = swid_tag_generator(full=False)
    for idx, document_string in enumerate(output):
        root = ET.fromstring(document_string)

        #Test Entity tag
        assert root[0].attrib['regid'] == DEFAULT_REGID

        #Test SoftwareIdentity tag attributes
        assert root.attrib['version'] == packages[idx].version
        assert root.attrib['name'] == packages[idx].package
        assert root.attrib['uniqueId'] == '{os_info}-{architecture}-{pi.package}-{pi.version}'.format(
            os_info=TestEnvironment.os_string,
            architecture=TestEnvironment.get_architecture(),
            pi=packages[idx])


def test_full_output(swid_tag_generator, packages):
    output = swid_tag_generator(full=True)
    for document in output:
        root = ET.fromstring(document)
        package_name = root.attrib['name']
        meta_tag = root[1]
        payload = root[2]

        assert meta_tag.attrib['product'] == '{os_info}-{architecture}'.format(
            os_info=TestEnvironment.os_string,architecture=TestEnvironment.get_architecture())

        assert len(payload) == 2

        files = next(p for p in packages if p.package == package_name).files
        for directory_tag in payload:
            directory_fullpath = directory_tag.attrib['root'] + "/" + directory_tag.attrib['name']
            for file_tag in directory_tag:
                test = [f for f in files if f.name == file_tag.attrib['name']
                        and f.location == directory_fullpath]

                assert len(test) == 1
                if test[0].mutable == 'True':
                    assert file_tag.attrib['mutable'] == 'True'
                else:
                    with pytest.raises(KeyError):
                        file_tag.attrib['mutable']
                assert file_tag.attrib['size'] == test[0].size


@pytest.mark.parametrize('package_name,package_version,expected_count', [
    ('cowsay', 1234, 0),
    ('cowsay', '1.0', 1),
    ('non-existent-software-id', 1337, 0)
])
def test_targeted_software_id_test(swid_tag_generator, package_name, package_version, expected_count):
    software_id = '{regid}_{os_info}-{architecture}-{package_name}-{package_version}' \
        .format(regid=DEFAULT_REGID,
                package_name=package_name,
                package_version=package_version,
                os_info=TestEnvironment.os_string,
                architecture=TestEnvironment.get_architecture())

    matcher = partial(software_id_matcher, value=software_id)
    output = list(swid_tag_generator(full=False, matcher=matcher))
    assert len(output) == expected_count


@pytest.mark.parametrize('package_name,expected', [
    ('cowsay', 1),
    ('whiptail', 0)
])
def test_targeted_package_name_test(swid_tag_generator, package_name, expected):
    matcher = partial(package_name_matcher, value=package_name)
    output = list(swid_tag_generator(full=False, matcher=matcher))
    assert len(output) == expected
