import logging


def get_logger(name: str, terminal_stream: Optional[bool] = True) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if PSENV_ENABLE_FILE_LOGGING:
        formatter = logging.Formatter(fmt=PSENV_LOG_MSG_FORMAT, datefmt=PSENV_LOG_DATE_FORMAT)

        file_handler = logging.FileHandler(filename=PSENV_LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if name.endswith("error_handler"):
            with PSENV_LOG_FILE.open("a") as file:
                file.write(f"\n --- Logging to {PSENV_LOG_FILE} at {PSENV_NOW} --- \n")

    if not terminal_stream:
        return logger

    stream_formatter = logging.Formatter(fmt=PSENV_STREAM_FORMAT, datefmt=PSENV_LOG_DATE_FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(getattr(logging, PSENV_LOG_LEVEL))
    logger.addHandler(stream_handler)

    return logger
