import datetime
import os
from pathlib import Path

# used to load the api configs file
PSENV_API_CONFIG_FILE = Path(os.getenv("PSENV_API_CONFIG_FILE", "psenv.yml"))
PSENV_PARAMETERS_CONFIG_FILE = Path(os.getenv("PSENV_PARAMETERS_CONFIG_FILE", "psenv.yml"))
PSENV_DEFAULT_ENVIRONMENT = os.getenv("PSENV_DEFAULT_ENVIRONMENT")

PSENV_NOW = str(datetime.datetime.now())

# used to turn on debug logging on and off
PSENV_DEBUG = os.getenv("PSENV_DEBUG", "false").lower() == "true"
PSENV_LOG_LEVEL = os.getenv("PSENV_LOG_LEVEL", "INFO")
PSENV_ENABLE_FILE_LOGGING = os.getenv("PSENV_ENABLE_FILE_LOGGING", "false").lower() == "true"
PSENV_LOG_MSG_FORMAT = "%(levelname)s :: %(asctime)s :: %(name)s :: %(message)s"
PSENV_STREAM_FORMAT = "%(message)s"
PSENV_LOG_DATE_FORMAT = "%Y-%m-%d %I:%M:%S %p"
PSENV_LOG_FILE = os.getenv("PSENV_LOG_FILE", "psenv.log")
