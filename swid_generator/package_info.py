# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os.path


class FileInfo(object):
    def __init__(self, path, actual_path=True):
        self.name = (os.path.split(path)[1]).strip()
        self.location = (os.path.split(path)[0]).strip()
        self.mutable = False
        self.full_pathname = '/'.join((self.location, self.name))

        splitted_location = self.full_pathname.split('/')
        self.full_pathname_splitted = splitted_location[1:]

        if actual_path:
            self.actual_full_pathname = self.full_pathname
            self.size = str(os.path.getsize(self.full_pathname))
        else:
            self.actual_full_pathname = ""

    def set_actual_path(self, file_path):
        self.actual_full_pathname = file_path.encode('utf-8')
        self.size = str(os.path.getsize(file_path))


class PackageInfo(object):
    def __init__(self, package='', version='', files=None, status=None):
        if files is None:
            files = []
        self.package = package
        self.version = version
        self.files = files
        self.status = status
