# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals


class AutodetectionError(RuntimeError):
    """
    Raised when autodetecting the environment fails.
    """
    pass


class EnvironmentNotInstalledError(RuntimeError):
    """
    Raised when a manually specified environment cannot be found on the system.
    """
    pass
