from typing import Dict

import pytest
from psenv.core.config.api_config import ApiConfig
from psenv.core.error_handling.exceptions import PsenvConfigException

@pytest.fixture
def valid_config_data() -> Dict[str, str]:
    return {
        "project": "test_project",
        "prefix": "test_prefix",
        "default": "test_default",
        "environments": ["dev", "prod"]
    }

@pytest.fixture
def invalid_config_data() -> Dict[str, str]:
    return {
        "project": "test_project",
        "prefix": "test_prefix",
        "default": "test_default",
    }

@pytest.fixture
def invalid_character_config_data() -> Dict[str, str]:
    return {
        "project": "test_project",
        "prefix": "test_prefix",
        "default": "test_default",
        "environments": ["dev", "prod!"]
    }

def test_api_config_initialization(valid_config_data):
    config = ApiConfig(**valid_config_data)
    assert config.project == "test_project"
    assert config.prefix == "test_prefix"
    assert config.default == "test_default"
    assert config.environments == ["dev", "prod"]


def test_api_config_missing_key(invalid_config_data):
    with pytest.raises(PsenvConfigException) as excinfo:
        ApiConfig(**invalid_config_data)
    assert "Missing required key: environments" in str(excinfo.value)


def test_api_config_validation(valid_config_data):
    config = ApiConfig(**valid_config_data)
    config.validate()  # Should not raise any exception


def test_api_config_invalid_character(invalid_character_config_data):
    config = ApiConfig(**invalid_character_config_data)
    with pytest.raises(PsenvConfigException) as excinfo:
        config.validate()
    assert "Invalid value for key: environments value: ['dev', 'prod!'] character ! is not allowed" in str(excinfo.value)
