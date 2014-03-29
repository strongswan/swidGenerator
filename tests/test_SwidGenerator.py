import platform
from functools import partial
from xml.etree import cElementTree as ET

import pytest

from swid_generator.generators import swid_generator
from swid_generator.package_info import PackageInfo
from swid_generator.settings import DEFAULT_REGID, DEFAULT_ENTITY_NAME
from swid_generator.environments.common import CommonEnvironment


class FileInfoMock(object):
    def __init__(self, name, location, size):
        self.name = name
        self.location = location
        self.size = size


class TestEnvironment(CommonEnvironment):
    os_string = 'SomeTestOS'

    def __init__(self, packages):
        self.packages = packages
        self.installed_states = {
            'install ok installed': True,
            'deinstall ok config-files': False
        }

    def get_list(self, include_files=False):
        return filter(self.is_installed, self.packages)

    @staticmethod
    def get_os_string():
        return TestEnvironment.os_string

    def is_installed(self, package):
        return self.installed_states.get(package.status, True)

    @staticmethod
    def architecture():
        return platform.machine()

    def get_files_for_package(self, package_name):
        for pi in self.packages:
            if pi.package == package_name:
                return pi.files



@pytest.fixture
def packages():
    cowsay_file1 = FileInfoMock('/usr/games', 'cowsay', 4421)
    cowsay_file2 = FileInfoMock('/usr/share/cowsay/cows', 'pony-smaller.cow', 305)

    fortune_file1 = FileInfoMock('/usr/games', 'fortune', 1234)
    fortune_file2 = FileInfoMock('/usr/share/doc/fortune-mod', 'copyright', 3333)

    openssh_file1 = FileInfoMock('/etc/init/', 'ssh.conf', 555)
    openssh_file2 = FileInfoMock('/usr/sbin/', 'sshd', 89484)

    return [
        PackageInfo('cowsay', '1.0', 'install ok installed', [cowsay_file1, cowsay_file2]),
        PackageInfo('fortune', '2.0', 'install ok installed', [fortune_file1, fortune_file2]),
        PackageInfo('openssh-server', '7000', 'deinstall ok config-files', [openssh_file1, openssh_file2])
    ]


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
            architecture=TestEnvironment.architecture(),
            pi=packages[idx])


def test_full_output(swid_tag_generator, packages):
    output = swid_tag_generator(full=True)
    for document in output:
        root = ET.fromstring(document)
        package_name = root.attrib['name']
        payload = root[1]
        assert len(payload) == 2

        files = filter(lambda p: p.package == package_name, packages)[0].files
        for file_tag in payload:
            assert file_tag.attrib['name'] in [f.name for f in files]


def test_targeted_request(swid_tag_generator, packages):
    target = '{regid}_{os_info}-{architecture}-{pi.package}-{pi.version}' \
        .format(regid=DEFAULT_REGID,
                os_info=TestEnvironment.os_string,
                pi=packages[0],
                architecture=TestEnvironment.architecture())
    output = list(swid_tag_generator(full=False, target=target))
    print output[0]
    assert len(output) == 1
    assert 'cowsay' in output[0]