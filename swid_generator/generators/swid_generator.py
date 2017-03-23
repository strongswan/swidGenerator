# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from xml.etree import cElementTree as ET

from .utils import create_unique_id, create_software_id

import ntpath


ROLE = 'tagCreator'
VERSION_SCHEME = 'alphanumeric'
XMLNS = 'http://standards.iso.org/iso/19770/-2/2015/schema.xsd'
XML_DECLARATION = '<?xml version="1.0" encoding="utf-8"?>'
N8060 = 'http://csrc.nist.gov/schema/swid/2015-extensions/swid-2015-extensions-1.0.xsd'


def _create_payload_tag(package_info):
    payload = ET.Element('Payload')
    last_full_pathname = ""
    last_directory_tag = ""

    for file_info in package_info.files:

        head, file_name = ntpath.split(file_info.full_pathname)
        root, folder_name = ntpath.split(head)

        full_pathname = root + folder_name

        if last_full_pathname == full_pathname:
            file_tag = ET.SubElement(last_directory_tag, 'File')
            file_tag.set('name', file_name)
        else:
            directory_tag = ET.SubElement(payload, 'Directory')
            directory_tag.set('root', root)
            directory_tag.set('name', folder_name)
            file_tag = ET.SubElement(directory_tag, 'File')
            file_tag.set('name', file_name)
            last_full_pathname = full_pathname
            last_directory_tag = directory_tag

        if file_info.mutable:
            file_tag.set('mutable', "True")

    return payload


def all_matcher(ctx):
    return True


def package_name_matcher(ctx, value):
    return ctx['package_info'].package == value


def software_id_matcher(ctx, value):
    env = ctx['environment']
    os_string = env.get_os_string()
    architecture = env.get_architecture()
    unique_id = create_unique_id(ctx['package_info'], os_string, architecture)
    software_id = create_software_id(ctx['regid'], unique_id)
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
    os_string = environment.get_os_string()
    pkg_info = environment.get_package_list()
    architecture = environment.get_architecture()

    for pi in pkg_info:

        ctx = {
            'regid': regid,
            'environment': environment,
            'package_info': pi
        }

        # Check if the software-id of the current package matches the targeted request
        if not matcher(ctx):
            continue

        # Header SoftwareIdentity
        software_identity = ET.Element('SoftwareIdentity')
        software_identity.set('xmlns', XMLNS)
        software_identity.set('n8060', N8060)
        software_identity.set('name', pi.package)
        software_identity.set('uniqueId', create_unique_id(pi, os_string, architecture))
        software_identity.set('version', pi.version)
        software_identity.set('versionScheme', VERSION_SCHEME)

        # SubElement Entity
        entity = ET.SubElement(software_identity, 'Entity')
        entity.set('name', entity_name)
        entity.set('regid', regid)
        entity.set('role', ROLE)

        if full:
            environment.get_files_for_package(pi)
            # pi.files.extend(environment.get_files_for_package(pi))
            payload_tag = _create_payload_tag(pi)
            software_identity.append(payload_tag)

        swidtag_flat = ET.tostring(software_identity, encoding='utf-8').replace(b'\n', b'')
        yield XML_DECLARATION.encode('utf-8') + swidtag_flat
