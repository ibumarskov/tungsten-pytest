import pytest
from tungsten_tests.clients.k8s_env_client import K8sEnvClient
from tungsten_tests import settings
from tungsten_tests.config import MCPConfig


conf = MCPConfig(settings.TF_CONF)


@pytest.fixture(scope='session')
def k8s_client():
    return K8sEnvClient(kubeconfig=conf.k8s_kubeconfig,
                        osdpl_name=conf.k8s_osdpl_name,
                        osdpl_namespace=conf.k8s_osdpl_namespace)
