# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from xml.etree import cElementTree as ET

from .utils import create_unique_id, create_software_id, create_system_id
from .utils import create_sha256_hash, create_sha384_hash, create_sha512_hash

import ntpath

ROLE = 'tagCreator'
VERSION_SCHEME = 'alphanumeric'
XMLNS = 'http://standards.iso.org/iso/19770/-2/2015/schema.xsd'
XML_DECLARATION = '<?xml version="1.0" encoding="utf-8"?>'
N8060 = 'http://csrc.nist.gov/schema/swid/2015-extensions/swid-2015-extensions-1.0.xsd'


def _create_payload_tag(package_info, hash_algorithms):
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
            file_tag.set('n8060:mutable', "True")

        file_tag.set('size', file_info.size)

        if 'sha256' in hash_algorithms:
            file_tag.set('SHA256:hash', create_sha256_hash(file_info.actual_full_pathname))
        if 'sha384' in hash_algorithms:
            file_tag.set('SHA384:hash', create_sha384_hash(file_info.actual_full_pathname))
        if 'sha512' in hash_algorithms:
            file_tag.set('SHA512:hash', create_sha512_hash(file_info.actual_full_pathname))

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


def create_software_identity_element(ctx, from_package_file=False):
    """
    This method creates the SoftwareIdentity-Tag for the SWID.
    :param ctx: Information of package and arguments given by User (example: full-flag, regid, etc.)
    :param from_package_file: Flag if the File-List comes from a Package-File or a local installed Package.
    :return: Whole Identification-Tag with all Information given.
    """
    software_identity = ET.Element('SoftwareIdentity')
    software_identity.set('xmlns', XMLNS)
    software_identity.set('xmlns:n8060', N8060)
    software_identity.set('name', ctx['package_info'].package)
    software_identity.set('uniqueId', create_unique_id(ctx['package_info'],
                                                       ctx['environment'].get_os_string(),
                                                       ctx['environment'].get_architecture())
                          )
    software_identity.set('version', ctx['package_info'].version)
    software_identity.set('versionScheme', VERSION_SCHEME)

    entity = ET.SubElement(software_identity, 'Entity')
    entity.set('name', ctx['entity_name'])
    entity.set('regid', ctx['regid'])
    entity.set('role', ROLE)

    if ctx['full']:

        if 'sha256' in ctx['hash_algorithms']:
            software_identity.set('xmlns:SHA256', "http://www.w3.org/2001/04/xmlenc#sha256")
        if 'sha384' in ctx['hash_algorithms']:
            software_identity.set('xmlns:SHA384', "http://www.w3.org/2001/04/xmlenc#sha384")
        if 'sha512' in ctx['hash_algorithms']:
            software_identity.set('xmlns:SHA512', "http://www.w3.org/2001/04/xmlenc#sha512")

        if from_package_file:
            ctx['package_info'].files.extend(ctx['environment'].get_files_from_packagefile(ctx['file_path']))
        else:
            ctx['package_info'].files.extend(ctx['environment'].get_files_for_package(ctx['package_info']))

        payload_tag = _create_payload_tag(ctx['package_info'], ctx['hash_algorithms'])
        software_identity.append(payload_tag)

    return software_identity


def create_swid_tags(environment, entity_name, regid,
                     hash_algorithms='sha256', full=False, matcher=all_matcher, file_path=None):
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
        hash_algorithms(str):
            Comma separated list of the hash algorithms to include in the SWID tag,
        full (bool):
            Whether to include file payload. Default is False.
        matcher (function):
            A function that defines whether to return a tag or not. Default is
            a function that returns ``True`` for all tags.

    Returns:
        A generator object for all available SWID XML strings. The XML strings
        are all bytestrings, using UTF-8 encoding.

    """

    ctx = {
        'regid': regid,
        'environment': environment,
        'entity_name': entity_name,
        'full': full,
        'hash_algorithms': hash_algorithms,
        'file_path': file_path
    }

    if file_path is not None:
        pi = environment.get_packageinfo_from_packagefile(file_path)

        ctx['package_info'] = pi

        software_identity = create_software_identity_element(ctx, from_package_file=True)

        swidtag_flat = ET.tostring(software_identity, encoding='utf-8').replace(b'\n', b'')
        yield XML_DECLARATION.encode('utf-8') + swidtag_flat

    else:

        pkg_info = environment.get_package_list()

        for pi in pkg_info:
            # Check if the software-id of the current package matches the targeted request

            ctx['package_info'] = pi

            if not matcher(ctx):
                continue

            software_identity = create_software_identity_element(ctx)

            swidtag_flat = ET.tostring(software_identity, encoding='utf-8').replace(b'\n', b'')
            yield XML_DECLARATION.encode('utf-8') + swidtag_flat
