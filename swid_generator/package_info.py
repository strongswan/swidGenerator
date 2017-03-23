# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os.path


class FileInfo(object):
    def __init__(self, path):
        self.name = (os.path.split(path)[1]).split(' ')[0]
        self.location = os.path.split(path)[0]
        self.mutable = False
        self.fullpathname = (self.location + "/" + self.name).strip()


class PackageInfo(object):
    def __init__(self, package='', version='', files=None, status=None):
        if files is None:
            files = []
        self.package = package
        self.version = version
        self.files = files
        self.status = status
        self.files_structured = []

    def append_file(self, file_info):
        self.files.append(file_info)
