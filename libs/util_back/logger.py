import os
import logging

from loguru import logger as log
from gstore import log_dir, GSTORE


class AllureHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.stream = None

    def emit(self, record):
        logging.getLogger(record.name).handle(record)


def set_allure_handler():
    """
    allure报告 handler
    """
    ah = AllureHandler()
    log.add(ah, level=logging.DEBUG, backtrace=True, diagnose=True)


def set_file_handler():
    """
    文件handler
    """
    log_file = os.path.join(log_dir, f"{GSTORE['time']}_log.log")
    log.add(log_file, level=logging.DEBUG, rotation="50 MB", retention="3 days", backtrace=True,
            diagnose=True, enqueue=True)


def init_log():
    set_file_handler()
    set_allure_handler()
