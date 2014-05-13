# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from xml.etree import cElementTree as ET

from tests.fixtures.rpm_environment import get_swid_by_name, rpm_document_strings, \
    rpm_networkmanager_generated, rpm_networkmanager_template, rpm_environment, common_environment


def test_yum_num_of_packages(rpm_document_strings):
    assert len(list(rpm_document_strings)) == 293


def test_networkmanager_softwareidentity_tag(rpm_networkmanager_generated, rpm_networkmanager_template):
    xml = rpm_networkmanager_generated

    for key in xml.attrib.keys():
        assert xml.attrib[key] == rpm_networkmanager_template.attrib[key]


def test_networkmanager_entity_tag(rpm_networkmanager_generated, rpm_networkmanager_template):
    generated_entity = rpm_networkmanager_generated[0]
    entity_tag = rpm_networkmanager_template[0]
    print(ET.tostring(entity_tag))

    for key in generated_entity.attrib.keys():
        assert generated_entity.attrib[key] == entity_tag.attrib[key]


def test_get_by_name(rpm_document_strings):
    network_manager_swid = get_swid_by_name(rpm_document_strings, 'NetworkManager')
    assert 'NetworkManager' in ET.tostring(network_manager_swid, encoding='utf8').decode('utf8')
