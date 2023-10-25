import yaml
from pathlib import Path


def create_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def create_file(path: Path) -> None:
    path.touch(exist_ok=True)


def write_file(path: Path, content: str) -> None:
    with path.open("w") as file:
        file.write(content)


def write_yml_file_if_not_exists(path: Path, content: dict) -> None:
    if not path.exists():
        write_yml_file(path, content)


def write_yml_file(path: Path, content: dict) -> None:
    with path.open("w") as file:
        yaml.dump(content, file, default_flow_style=False)


def read_yml_file(path: Path) -> dict:
    with path.open("r") as file:
        return yaml.safe_load(file)
