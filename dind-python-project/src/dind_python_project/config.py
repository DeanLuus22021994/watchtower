"""Configuration handling for the application."""

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AppConfig:
    """Application configuration settings."""

    debug: bool = False
    env: str = "development"
    log_level: str = "INFO"
    use_gpu: bool = False

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create configuration from environment variables."""
        return cls(
            debug=os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"),
            env=os.getenv("ENV", "development"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            use_gpu=os.getenv("USE_GPU", "False").lower() in ("true", "1", "yes"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "debug": self.debug,
            "env": self.env,
            "log_level": self.log_level,
            "use_gpu": self.use_gpu,
        }