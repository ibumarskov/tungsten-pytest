import os.path

import pytest

from tungsten_tests.clients.k8s_env_client import K8sEnvClient
from tungsten_tests.settings import TFT_KUBECONFIG
from tungsten_tests.helpers import exceptions


@pytest.fixture(scope='session')
def k8s_client(config):
    if not TFT_KUBECONFIG:
        raise exceptions.TFTKubeConfigPathIsNotSet
    if not os.path.isfile(TFT_KUBECONFIG):
        raise exceptions.FileNotFoundError(path=TFT_KUBECONFIG)
    return K8sEnvClient(TFT_KUBECONFIG, config)
