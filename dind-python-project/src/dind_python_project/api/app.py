"""Web API module for Flask application."""

import logging
from typing import Any, Dict, Optional

from flask import Flask, jsonify, request

from dind_python_project.config import AppConfig
from dind_python_project.core.processor import DataProcessor

logger = logging.getLogger(__name__)


def create_app(config: Optional[AppConfig] = None) -> Flask:
    """Create and configure the Flask application.
    
    Args:
        config: Application configuration. Defaults to None, which loads from environment.
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = AppConfig.from_env()
    
    # Configure app
    app.config.update(config.to_dict())
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Register routes
    register_routes(app)
    
    return app


def register_routes(app: Flask) -> None:
    """Register application routes.
    
    Args:
        app: Flask application
    """
    # Health check endpoint
    @app.route("/health")
    def health_check() -> Dict[str, Any]:
        """Health check endpoint."""
        return jsonify({"status": "healthy", "version": app.config.get("VERSION", "0.1.0")})
    
    # API endpoints
    @app.route("/api/v1/process", methods=["POST"])
    def process_data() -> Dict[str, Any]:
        """Process uploaded data."""
        if not request.files or "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        # Save uploaded file to temporary location
        import tempfile
        import os
        
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)
        file.save(temp_file_path)
        
        # Process the file
        try:
            use_gpu = app.config.get("use_gpu", False)
            processor = DataProcessor(use_gpu=use_gpu)
            result = processor.process_file(temp_file_path)
            
            # Clean up
            os.unlink(temp_file_path)
            os.rmdir(temp_dir)
            
            return jsonify(result)
        except Exception as e:
            logger.exception("Error processing file")
            # Clean up in case of error
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
            return jsonify({"error": str(e)}), 500