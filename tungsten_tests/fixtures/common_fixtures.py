import logging
import pytest

from tungsten_tests.config import MCPConfig
from tungsten_tests.settings import TFT_CONF

logger = logging.getLogger()


@pytest.fixture(scope='session')
def config():
    return MCPConfig(TFT_CONF)


@pytest.fixture(scope='module')
def cleanup():
    _cleanups = []

    def cleanup_func(function, *args, **kwargs):
        _cleanups.append((function, args, kwargs))

    yield cleanup_func

    logger.info("Run cleanup")
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

    logger.info("Run cleanup")
    for c in reversed(_cleanups):
        try:
            logger.info("call {} with args: {}, kwargs: {}".format(
                c[0], c[1], c[2]))
            c[0](*c[1], **c[2])
        except Exception, e:
            logger.error("Failed to call cleanup function: {}".format(e))
