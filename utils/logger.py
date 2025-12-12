import logging
import os


import logging
from config.settings import LOG_LEVEL


def get_logger(name: str = "luda"):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

