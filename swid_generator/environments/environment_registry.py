# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from ..exceptions import AutodetectionError, EnvironmentNotInstalledError


class EnvironmentRegistry(object):
    def __init__(self):
        self.environments = {}

    def _autodetect_env(self):
        """
        Detect the used package manager by searching for a given executable in
        the path. Return a class representing the package manager environment
        or ``None`` if autodetection fails.
        """
        for _, environment_class in self.environments.items():
            if environment_class.is_installed():
                return environment_class

    def get_environment_strings(self):
        """
        Return the registered environments.

        Returns:
            String describing environment (e.g 'rpm', 'dpkg')

        """
        return ['auto'] + sorted(self.environments.keys())

    def register(self, environment_name, environment_class):
        """
        Register an environment class.

        Args:
            environment_name:
                The name to be assigned to this environment. This should be
                short and all-lowercase, e.g. ``dpkg`` or ``rpm``.
            environment_class:
                The environment class to register. This should be a reference
                to a class, not to an instance.

        """
        self.environments[environment_name] = environment_class()

    def get_environment(self, environment_string):
        """
        Try to get the environment class for the given environment string.

        Args:
            environment_string (str):
                The environment to return. If ``auto`` is specified, try to
                autodetect the environment.

        Returns:
            Class representing the package manager environment.

        Raises:
            AutodetectionError:
                Raised if autodetection fails.
            EnvironmentNotInstalledError:
                Raised if the given environment is not installed.
            KeyError:
                Raised if an invalid environment string is specified.

        """

        if environment_string == 'auto':
            detected_env = self._autodetect_env()
            if detected_env is None:
                raise AutodetectionError('Could not autodetect environment.')
            return detected_env

        env = self.environments[environment_string]
        if env.is_installed():
            return env
        else:
            raise EnvironmentNotInstalledError('Environment "%s" is not installed. ' % environment_string)
