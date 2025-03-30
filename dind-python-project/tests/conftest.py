"""Test configuration and fixtures for the application."""

import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from dind_python_project.api.app import create_app
from dind_python_project.config import AppConfig


@pytest.fixture
def app_config() -> AppConfig:
    """Create test application configuration."""
    return AppConfig(debug=True, env="testing", log_level="DEBUG")


@pytest.fixture
def app(app_config: AppConfig) -> Flask:
    """Create test Flask application."""
    return create_app(app_config)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """Create sample data for testing."""
    return {
        "name": "Test Project",
        "values": [1, 2, 3, 4, 5],
        "metadata": {
            "author": "Test User",
            "version": "1.0.0"
        }
    }


@pytest.fixture
def sample_data_file(sample_data: Dict[str, Any]) -> Generator[Path, None, None]:
    """Create a temporary file with sample data for testing."""
    import json
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
        json.dump(sample_data, temp_file)
        temp_file_path = Path(temp_file.name)
    
    yield temp_file_path
    
    # Clean up after the test
    if temp_file_path.exists():
        os.unlink(temp_file_path)