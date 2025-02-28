"""
Configuration management for GitBrowse.
"""

import os
import json
import logging
from typing import Any, Dict, Optional, Union

logger = logging.getLogger("gitbrowse.config")

# Default configuration values
DEFAULT_CONFIG = {
    "language": "en",
    "cache_timeout": 3600,  # 1 hour in seconds
    "max_concurrent_downloads": 5,
    "connection_check_interval": 30,  # seconds
    "theme": "default",
    "github_token": None,
}


class Config:
    """Configuration manager for GitBrowse."""
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default.
        
        Returns:
            Configuration dictionary
        """
        config = DEFAULT_CONFIG.copy()
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    
                    # Update configuration with loaded values
                    config.update(loaded_config)
            else:
                # Create default configuration file
                self._save_config(config)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error loading configuration: {str(e)}")
            
            # If config file is corrupted, create a new one
            self._save_config(config)
        
        return config
    
    def _save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except IOError as e:
            logger.error(f"Error saving configuration: {str(e)}")
            return False
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Set a configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        self.config[key] = value
        return self._save_config(self.config)
    
    def get_language(self) -> str:
        """Get the current language setting.
        
        Returns:
            Language code
        """
        return self.get("language", "en")
    
    def set_language(self, language: str) -> bool:
        """Set the language.
        
        Args:
            language: Language code
            
        Returns:
            True if successful, False otherwise
        """
        return self.set("language", language)
    
    def get_github_token(self) -> Optional[str]:
        """Get the GitHub API token.
        
        Returns:
            GitHub API token or None
        """
        # Check environment variable first
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            return token
        
        # Fall back to config file
        return self.get("github_token")
    
    def set_github_token(self, token: str) -> bool:
        """Set the GitHub API token.
        
        Args:
            token: GitHub API token
            
        Returns:
            True if successful, False otherwise
        """
        return self.set("github_token", token)