import logging
import os
import urllib2

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
