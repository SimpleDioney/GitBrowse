"""
Repository service for GitBrowse.
"""

import os
import logging
import subprocess
from typing import List, Dict, Any, Optional, Tuple

from gitbrowse.api.github import GitHubAPI
from gitbrowse.services.network import NetworkService
from gitbrowse.services.downloader import DownloadService

logger = logging.getLogger("gitbrowse.services.repo")


class RepositoryService:
    """Service for handling repository operations."""
    
    def __init__(self, github_api: GitHubAPI, network_service: NetworkService):
        """Initialize the repository service.
        
        Args:
            github_api: GitHub API instance
            network_service: Network service instance
        """
        self.github_api = github_api
        self.network_service = network_service
        self.downloader = DownloadService()
    
    def get_user_repositories(self, username: str) -> List[Dict[str, Any]]:
        """Get repositories for a GitHub user.
        
        Args:
            username: GitHub username
            
        Returns:
            List of repository information dictionaries
        """
        if not self.network_service.is_connected():
            logger.warning("No internet connection to fetch repositories")
            return []
        
        try:
            return self.github_api.get_user_repositories(username)
        except Exception as e:
            logger.error(f"Error getting repositories for {username}: {str(e)}")
            return []
    
    def get_repository_files(
        self, username: str, repo_name: str, branch: str = 'main', path: str = ''
    ) -> List[Dict[str, Any]]:
        """Get files in a repository directory.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            branch: Branch name
            path: Directory path within the repository
            
        Returns:
            List of file information dictionaries
        """
        if not self.network_service.is_connected():
            logger.warning("No internet connection to fetch repository files")
            return []
        
        try:
            # Double check the branch name if it's the initial request
            if not path and branch in ['main', 'master']:
                try:
                    actual_branch = self.github_api.get_default_branch(username, repo_name)
                    if actual_branch and actual_branch != branch:
                        logger.info(f"Using actual default branch: {actual_branch} instead of {branch}")
                        branch = actual_branch
                except Exception as e:
                    logger.warning(f"Could not verify default branch: {str(e)}")
            
            return self.github_api.get_repository_files(username, repo_name, branch, path)
        except Exception as e:
            logger.error(f"Error getting files for {username}/{repo_name}: {str(e)}")
            return []
    
    def get_file_content(
        self, username: str, repo_name: str, path: str, branch: str = 'main'
    ) -> str:
        """Get the content of a file from a repository.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            path: File path within the repository
            branch: Branch name
            
        Returns:
            File content as string
        """
        if not self.network_service.is_connected():
            logger.warning("No internet connection to fetch file content")
            return "Cannot fetch file content: No internet connection"
        
        try:
            return self.github_api.get_file_content(username, repo_name, path, branch)
        except Exception as e:
            logger.error(f"Error getting file content: {str(e)}")
            return f"Error retrieving file content: {str(e)}"
    
    def download_file(self, url: str, destination: str) -> bool:
        """Download a file from a URL.
        
        Args:
            url: File URL
            destination: Destination path
            
        Returns:
            True if successful, False otherwise
        """
        if not self.network_service.is_connected():
            logger.warning("No internet connection to download file")
            return False
        
        try:
            # Ensure download directory exists
            os.makedirs(os.path.dirname(os.path.abspath(destination)), exist_ok=True)
            
            # Queue the download
            task_id = self.downloader.download_file(url, destination)
            
            # Wait for the download to complete
            return self.downloader.wait_for_downloads([task_id])
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            return False
    
    def download_directory(
        self, username: str, repo_name: str, path: str, destination: str, branch: str = 'main'
    ) -> bool:
        """Download a directory from a repository.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            path: Directory path within the repository
            destination: Destination path
            branch: Branch name
            
        Returns:
            True if successful, False otherwise
        """
        if not self.network_service.is_connected():
            logger.warning("No internet connection to download directory")
            return False
        
        try:
            # Get all files in the directory recursively
            all_files = self.github_api.get_directory_contents_recursive(
                username, repo_name, path, branch
            )
            
            # Filter out directories, we only need to download files
            file_list = [f for f in all_files if f.get("type") == "file"]
            
            # Prepare file info for downloading
            download_files = []
            for file_info in file_list:
                rel_path = file_info.get("path", "")
                if rel_path.startswith(path):
                    rel_path = rel_path[len(path):].lstrip('/')
                
                download_files.append({
                    "url": file_info.get("url", ""),
                    "path": os.path.join(rel_path)
                })
            
            # Queue all files for download
            task_ids = self.downloader.download_files(download_files, destination)
            
            # Wait for all downloads to complete
            return self.downloader.wait_for_downloads(task_ids)
        except Exception as e:
            logger.error(f"Error downloading directory: {str(e)}")
            return False
    
    def clone_repository(
        self, username: str, repo_name: str, clone_url: Optional[str] = None
    ) -> bool:
        """Clone a repository.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            clone_url: Optional clone URL
            
        Returns:
            True if successful, False otherwise
        """
        if not self.network_service.is_connected():
            logger.warning("No internet connection to clone repository")
            return False
        
        try:
            # Construct the clone URL if not provided
            if not clone_url:
                clone_url = f"https://github.com/{username}/{repo_name}.git"
            
            # Create repositories directory if it doesn't exist
            repos_dir = os.path.join(os.getcwd(), "repositories")
            os.makedirs(repos_dir, exist_ok=True)
            
            # Clone the repository
            dest_path = os.path.join(repos_dir, repo_name)
            
            # Check if the repository already exists
            if os.path.exists(dest_path):
                logger.warning(f"Repository directory {dest_path} already exists")
                try:
                    # Try to update the repository instead
                    subprocess.run(
                        ["git", "pull"], 
                        cwd=dest_path, 
                        check=True, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE
                    )
                    logger.info(f"Updated existing repository at {dest_path}")
                    return True
                except subprocess.CalledProcessError as e:
                    logger.error(f"Error updating repository: {str(e)}")
                    return False
            
            # Clone the repository
            subprocess.run(
                ["git", "clone", clone_url, dest_path], 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            logger.info(f"Successfully cloned repository to {dest_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error cloning repository: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error cloning repository: {str(e)}")
            return False