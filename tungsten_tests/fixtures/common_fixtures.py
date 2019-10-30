import logging
import pytest

from tungsten_tests.config import MCPConfig
from tungsten_tests.settings import TFT_CONF
from tungsten_tests.helpers import common, exceptions

logger = logging.getLogger()


@pytest.fixture(scope='session')
def config():
    if not TFT_CONF:
        raise exceptions.TFTConfigPathIsNotSet
    # if not os.path.isfile(TFT_CONF):
    #     raise exceptions.FileNotFoundError(path=TFT_CONF)
    return MCPConfig(TFT_CONF)


@pytest.fixture(scope='function')
def cleanup():
    _cleanups = []

    def cleanup_func(function, *args, **kwargs):
        _cleanups.append((function, args, kwargs))

    yield cleanup_func

    logger.info("Run cleanup (scope: function)")
    for c in reversed(_cleanups):
        try:
            logger.info("call {} with args: {}, kwargs: {}".format(
                c[0], c[1], c[2]))
            c[0](*c[1], **c[2])
        except Exception, e:
            logger.error("Failed to call cleanup function: {}".format(e))


@pytest.fixture(scope='class')
def cleanup_class():
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

    def return_ssh_connect(hostname, username='ubuntu',
                           pkey=config.os_private_key, **kwargs):
        client = common.ssh_connect(hostname, username=username, pkey=pkey,
                                    attempts=5, **kwargs)
        _connections.append(client)
        return client

    yield return_ssh_connect

    # Close sessions
    for c in _connections:
        logger.info("Close SSH session with {}".format(c))
        c.close
