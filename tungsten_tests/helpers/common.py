import logging
import os
import paramiko
import time
import urllib2

from tungsten_tests.helpers import exceptions

logger = logging.getLogger()


def download_file(url, path='~'):
    file_path = path + '/' + os.path.basename(url)
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    if os.path.isfile(file_path):
        logger.info('File {} found. Skip download.'.format(file_path))
        return file_path
    logger.info('Start download: {}'.format(url))
    filedata = urllib2.urlopen(url)
    datatowrite = filedata.read()
    with open(file_path, 'wb') as f:
        f.write(datatowrite)
    logger.info('File was downloaded: {}'.format(file_path))
    return file_path


def ssh_connect(hostname, username='ubuntu', pkey=None, attempts=5, **kwargs):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if pkey is not None:
        pkey = paramiko.RSAKey.from_private_key_file(pkey)
    logger.info("Establish SSH connect to {}".format(hostname))
    for i in range(attempts):
        try:
            logger.debug("Attempt {} from {}".format(i+1, attempts))
            client.connect(hostname=hostname, username=username, pkey=pkey,
                           **kwargs)
            break
        except Exception as e:
            logger.debug("Attempt failed: {}".format(e))
            time.sleep(10)
            continue
    if not client.get_transport().is_active():
        client.connect(hostname=hostname, username=username, pkey=pkey,
                       **kwargs)
    return client


def exec_command(ssh_client, cmd):
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    out = stdout.read()
    err = stderr.read()
    logger.debug("stdout:\n{}".format(out))
    if err:
        logger.debug("stderr:\n{}".format(err))
    return out, err


def wait_for_cloud_init(ssh_client, interval=10, retries=18):
    exit_code = None
    logger.info("Check cloud initialization")
    for i in range(retries):
        logger.debug("Attempt {} from {}".format(i+1, retries))
        stdin, stdout, stderr = ssh_client.exec_command(
            'ls /home/ubuntu/tft_ready')
        exit_code = (stdout.channel.recv_exit_status())
        if exit_code == 0:
            logger.info("Initialization is completed")
            break
        time.sleep(interval)
    if exit_code != 0:
        out = stdout.read()
        err = stderr.read()
        logger.error("stdout:\n{}\nstderr:\n{}".format(out, err))
        raise exceptions.InstanceNotReady


def wait_for_http_status(url, expected_code=200, interval=3, retries=20):
    status_code = None
    logger.info("Check HTTP status code of the response")
    for i in range(retries):
        logger.debug("Attempt {} from {}".format(i + 1, retries))
        request = urllib2.Request(url)
        try:
            status_code = urllib2.urlopen(request).getcode()
        except:  # noqa
            pass
        if status_code == expected_code:
            logger.info("Got expected HTTP status code")
            break
        time.sleep(interval)
    if status_code != expected_code:
        raise exceptions.IncorrectHTTPStatusCode(code=status_code,
                                                 expected=expected_code)
