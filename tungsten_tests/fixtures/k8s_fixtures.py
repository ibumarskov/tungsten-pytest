import pytest

from tungsten_tests.clients.k8s_env_client import K8sEnvClient
from tungsten_tests.settings import TFT_KUBECONFIG


@pytest.fixture(scope='session')
def k8s_client(config):
    return K8sEnvClient(TFT_KUBECONFIG, config)
