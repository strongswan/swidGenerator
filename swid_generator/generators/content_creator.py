# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os.path
import ntpath

from .utils import create_sha256_hash, create_sha384_hash, create_sha512_hash
from itertools import groupby
from xml.etree import ElementTree as ET


def _add_hashes(file_info, file_tag, hash_algorithms):
    if 'sha256' in hash_algorithms:
        file_tag.set('SHA256:hash', create_sha256_hash(file_info.actual_full_pathname))
    if 'sha384' in hash_algorithms:
        file_tag.set('SHA384:hash', create_sha384_hash(file_info.actual_full_pathname))
    if 'sha512' in hash_algorithms:
        file_tag.set('SHA512:hash', create_sha512_hash(file_info.actual_full_pathname))


def _sort_files(files):
    def _lenfunc(obj):
        return len(obj.full_pathname_splitted)

    def _keyfunc(file, i):
        return file.full_pathname_splitted[i - 1]

    longest_path_length = len(max(files, key=_lenfunc).full_pathname_splitted) - 1

    for file_info in files:
        del file_info.full_pathname_splitted[-1]

        path_length = len(file_info.full_pathname_splitted)
        file_info.full_pathname_splitted.extend([''] * (longest_path_length - path_length))

    for path_length in range(longest_path_length, 0, -1):
        files.sort(key=lambda f, i=path_length: _keyfunc(f, i))
    return files


def create_flat_content_tag(root_element, package_info, hash_algorithms):
    last_full_pathname = ""
    last_directory_tag = ""

    root_element.set('n8060:pathSeparator', '/')
    root_element.set('n8060:envVarPrefix', '$')
    root_element.set('n8060:envVarSuffix', '')

    if len(package_info.files) > 0:
        package_info.files = _sort_files(package_info.files)

    for file_info in package_info.files:

        head, file_name = ntpath.split(file_info.full_pathname)
        root, folder_name = ntpath.split(head)
        if root == '//':
            root = '/'

        full_pathname = root + folder_name

        if last_full_pathname == full_pathname:
            file_tag = ET.SubElement(last_directory_tag, 'File')
            file_tag.set('name', file_name)
        else:
            directory_tag = ET.SubElement(root_element, 'Directory')
            directory_tag.set('root', root)
            directory_tag.set('name', folder_name)
            file_tag = ET.SubElement(directory_tag, 'File')
            file_tag.set('name', file_name)
            last_full_pathname = full_pathname
            last_directory_tag = directory_tag

        if file_info.mutable:
            file_tag.set('n8060:mutable', "true")

        file_tag.set('size', file_info.size)

        _add_hashes(file_info, file_tag, hash_algorithms)

    return root_element


def create_hierarchic_content_tag(root_element, package_info, hash_algorithms):
    root_element.set('n8060:pathSeparator', '/')
    root_element.set('n8060:envVarPrefix', '$')
    root_element.set('n8060:envVarSuffix', '')

    def _file_hierarchy(filelist, depth=0, parent_tag=None):
        def _keyfunc(obj):
            return obj.full_pathname_splitted[depth]

        filelist.sort(key=_keyfunc)

        for head, tail_of_file_iterator in groupby(filelist, _keyfunc):
            sub_files = list()
            for file_info in tail_of_file_iterator:
                if depth + 1 >= len(file_info.full_pathname_splitted):
                    file_tag = ET.SubElement(parent_tag, 'File')
                    file_tag.set('name', file_info.name)
                    if file_info.mutable:
                        file_tag.set('n8060:mutable', "true")
                    file_tag.set('size', file_info.size)
                    if depth == 0:
                        if os.path.isabs(file_info.full_pathname):
                            file_tag.set('root', '/')

                    _add_hashes(file_info, file_tag, hash_algorithms)
                else:
                    sub_files.append(file_info)

            if len(sub_files) > 0:
                sub_tag = ET.SubElement(parent_tag, 'Directory')
                sub_tag.set('name', head)
                if depth == 0:
                    if os.path.isabs(file_info.full_pathname):
                        sub_tag.set('root', '/')
                _file_hierarchy(sub_files, depth=depth + 1, parent_tag=sub_tag)

    _file_hierarchy(list(package_info.files), parent_tag=root_element)

    return root_element
