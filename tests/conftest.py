from typing import Dict

import pytest
from pathlib import Path


@pytest.fixture
def fixture_path() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def good_api_config_path(fixture_path) -> Path:
    return fixture_path / "good_api_config.yml"


@pytest.fixture
def valid_config_data() -> Dict[str, str]:
    return {"project": "test_project", "prefix": "test_prefix", "default": "test_default", "environments": ["dev", "prod"]}


@pytest.fixture
def invalid_config_data() -> Dict[str, str]:
    return {
        "project": "test_project",
        "prefix": "test_prefix",
        "default": "test_default",
    }


@pytest.fixture
def invalid_character_config_data() -> Dict[str, str]:
    return {"project": "test_project", "prefix": "test_prefix", "default": "test_default", "environments": ["dev", "prod!"]}
