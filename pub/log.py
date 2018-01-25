#! python3
# coding: utf-8

import logging
import logging.config
import os

log_conf = os.path.sep.join([os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"etc","log.conf"])
logging.config.fileConfig(log_conf)

logger = logging.getLogger("baton")

if __name__ == "__main__":
    logger.info("hello")
    logger.warning("warn")
    logger.debug("debug")