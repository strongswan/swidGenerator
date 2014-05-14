# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os.path


class FileInfo(object):
    def __init__(self, path):
        self.location, self.name = os.path.split(path)


class PackageInfo(object):
    def __init__(self, package='', version='', files=None):
        if files is None:
            files = []
        self.package = package
        self.version = version
        self.files = files
