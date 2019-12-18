import pytest

from tungsten_tests.clients.tungsten.vnc_client import ContrailEnvClient
from tungsten_tests.clients.tungsten.analytic_client import AnalyticClient


@pytest.fixture(scope='session')
def tf(config):
    return ContrailEnvClient(
        username=config.tf_auth_user, password=config.tf_auth_pwd,
        tenant_name=config.tf_auth_tenant, api_server_host=config.tf_srv_ip,
        api_server_port=config.tf_srv_port, auth_host=config.tf_auth_srv,
        auth_port=config.tf_auth_port, auth_protocol=config.tf_auth_proto,
        auth_url=config.tf_auth_url, auth_type=config.tf_auth_type)


@pytest.fixture(scope='session')
def tf_analytic():
    ip = '10.11.0.228'
    return AnalyticClient(ip=ip)
