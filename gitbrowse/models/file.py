"""
File data model for GitBrowse.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class File:
    """File data model."""
    
    name: str
    path: str
    type: str  # "file" or "dir"
    url: str = ""
    size: int = 0
    sha: str = ""
    content: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "File":
        """Create a File instance from a dictionary.
        
        Args:
            data: Dictionary with file data
            
        Returns:
            File instance
        """
        return cls(
            name=data.get("name", ""),
            path=data.get("path", ""),
            type=data.get("type", "file"),
            url=data.get("url", ""),
            size=data.get("size", 0),
            sha=data.get("sha", ""),
            content=data.get("content", "")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the File instance to a dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "path": self.path,
            "type": self.type,
            "url": self.url,
            "size": self.size,
            "sha": self.sha
        }
    
    @property
    def is_directory(self) -> bool:
        """Check if the file is a directory.
        
        Returns:
            True if the file is a directory, False otherwise
        """
        return self.type.lower() in ["dir", "directory"]
    
    @property
    def is_file(self) -> bool:
        """Check if the file is a regular file.
        
        Returns:
            True if the file is a regular file, False otherwise
        """
        return not self.is_directory
    
    @property
    def extension(self) -> str:
        """Get the file extension.
        
        Returns:
            File extension
        """
        if self.is_directory:
            return ""
        
        parts = self.name.split(".")
        return parts[-1] if len(parts) > 1 else ""
    
    def get_download_path(self, base_dir: str = "downloads") -> str:
        """Get the local download path for the file.
        
        Args:
            base_dir: Base directory for downloads
            
        Returns:
            Local file path
        """
        import os
        return os.path.join(base_dir, self.path)
    
    def __str__(self) -> str:
        """Get a string representation of the file.
        
        Returns:
            String representation
        """
        type_icon = "📁" if self.is_directory else "📄"
        return f"{type_icon} {self.name}"