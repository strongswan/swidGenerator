# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from xml.etree import cElementTree as ET


ROLE = 'tagcreator'
VERSION_SCHEME = 'alphanumeric'
XMLNS = 'http://standards.iso.org/iso/19770/-2/2014/schema.xsd'
XML_DECLARATION = '<?xml version="1.0" encoding="utf-8"?>'


def _create_payload_tag(package_info):
    payload = ET.Element('Payload')
    for file_info in package_info.files:
        file_element = ET.SubElement(payload, 'File')
        file_element.set('name', file_info.name)
        file_element.set('location', file_info.location)

    return payload


def _create_unique_id(os_info, package_info, architecture):
    unique_id_format = '{os_info}-{architecture}-{pi.package}-{pi.version}'
    return unique_id_format.format(os_info=os_info,
                                   pi=package_info,
                                   architecture=architecture)


def _create_software_id(os_info, package_info, regid, architecture):
    return '{regid}_{uniqueID}'.format(
        regid=regid, uniqueID=_create_unique_id(os_info, package_info, architecture))


def all_matcher(ctx):
    return True


def package_name_matcher(ctx, value):
    return ctx['package_info'].package == value


def software_id_matcher(ctx, value):
    software_id = _create_software_id(
        ctx['environment'].get_os_string(),
        ctx['package_info'],
        ctx['regid'],
        ctx['environment'].get_architecture())

    return software_id == value


def create_swid_tags(environment, entity_name, regid, full=False, matcher=all_matcher):
    """
    Return SWID tags as utf8-encoded xml bytestrings for all available
    packages.

    Args:
        environment (swid_generator.environment.CommonEnvironment):
            The package management environment.
        entity_name (str):
            The SWID tag entity name.
        regid (str):
            The SWID tag regid.
        full (bool):
            Whether to include file payload. Default is False.
        matcher (function):
            A function that defines whether to return a tag or not. Default is
            a function that returns ``True`` for all tags.

    Returns:
        A generator object for all available SWID XML strings. The XML strings
        are all bytestrings, using UTF-8 encoding.

    """
    os_info = environment.get_os_string()
    pkg_info = environment.get_list()

    for pi in pkg_info:

        ctx = {
            'regid': regid,
            'environment': environment,
            'package_info': pi
        }

        # Check if the software-id of the current package matches the targeted request
        if not matcher(ctx):
            continue

        software_identity = ET.Element('SoftwareIdentity')
        software_identity.set('xmlns', XMLNS)
        software_identity.set('name', pi.package)
        software_identity.set('uniqueId', _create_unique_id(os_info, pi, environment.get_architecture()))

        software_identity.set('version', pi.version)
        software_identity.set('versionScheme', VERSION_SCHEME)

        entity = ET.SubElement(software_identity, 'Entity')
        entity.set('name', entity_name)
        entity.set('regid', regid)
        entity.set('role', ROLE)

        if full:
            pi.files = environment.get_files_for_package(pi.package)
            payload_tag = _create_payload_tag(pi)
            software_identity.append(payload_tag)

        swidtag_flat = ET.tostring(software_identity, encoding='utf-8', method='xml').replace(b'\n', b'')
        yield XML_DECLARATION.encode('utf-8') + swidtag_flat
