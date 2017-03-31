# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os.path


class FileInfo(object):
    def __init__(self, path):
        self.name = (os.path.split(path)[1]).strip()
        self.location = (os.path.split(path)[0]).strip()
        self.mutable = False
        self.full_pathname = '/'.join((self.location, self.name))
        self.size = str(os.path.getsize(self.full_pathname))


class PackageInfo(object):
    def __init__(self, package='', version='', files=None, status=None):
        if files is None:
            files = []
        self.package = package
        self.version = version
        self.files = files
        self.status = status
