"""Core data processing module with GPU support."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process data with optional GPU acceleration."""

    def __init__(self, use_gpu: bool = False) -> None:
        """Initialize the processor.

        Args:
            use_gpu: Whether to use GPU acceleration if available
        """
        self.use_gpu = use_gpu
        self._initialize_backend()

    def _initialize_backend(self) -> None:
        """Initialize the appropriate backend based on settings."""
        if self.use_gpu:
            try:
                # Conditionally import GPU libraries to avoid dependencies when not needed
                # This is just a placeholder - in reality you would initialize your
                # GPU frameworks here (PyTorch, TensorFlow, etc.)
                logger.info("Initializing GPU backend")
                self._has_gpu = True
            except ImportError:
                logger.warning("GPU requested but libraries not available, falling back to CPU")
                self._has_gpu = False
        else:
            logger.info("Using CPU backend")
            self._has_gpu = False

    def process_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Process data from a file.

        Args:
            file_path: Path to the input file

        Returns:
            Processed data as a dictionary
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")

        # Read the file
        logger.info(f"Processing file: {file_path}")
        data = self._read_file(file_path)

        # Process the data
        return self._process_data(data)

    def _read_file(self, file_path: Path) -> Dict[str, Any]:
        """Read data from a file.

        Args:
            file_path: Path to the input file

        Returns:
            Data read from the file
        """
        suffix = file_path.suffix.lower()
        if suffix == ".json":
            with open(file_path, "r") as f:
                return json.load(f)
        elif suffix in (".txt", ".csv"):
            # This is a simplified example - real implementation would be more robust
            data = []
            with open(file_path, "r") as f:
                for line in f:
                    data.append(line.strip())
            return {"lines": data}
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    def _process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the data using the appropriate backend.

        Args:
            data: Input data dictionary

        Returns:
            Processed data
        """
        # This is a placeholder implementation
        # In a real application, this would do meaningful processing
        result = {
            "processed": True,
            "backend": "GPU" if self._has_gpu else "CPU",
            "summary": self._generate_summary(data),
        }
        return result

    def _generate_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the data.

        Args:
            data: Input data dictionary

        Returns:
            Summary statistics
        """
        # This is a simplified example
        summary = {"fields": len(data)}
        
        # Count items if there are lists
        for key, value in data.items():
            if isinstance(value, list):
                summary[f"{key}_count"] = len(value)
                
                # If the list contains numbers, calculate statistics
                if all(isinstance(x, (int, float)) for x in value):
                    arr = np.array(value)
                    summary[f"{key}_mean"] = float(arr.mean())
                    summary[f"{key}_std"] = float(arr.std())
                    summary[f"{key}_min"] = float(arr.min())
                    summary[f"{key}_max"] = float(arr.max())
        
        return summary

    def save_results(self, results: Dict[str, Any], output_path: Union[str, Path]) -> None:
        """Save processing results to a file.

        Args:
            results: Results to save
            output_path: Path where to save the results
        """
        output_path = Path(output_path)
        logger.info(f"Saving results to {output_path}")
        
        # Create directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)