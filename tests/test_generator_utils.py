# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from swid_generator.package_info import PackageInfo
from swid_generator.generators import utils


def test_valid_unique_id():
    pi = PackageInfo(package='swid_generator', version='0.1.2')
    os_string = 'debian_7.4'
    architecture = 'x86_64'
    unique_id = utils.create_unique_id(pi, os_string, architecture)
    assert unique_id == 'debian_7.4-x86_64-swid_generator-0.1.2'


def test_reserved_unique_id():
    """
    Test a unique ID with a version that contains reserved characters.
    """
    pi = PackageInfo(package='ntp', version="1:4/2?6#p[3]+dfsg-1!ubuntu@3.1$&'()*,;=")
    os_string = 'debian_7.4'
    architecture = 'i686'
    unique_id = utils.create_unique_id(pi, os_string, architecture)
    assert unique_id == 'debian_7.4-i686-ntp-1~4~2~6~p~3~~dfsg-1~ubuntu~3.1~~~~~~~~~'


def test_software_id():
    regid = 'strongswan.org'
    unique_id = 'debian_7.4-x86_64-swid_generator-0.1.2'
    software_id = utils.create_software_id(regid, unique_id)
    assert software_id == 'strongswan.org_debian_7.4-x86_64-swid_generator-0.1.2'


def test_create_hashes():

    file_path = "tests/dumps/package_files/docker.deb"

    expectedsha256hash = "2de78155edc9416debe50b1e9068fc3aad19eb46bc25d2cbc81e313f87d4fecf"
    expectedsha384hash = "55c8ff62968d089814429ef6f8d7df52d66465db0295b14ed5773ad50c4b4b7aeae2abde266a00769406310f5e42ffb1"
    expectedsha512hash = "5251806f42c3b14c90a2071425f101e6d893515b8e47" \
                         "c9d5bcb19099bc52c5d4d1175ddc6f9163d95a8cca952b" \
                         "09986d280bb84c2911939ae51f08e3428884d9"

    result256 = utils.create_sha256_hash(file_path)
    result384 = utils.create_sha384_hash(file_path)
    result512 = utils.create_sha512_hash(file_path)

    assert expectedsha256hash == result256
    assert expectedsha384hash == result384
    assert expectedsha512hash == result512
