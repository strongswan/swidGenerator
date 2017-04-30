import pytest

from minimock import Mock

from swid_generator.environments.common import CommonEnvironment
from swid_generator.environments.environment_registry import EnvironmentRegistry
from swid_generator.exceptions import AutodetectionError, EnvironmentNotInstalledError


class TestEnvironmentFail(CommonEnvironment):
    @classmethod
    def is_installed(cls):
        return False


class TestEnvironmentNoFail(CommonEnvironment):
    @classmethod
    def is_installed(cls):
        return True


@pytest.fixture
def env_registry():
    env_registry = EnvironmentRegistry()
    env_registry.register("test_env_fail", TestEnvironmentFail)
    env_registry.register("test_env_no_fail", TestEnvironmentNoFail)
    return env_registry

@pytest.fixture
def env_registry_with_fail():
    env_registry = EnvironmentRegistry()
    env_registry.register("test_env_fail", TestEnvironmentFail)
    return env_registry


def test_autodetection_no_fail(env_registry):
    with pytest.raises(AutodetectionError):
        env_registry.get_environment('auto')


def test_autodetection_no_fail(env_registry_with_fail):
    with pytest.raises(AutodetectionError):
        env_registry_with_fail.get_environment('auto')


def test_not_executable_fail(env_registry):
    env_registry.register('test_env', TestEnvironmentFail)

    with pytest.raises(EnvironmentNotInstalledError):
        env_registry.get_environment('test_env')


def test_environment_registry_register(env_registry, env_registry_with_fail):
    assert len(env_registry.environments) == 2
    assert len(env_registry_with_fail.environments) == 1
    assert env_registry.environments['test_env_fail'] is not None
    assert env_registry.environments['test_env_no_fail'] is not None


def test_get_environment(env_registry):
    env = env_registry.get_environment('test_env_no_fail')
    assert env is not None


def test_get_environment_strings(env_registry):
    result = env_registry.get_environment_strings()
    expected = ['auto', 'test_env_fail', 'test_env_no_fail']
    assert result == expected
