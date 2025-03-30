"""Tests for the Flask API application."""

import json
from pathlib import Path
from typing import Dict, Any

import pytest
from flask.testing import FlaskClient

from dind_python_project.api.app import create_app
from dind_python_project.config import AppConfig


class TestAPI:
    """Test suite for the Flask API."""

    def test_health_check(self, client: FlaskClient) -> None:
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "healthy"
        assert "version" in data

    def test_process_endpoint_no_file(self, client: FlaskClient) -> None:
        """Test process endpoint with no file."""
        response = client.post("/api/v1/process")
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert "error" in data
        assert "No file provided" in data["error"]

    def test_process_endpoint_empty_filename(self, client: FlaskClient) -> None:
        """Test process endpoint with empty filename."""
        response = client.post(
            "/api/v1/process",
            data={"file": (b"", "")},
            content_type="multipart/form-data"
        )
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert "error" in data
        assert "No file selected" in data["error"]

    def test_process_endpoint_with_file(self, client: FlaskClient, sample_data: Dict[str, Any]) -> None:
        """Test process endpoint with a valid file."""
        file_content = json.dumps(sample_data).encode("utf-8")
        
        response = client.post(
            "/api/v1/process",
            data={"file": (file_content, "test_data.json")},
            content_type="multipart/form-data"
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert "processed" in data
        assert data["processed"] is True
        assert "backend" in data
        assert "summary" in data

    def test_app_configuration(self) -> None:
        """Test application configuration."""
        config = AppConfig(debug=True, env="testing", log_level="DEBUG", use_gpu=True)
        app = create_app(config)
        
        assert app.config["debug"] is True
        assert app.config["env"] == "testing"
        assert app.config["log_level"] == "DEBUG"
        assert app.config["use_gpu"] is True