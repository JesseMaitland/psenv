import os
from dotenv import load_dotenv

load_dotenv()

PSENV_DEBUG = os.environ.get("PSENV_DEBUG", "").lower() == "true"


# PSENV_AWS_ACCOUNT_ID = int(os.getenv("PSENV_AWS_ACCOUNT_ID", 0))
# PSENV_AWS_ARN_NAME = os.getenv("PSENV_AWS_ARN_NAME", None)
