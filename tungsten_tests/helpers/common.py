from contextlib import contextmanager
import logging
import os
import paramiko
import time
import urllib2

from tungsten_tests.helpers import exceptions

logger = logging.getLogger()


def download_file(url, path='~'):
    file_path = path + '/' + os.path.basename(url)
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


@contextmanager
def ssh_connect(hostname, username='ubuntu', pkey=None, **kwargs):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if pkey is not None:
        pkey = paramiko.RSAKey.from_private_key_file(pkey)

    logger.info("Establish SSH connect to {}".format(hostname))
    try:
        attempts = 12
        for i in range(attempts):
            try:
                logger.info("Attempt {} from {}".format(i, attempts))
                client.connect(hostname=hostname, username=username, pkey=pkey,
                               **kwargs)
                break
            except Exception as e:
                logger.warning("Attempt failed: {}".format(e))
                time.sleep(10)
                continue
        yield client
    finally:
        client.close()


def wait_for_cloud_init(ssh_client, interval=5, retries=12):
    exit_code = None
    logger.info("Check cloud initialization")
    for i in range(retries):
        logger.debug("Retry {} from {}".format(i+1, retries))
        ssh_client
        stdin, stdout, stderr = ssh_client.exec_command(
            'ls /home/ubuntu/tft_ready')
        exit_code = (stdout.channel.recv_exit_status())
        if exit_code == 0:
            break
        time.sleep(interval)
    out = stdout.read()
    err = stderr.read()
    logger.debug("stdout:\n{}\nstderr:\n{}".format(out, err))
    if exit_code is None:
        raise exceptions.InstanceNotReady
