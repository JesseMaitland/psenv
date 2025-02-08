from typing import Dict
from unittest.mock import patch
import pytest
from psenv.core.configs.api_config import ApiConfig, ApiConfigLoader
from psenv.core.error_handling.exceptions import PsenvConfigException


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


def test_api_config_loader(good_api_config_path):
    loader = ApiConfigLoader(good_api_config_path)
    config = loader.load()
    assert isinstance(config, ApiConfig)


def test_validation_called_on_load(good_api_config_path):
    with patch.object(ApiConfig, "validate") as mock_validate:
        loader = ApiConfigLoader(good_api_config_path)
        loader.load()
        mock_validate.assert_called_once()
