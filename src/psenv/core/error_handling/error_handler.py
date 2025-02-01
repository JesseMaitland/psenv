import functools
from psenv.utilities.logging_utils import get_logger
from psenv.core.error_handling import exceptions
from psenv.environment.config import (
    PSENV_DEBUG,
    PSENV_ENABLE_FILE_LOGGING,
    PSENV_DEBUG
)

logger = get_logger(__name__)


class ErrorHandler:
    def __init__(self) -> None:
        self.debug = PSENV_DEBUG

    def handle(self, exception: Exception) -> int:
        self.log_error(exception)
        return self.reraise_if_debug(exception)

    @staticmethod
    def log_error(exception: Exception) -> None:
        if PSENV_ENABLE_FILE_LOGGING:
            error_logger = get_logger("error_logger", terminal_stream=False)
            error_logger.exception(exception)
        logger.info(exception.args[0])

    def reraise_if_debug(self, exception: Exception) -> int:
        """Reraise exception if we are debugging."""
        if self.debug:
            raise exception
        else:
            return 1


def handle_cli_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        error_handler = ErrorHandler()

        try:
            return func(*args, **kwargs)

        except PermissionError as e:
            return error_handler.handle(e)

        except FileNotFoundError as e:
            return error_handler.handle(e)

        except OSError as e:
            return error_handler.handle(e)

        except exceptions.PsenvConfigException as e:
            return error_handler.handle(e)

    return wrapper
