from pathlib import Path

from psenv.api import LoadPsEnv
import os

load_psenv = LoadPsEnv(
    config_path=Path("demo/psenv.yml"),
    env="dev"
)

load_psenv()

for key, value in os.environ.items():
    print(f"{key}={value}")

