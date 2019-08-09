import pytest
from tungsten_tests.clients.k8s_env_client import K8sEnvClient
from tungsten_tests import settings


@pytest.fixture(scope='session')
def k8s_client():
    return K8sEnvClient(settings.OSDPL_NAMESPACE)
