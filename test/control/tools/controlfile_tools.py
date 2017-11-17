import os
import logging
import time
import hashlib
import yaml
from NewLogger import InitLog

version_status = 'debug'

logger = InitLog().getLogger()

def controlfile(status):
    def deractor(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return deractor

def log_bystatus(text_content, log_level):

    time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    log_msg = ''.join([time_str, '--------->loglevel: (%s)\n' % log_level, text_content, '\n'])
    if version_status == 'debug':
        # print(text_content+'\n')
        if log_level == 'i':
            logger.info(log_msg)
        elif log_level == 'e':
            logger.error(log_msg)
        else:
            logger.warning(log_msg)

def load(file_path, decodemethod = 'UTF-8'):
    """load file data with default utf-8"""
    with open(file_path, 'r') as f:
        read_content = (f.read()).decode(encoding=decodemethod, errors='strict')
        log_bystatus(read_content, 'i')
        return read_content

def loadyaml(file_path, decodemethod = 'UTF-8'):

    file_data = load(file_path, decodemethod)
    try:

        yaml_data = yaml.load(file_data)
        return yaml_data

    except ValueError as e:
        log_bystatus(e, 'e')
        return None

def save(file, file_content, decodemethod = 'UTF-8'):

    with open(file, 'w') as f:
        f.write(file_content.encode(encoding=decodemethod, errors='strict'))

def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

if __name__ == '__main__':

    print sha256_checksum('__init__.py')
    log_bystatus('err!!!!', 'i')
    log_bystatus('err!!!!', 'e')
    log_bystatus('err!!!!', 'w')