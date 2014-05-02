# -*- coding: utf-8 -*-
class AutodetectionError(RuntimeError):
    pass


class EnvironmentNotInstalledError(RuntimeError):
    pass


class EnvironmentRegistry(object):
    def __init__(self):
        self.environments = {}

    def _autodetect_env(self):
        """
        Detect the used packetmanager by searching for a given executable in the path.
        Return a static class representing the packetmanager environment or None if autodetection fails.

        """

        for environment_string, environment_class in self.environments.items():
            if environment_class.is_installed():
                return environment_class

    def get_environment_strings(self):
        """
        Return the registered environments

        Returns:
            String describing environment (e.g 'rpm', 'dpkg')

        """
        strings = ['auto']
        for env in self.environments.keys():
            strings.append(env)
        return strings

    def register(self, environment_name, environment_class):
        self.environments[environment_name] = environment_class

    def get_environment(self, environment_string):
        """
        Try to get the environment class for the given environment string.

        Args:
            environment_string (str):
                The evnironment to lookup. If 'auto' is used, try to autodetect the environment

        Returns:
            Class representing the packetmanager environment or
            None if the environment is not found or not installed.

        Raises:
            AutodetectionError:
                Raised if autodetection fails.
            EnvironmentNotInstalledError:
                Raised if the given environment is not installed.
        """

        if environment_string == 'auto':
            detected_env = self._autodetect_env()
            if detected_env is None:
                raise AutodetectionError('Could not autodetect environment.')
            return detected_env

        # if an explicit environment is provided
        env = self.environments[environment_string]
        if env.is_installed():
            return env
        else:
            raise EnvironmentNotInstalledError('Environment "%s" is not installed. ' % environment_string)