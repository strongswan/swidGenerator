# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os.path


class FileInfo(object):
    def __init__(self, path):
        # Split is because of md5 Hash after file-name Information.
        self.name = (os.path.split(path)[1]).split(' ')[0]
        self.location = (os.path.split(path)[0]).strip()
        self.mutable = False
        self.full_pathname = '/'.join((self.location, self.name))


class PackageInfo(object):
    def __init__(self, package='', version='', files=None, status=None):
        if files is None:
            files = []
        self.package = package
        self.version = version
        self.files = files
        self.status = status
        self.files_structured = []
