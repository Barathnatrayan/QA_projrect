import logging
import os


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    if os.getenv('LOG_PID'):
        formatter = logging.Formatter('[%(process)d] %(message)s')
        sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


def custom_file_stream_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        # sh = logging.StreamHandler()
        fh = logging.FileHandler(f'manifest_debug_logs.txt')
        logger.addHandler(fh)
        # logger.addHandler(sh)
    return logger
