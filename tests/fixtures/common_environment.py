import pytest
from minimock import Mock

from swid_generator.environments.common import CommonEnvironment


@pytest.fixture
def common_environment():
    CommonEnvironment.get_architecture = Mock("CommonEnviroment.get_architecture")
    CommonEnvironment.get_architecture.mock_returns = 'i686'
    return CommonEnvironment
