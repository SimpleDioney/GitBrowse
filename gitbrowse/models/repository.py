"""
Repository data model for GitBrowse.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import datetime
from gitbrowse.models.file import File


@dataclass
class Repository:
    """Repository data model."""
    
    name: str
    owner: str
    url: str
    clone_url: str
    default_branch: str = "main"
    description: str = ""
    stars: int = 0
    forks: int = 0
    language: str = ""
    updated_at: Optional[datetime.datetime] = None
    files: List[File] = field(default_factory=list)
    private: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Repository":
        """Create a Repository instance from a dictionary.
        
        Args:
            data: Dictionary with repository data
            
        Returns:
            Repository instance
        """
        # Convert updated_at string to datetime if present
        updated_at = None
        if "updated_at" in data and data["updated_at"]:
            try:
                updated_at = datetime.datetime.fromisoformat(
                    data["updated_at"].replace("Z", "+00:00")
                )
            except (ValueError, TypeError):
                pass
        
        # Extract owner from URL if not provided
        owner = data.get("owner", "")
        if not owner and "/" in data.get("url", ""):
            parts = data["url"].split("/")
            if len(parts) > 3:
                owner = parts[-2]
        
        return cls(
            name=data.get("name", ""),
            owner=owner,
            url=data.get("url", ""),
            clone_url=data.get("clone_url", ""),
            default_branch=data.get("default_branch", "main"),
            description=data.get("description", ""),
            stars=data.get("stars", 0),
            forks=data.get("forks", 0),
            language=data.get("language", ""),
            updated_at=updated_at,
            private=data.get("private", False)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the Repository instance to a dictionary.
        
        Returns:
            Dictionary representation
        """
        result = {
            "name": self.name,
            "owner": self.owner,
            "url": self.url,
            "clone_url": self.clone_url,
            "default_branch": self.default_branch,
            "description": self.description,
            "stars": self.stars,
            "forks": self.forks,
            "language": self.language,
            "private": self.private
        }
        
        if self.updated_at:
            result["updated_at"] = self.updated_at.isoformat()
        
        return result
    
    def add_file(self, file: File) -> None:
        """Add a file to the repository.
        
        Args:
            file: File instance
        """
        self.files.append(file)
    
    def get_file(self, path: str) -> Optional[File]:
        """Get a file by path.
        
        Args:
            path: File path
            
        Returns:
            File instance or None if not found
        """
        for file in self.files:
            if file.path == path:
                return file
        return None
    
    @property
    def full_name(self) -> str:
        """Get the full repository name (owner/repo).
        
        Returns:
            Full repository name
        """
        return f"{self.owner}/{self.name}"
    
    def __str__(self) -> str:
        """Get a string representation of the repository.
        
        Returns:
            String representation
        """
        return f"{self.full_name} ({self.stars}★, {self.forks}⑂)"