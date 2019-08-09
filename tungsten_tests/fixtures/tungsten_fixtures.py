import pytest
from tungsten_tests.clients.tungsten.vnc_client import ContrailEnvClient
from tungsten_tests.clients.tungsten.analytic_client import ContrailAnalClient
from tungsten_tests import settings


@pytest.fixture(scope='session')
def tf():
    return ContrailEnvClient(conf_file=settings.VNC_CONF_FILE)


@pytest.fixture(scope='session')
def tf_analytic():
    return ContrailAnalClient(ip=settings.ANALYTIC_IP,
                              port=settings.ANALYTIC_PORT)
