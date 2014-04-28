# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import platform


class CommonEnvironment(object):
    executable = None

    @staticmethod
    def get_architecture():
        #returns '64bit' or '32bit'
        return platform.machine()

    @staticmethod
    def get_os_string():
        dist = platform.dist()
        return dist[0] + '_' + dist[1]