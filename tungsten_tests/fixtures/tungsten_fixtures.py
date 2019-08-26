import pytest
from tungsten_tests import settings
from tungsten_tests.clients.tungsten.vnc_client import ContrailEnvClient
from tungsten_tests.clients.tungsten.analytic_client import ContrailAnalClient
from tungsten_tests.config import MCPConfig


conf = MCPConfig(settings.TF_CONF)


@pytest.fixture(scope='session')
def tf():
    return ContrailEnvClient(
        username=conf.tf_auth_user, password=conf.tf_auth_pwd,
        tenant_name=conf.tf_auth_tenant, api_server_host=conf.tf_srv_ip,
        api_server_port=conf.tf_srv_port, auth_host=conf.tf_auth_srv,
        auth_port=conf.tf_auth_port, auth_protocol=conf.tf_auth_proto,
        auth_url=conf.tf_auth_url, auth_type=conf.tf_auth_type)


@pytest.fixture(scope='session')
def tf_analytic():
    return ContrailAnalClient(ip=conf.tf_nal_ip,
                              port=conf.tf_nal_port)
