import pytest

from tungsten_tests.clients.k8s_env_client import K8sEnvClient, \
    K8sTFOperator, K8sTFAnalytic, K8sTFConfig, K8sTFControl, K8sTFVrouter
from tungsten_tests.settings import TFT_KUBECONFIG


@pytest.fixture(scope='session')
def k8s_client(config):
    return K8sEnvClient(TFT_KUBECONFIG)


@pytest.fixture(scope='session')
def k8s_tf_operator(config):
    return K8sTFOperator(TFT_KUBECONFIG,
                         name=config.k8s_tfoperator_name,
                         namespace=config.k8s_tfoperator_namespace,
                         plural=config.k8s_tfoperator_plural,
                         group=config.k8s_tfoperator_group,
                         version=config.k8s_tfoperator_version)


@pytest.fixture(scope='session')
def k8s_tf_analytic(config):
    return K8sTFAnalytic(TFT_KUBECONFIG, name='tf-analytics',
                         namespace=config.k8s_tfoperator_namespace,
                         plural='tfanalytics',
                         group='analytics.tf.mirantis.com',
                         version=config.k8s_tfoperator_version)


@pytest.fixture(scope='session')
def k8s_tf_config(config):
    return K8sTFConfig(TFT_KUBECONFIG, name='tf-config',
                       namespace=config.k8s_tfoperator_namespace,
                       plural='tfconfigs',
                       group='config.tf.mirantis.com',
                       version=config.k8s_tfoperator_version)


@pytest.fixture(scope='session')
def k8s_tf_control(config):
    return K8sTFControl(TFT_KUBECONFIG, name='tf-control',
                        namespace=config.k8s_tfoperator_namespace,
                        plural='tfcontrols',
                        group='control.tf.mirantis.com',
                        version=config.k8s_tfoperator_version)


@pytest.fixture(scope='session')
def k8s_tf_vrouter(config):
    return K8sTFVrouter(TFT_KUBECONFIG, name='tf-vrouter',
                        namespace=config.k8s_tfoperator_namespace,
                        plural='tfvrouters',
                        group='vrouter.tf.mirantis.com',
                        version=config.k8s_tfoperator_version)
