"""Tests for the core data processor."""

import json
import tempfile
from pathlib import Path

import pytest

from dind_python_project.core.processor import DataProcessor


class TestDataProcessor:
    """Test suite for the DataProcessor class."""

    def test_init_with_cpu(self) -> None:
        """Test initialization with CPU backend."""
        processor = DataProcessor(use_gpu=False)
        assert processor.use_gpu is False
        assert processor._has_gpu is False

    def test_process_file(self, sample_data_file: Path) -> None:
        """Test processing a file."""
        processor = DataProcessor(use_gpu=False)
        result = processor.process_file(sample_data_file)
        
        # Verify result structure
        assert "processed" in result
        assert result["processed"] is True
        assert "backend" in result
        assert result["backend"] == "CPU"
        assert "summary" in result
        
        # Verify summary contains expected statistics
        summary = result["summary"]
        assert "fields" in summary
        assert "values_count" in summary
        assert "values_mean" in summary
        assert "values_std" in summary
        assert "values_min" in summary
        assert "values_max" in summary
        
        # Verify statistics are correct
        assert summary["values_count"] == 5
        assert summary["values_mean"] == 3.0
        assert summary["values_min"] == 1.0
        assert summary["values_max"] == 5.0

    def test_save_results(self) -> None:
        """Test saving results to a file."""
        processor = DataProcessor(use_gpu=False)
        results = {
            "processed": True,
            "backend": "CPU",
            "summary": {"test": "value"}
        }
        
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
            output_path = Path(temp_file.name)
        
        try:
            processor.save_results(results, output_path)
            
            # Verify file exists and contains expected content
            assert output_path.exists()
            with open(output_path, "r") as f:
                saved_data = json.load(f)
            
            assert saved_data == results
        finally:
            # Clean up
            if output_path.exists():
                output_path.unlink()

    def test_file_not_found(self) -> None:
        """Test handling of non-existent files."""
        processor = DataProcessor(use_gpu=False)
        with pytest.raises(FileNotFoundError):
            processor.process_file("nonexistent_file.json")

    def test_unsupported_file_format(self, tmp_path: Path) -> None:
        """Test handling of unsupported file formats."""
        unsupported_file = tmp_path / "test.xyz"
        unsupported_file.write_text("test content")
        
        processor = DataProcessor(use_gpu=False)
        with pytest.raises(ValueError, match="Unsupported file format"):
            processor.process_file(unsupported_file)