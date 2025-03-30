"""Configuration handling for the application."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = Path(__file__).parents[3] / ".env"
load_dotenv(dotenv_path=dotenv_path)


@dataclass
class AppConfig:
    """Application configuration settings."""

    debug: bool = False
    env: str = "development"
    log_level: str = "INFO"
    use_gpu: bool = False
    version: str = "0.1.0"
    project_name: str = "dind-python-project"

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create configuration from environment variables."""
        return cls(
            debug=os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"),
            env=os.getenv("ENV", "development"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            use_gpu=os.getenv("USE_GPU", "False").lower() in ("true", "1", "yes"),
            version=os.getenv("VERSION", "0.1.0"),
            project_name=os.getenv("PROJECT_NAME", "dind-python-project"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "debug": self.debug,
            "env": self.env,
            "log_level": self.log_level,
            "use_gpu": self.use_gpu,
            "version": self.version,
            "project_name": self.project_name,
        }