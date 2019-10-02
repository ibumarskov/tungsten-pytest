import logging
import paramiko
import pytest
import time

from tungsten_tests.config import MCPConfig
from tungsten_tests.settings import TFT_CONF
from tungsten_tests.helpers import exceptions

logger = logging.getLogger()


@pytest.fixture(scope='session')
def config():
    if not TFT_CONF:
        raise exceptions.TFTConfigPathIsNotSet
    # if not os.path.isfile(TFT_CONF):
    #     raise exceptions.FileNotFoundError(path=TFT_CONF)
    return MCPConfig(TFT_CONF)


@pytest.fixture(scope='class')
def cleanup():
    _cleanups = []

    def cleanup_func(function, *args, **kwargs):
        _cleanups.append((function, args, kwargs))

    yield cleanup_func

    logger.info("Run cleanup (scope: class)")
    for c in reversed(_cleanups):
        try:
            logger.info("call {} with args: {}, kwargs: {}".format(
                c[0], c[1], c[2]))
            c[0](*c[1], **c[2])
        except Exception, e:
            logger.error("Failed to call cleanup function: {}".format(e))


@pytest.fixture(scope='session')
def cleanup_session():
    _cleanups = []

    def cleanup_func(function, *args, **kwargs):
        _cleanups.append((function, args, kwargs))

    yield cleanup_func

    logger.info("Run cleanup (scope: session)")
    for c in reversed(_cleanups):
        try:
            logger.info("call {} with args: {}, kwargs: {}".format(
                c[0], c[1], c[2]))
            c[0](*c[1], **c[2])
        except Exception, e:
            logger.error("Failed to call cleanup function: {}".format(e))


@pytest.fixture()
def ssh_connect(config, create_keypair):
    _connections = []
    k = paramiko.RSAKey.from_private_key_file(config.os_private_key)

    def return_ssh_connect(hostname, username='ubuntu', pkey=k, **kwargs):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logger.info("Establish SSH connect to {}".format(hostname))
        attempts = 5
        for i in range(attempts):
            try:
                logger.info("Attempt {} from {}".format(i, attempts))
                client.connect(hostname=hostname, username=username, pkey=pkey,
                               **kwargs)
                _connections.append(client)
                return client
            except Exception as e:
                logger.warning("Attempt failed: {}".format(e))
                time.sleep(10)
                continue

    yield return_ssh_connect

    # Close sessions
    for c in _connections:
        logger.info("Close SSH session with {}".format(c))
        c.close
