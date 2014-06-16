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
    regid = 'regid.2004-03.org.strongswan'
    unique_id = 'debian_7.4-x86_64-swid_generator-0.1.2'
    software_id = utils.create_software_id(regid, unique_id)
    assert software_id == 'regid.2004-03.org.strongswan_debian_7.4-x86_64-swid_generator-0.1.2'
