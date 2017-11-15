import logging
import hashlib

version_status = 'debug'

def controlfile(status):
    def deractor(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return deractor

def log_bystatus(text_content, log_level):
    if version_status == 'debug':
        # print(text_content+'\n')
        if log_level == 'i':
            logging.info(text_content + '\n')
        elif log_level == 'e':
            logging.error(text_content + '\n')
        else:
            logging.warning(text_content + '\n')

def load(file, decodemethod = 'UTF-8'):
    """load file data with default utf-8"""
    with open(file, 'r') as f:
        read_content = (f.read()).decode(encoding=decodemethod, errors='strict')
        log_bystatus(read_content, 'i')
        return read_content

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