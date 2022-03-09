import os
import logging.handlers
from os.path import dirname,abspath

base_path = dirname(dirname(abspath(__file__)))

logger = logging.getLogger('datahub')
logger.setLevel(logging.DEBUG)
handler_all = logging.handlers.TimedRotatingFileHandler(
    filename=os.path.join(base_path, 'log', 'datahub.log'), when='M', backupCount=3, encoding='UTF-8')
logger.addHandler(handler_all)


def info(msg):
    logger.info(msg)


def warning(msg):
    logger.warning(msg)


def error(msg):
    logger.error(msg)


def exception(msg):
    logger.exception(msg)