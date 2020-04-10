import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.logging import default_handler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

LOG_PATH_ALL = os.path.join(LOG_PATH, 'all.log')

LOG_FILE_MAX_BYTES = 10 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 10


def init_app(app: Flask):
    app.logger.removeHandler(default_handler)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(filename)s] %(message)s"
    )

    file_handler = RotatingFileHandler(
        filename=LOG_PATH_ALL,
        mode='a',
        maxBytes=LOG_FILE_MAX_BYTES,
        backupCount=LOG_FILE_BACKUP_COUNT,
        encoding='utf-8'
    )

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)

    for logger in (app.logger,
                   logging.getLogger('werkzeug')):
        logger.addHandler(file_handler)
