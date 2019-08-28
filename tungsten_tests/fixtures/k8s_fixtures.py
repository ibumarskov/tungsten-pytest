import pytest
from tungsten_tests.clients.k8s_env_client import K8sEnvClient


@pytest.fixture(scope='session')
def k8s_client(config):
    return K8sEnvClient(kubeconfig=config.k8s_kubeconfig,
                        osdpl_name=config.k8s_osdpl_name,
                        osdpl_namespace=config.k8s_osdpl_namespace)
