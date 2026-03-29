"""
Configuration Manager Module
Handles loading and managing system configuration from JSON files.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Manages application configuration settings."""
    
    def __init__(self, config_path: str = None, logger: Optional[logging.Logger] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file. If None, uses default path.
            logger: Optional logger instance. If None, creates a default logger.
        """
        self.logger = logger or logging.getLogger(__name__)
        
        if config_path is None:
            # Default to config.json in the project root
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config.json"
        
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from JSON file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self.logger.info(f"Configuration loaded from {self.config_path}")
            else:
                # Create default configuration if file doesn't exist
                self.config = self._get_default_config()
                self.save_config()
                self.logger.info(f"Created default configuration at {self.config_path}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {e}")
            self.config = self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}", exc_info=True)
            self.config = self._get_default_config()
    
    def save_config(self) -> None:
        """Save current configuration to JSON file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            self.logger.debug(f"Configuration saved to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}", exc_info=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key path (e.g., 'system.app_name').
        
        Args:
            key: Configuration key path separated by dots.
            default: Default value if key not found.
            
        Returns:
            Configuration value or default.
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value by key path.
        
        Args:
            key: Configuration key path separated by dots.
            value: Value to set.
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration dictionary."""
        return {
            "system": {
                "app_name": "Lottery Analysis System",
                "version": "1.0.0",
                "language": "en"
            },
            "data": {
                "validity_period_days": 365,
                "max_records": 10000,
                "cache_enabled": True
            },
            "prediction": {
                "analysis_window": 30,
                "min_data_points": 10,
                "prediction_algorithms": ["frequency", "hot_cold", "pattern"],
                "confidence_threshold": 0.6
            },
            "ui": {
                "theme": "light",
                "window_width": 1200,
                "window_height": 800,
                "chart_style": "default"
            },
            "export": {
                "default_format": "csv",
                "include_statistics": True,
                "include_predictions": True
            },
            "security": {
                "password_length": 16,
                "password_include_special": True,
                "password_include_numbers": True,
                "password_include_uppercase": True
            }
        }
