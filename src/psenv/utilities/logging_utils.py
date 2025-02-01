import logging
from typing import Optional

from psenv.environment import config


def get_logger(name: str, terminal_stream: Optional[bool] = True) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if config.PSENV_ENABLE_FILE_LOGGING:
        formatter = logging.Formatter(fmt=config.PSENV_LOG_MSG_FORMAT, datefmt=config.PSENV_LOG_DATE_FORMAT)

        file_handler = logging.FileHandler(filename=config.PSENV_LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if name.endswith("error_handler"):
            with config.PSENV_LOG_FILE.open("a") as file:
                file.write(f"\n --- Logging to {config.PSENV_LOG_FILE} at {config.PSENV_NOW} --- \n")

    if not terminal_stream:
        return logger

    stream_formatter = logging.Formatter(fmt=config.PSENV_STREAM_FORMAT, datefmt=config.PSENV_LOG_DATE_FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(getattr(logging, config.PSENV_LOG_LEVEL))
    logger.addHandler(stream_handler)

    return logger
