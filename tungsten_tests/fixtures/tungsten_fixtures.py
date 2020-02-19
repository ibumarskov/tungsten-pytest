import pytest

from tungsten_tests.clients.tungsten.vnc_client import ContrailEnvClient
from tungsten_tests.clients.tungsten.analytic_client import AnalyticClient


@pytest.fixture(scope='session')
def tf(config, k8s_tf_config):
    service_name = k8s_tf_config.name + "-api"
    service = k8s_tf_config.read_namespaced_service(service_name)
    for p in service.spec.ports:
        if p.name == "api":
            config.tf_srv_port = p.port
    config.tf_srv_ip = service.spec.cluster_ip
    return ContrailEnvClient(
        username=config.tf_auth_user, password=config.tf_auth_pwd,
        tenant_name=config.tf_auth_tenant, api_server_host=config.tf_srv_ip,
        api_server_port=config.tf_srv_port, auth_host=config.tf_auth_srv,
        auth_port=config.tf_auth_port, auth_protocol=config.tf_auth_proto,
        auth_url=config.tf_auth_url, auth_type=config.tf_auth_type)


@pytest.fixture(scope='session')
def tf_analytic(k8s_tf_analytic):
    service_name = k8s_tf_analytic.name + "-api"
    service = k8s_tf_analytic.read_namespaced_service(service_name)
    port = None
    for p in service.spec.ports:
        if p.name == "api":
            port = p.port
    ip = service.spec.cluster_ip
    return AnalyticClient(ip=ip, port=port)
