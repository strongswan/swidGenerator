import pytest

from swid_generator.environments.common import CommonEnvironment
from swid_generator.environments.environment_registry import EnvironmentRegistry
from swid_generator.exceptions import AutodetectionError, EnvironmentNotInstalledError


class TestEnvironment(CommonEnvironment):
    @classmethod
    def is_installed(cls):
        return False


@pytest.fixture
def env_registry():
    return EnvironmentRegistry()


def test_autodetection_fail(env_registry):
    env_registry.register('test_env', TestEnvironment)

    with pytest.raises(AutodetectionError):
        env_registry.get_environment('auto')


def test_not_executable_fail(env_registry):
    env_registry.register('test_env', TestEnvironment)

    with pytest.raises(EnvironmentNotInstalledError):
        env_registry.get_environment('test_env')
