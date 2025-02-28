"""
GitHub API interaction module for GitBrowse.
"""

import os
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
import requests
from bs4 import BeautifulSoup

from gitbrowse.api.utils import handle_rate_limit, cache_response

logger = logging.getLogger("gitbrowse.api.github")


class GitHubAPI:
    """GitHub API wrapper for GitBrowse."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize the GitHub API client.
        
        Args:
            token: Optional GitHub API token for authentication
        """
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.web_url = "https://github.com"
        self.raw_url = "https://raw.githubusercontent.com"
        self.cache_dir = os.path.join(os.getcwd(), "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Set up requests session with appropriate headers
        self.session = requests.Session()
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitBrowse/2.0"
        }
        
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        self.session.headers.update(headers)
    
    @handle_rate_limit
    @cache_response(timeout=3600)  # Cache for 1 hour
    def get_user_repositories(self, username: str) -> List[Dict[str, Any]]:
        """Get a list of repositories for a GitHub user.
        
        Args:
            username: GitHub username
            
        Returns:
            List of repository information dictionaries
        
        Raises:
            requests.RequestException: If the API request fails
        """
        # First try the API approach
        try:
            repositories = []
            page = 1
            
            while True:
                url = f"{self.base_url}/users/{username}/repos"
                params = {
                    "per_page": 100,
                    "page": page,
                    "sort": "updated"
                }
                
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                repos = response.json()
                if not repos:
                    break
                
                for repo in repos:
                    repositories.append({
                        "name": repo["name"],
                        "url": repo["html_url"],
                        "clone_url": repo["clone_url"],
                        "description": repo.get("description", ""),
                        "stars": repo["stargazers_count"],
                        "forks": repo["forks_count"],
                        "default_branch": repo["default_branch"],
                        "language": repo.get("language", ""),
                        "updated_at": repo["updated_at"]
                    })
                
                page += 1
            
            return repositories
            
        except requests.RequestException as e:
            logger.warning(f"API fetch failed, falling back to scraping: {str(e)}")
            # Fall back to web scraping if API fails
            return self._scrape_user_repositories(username)
    
    def _scrape_user_repositories(self, username: str) -> List[Dict[str, Any]]:
        """Scrape repositories from GitHub web interface.
        
        Args:
            username: GitHub username
            
        Returns:
            List of repository information dictionaries
        """
        repositories = []
        page = 1
        
        while True:
            url = f"{self.web_url}/{username}?tab=repositories&page={page}"
            response = self.session.get(url)
            
            if response.status_code == 404:
                # User not found
                return []
            
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find repository elements
            repo_elements = soup.findAll('h3', {'class': 'wb-break-all'})
            
            if not repo_elements:
                # No more repositories or no repositories found
                break
            
            for repo_element in repo_elements:
                name_element = repo_element.find('a')
                if name_element:
                    repo_name = name_element.text.strip()
                    repo_url = name_element['href']
                    
                    # Get stars and forks
                    stars, forks = self._scrape_repo_stats(repo_url)
                    
                    # Get default branch
                    default_branch = self._get_default_branch(username, repo_name)
                    
                    repositories.append({
                        "name": repo_name,
                        "url": f"{self.web_url}{repo_url}",
                        "clone_url": f"{self.web_url}{repo_url}.git",
                        "description": "",  # Not easily available from scraping
                        "stars": stars,
                        "forks": forks,
                        "default_branch": default_branch,
                        "language": "",  # Not easily available from scraping
                        "updated_at": ""  # Not easily available from scraping
                    })
            
            page += 1
        
        return repositories
    
    def _scrape_repo_stats(self, repo_url: str) -> Tuple[int, int]:
        """Scrape repository statistics (stars and forks).
        
        Args:
            repo_url: Repository URL path
            
        Returns:
            Tuple of (stars, forks)
        """
        url = f"{self.web_url}{repo_url}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get stars
            stars_element = soup.find('a', {'href': f'{repo_url}/stargazers'})
            stars = int(stars_element.text.strip().split()[0].replace(',', '')) if stars_element else 0
            
            # Get forks
            forks_element = soup.find('a', {'href': lambda href: href and "/forks" in href})
            forks = 0
            if forks_element:
                forks_text = forks_element.text.strip().split()[0].replace(',', '')
                try:
                    forks = int(forks_text)
                except ValueError:
                    pass
            
            return stars, forks
            
        except (requests.RequestException, ValueError, AttributeError) as e:
            logger.warning(f"Error scraping repo stats: {str(e)}")
            return 0, 0
    
    @handle_rate_limit
    @cache_response(timeout=3600)  # Cache for 1 hour
    def get_default_branch(self, username: str, repo_name: str) -> str:
        """Get the default branch for a repository.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            
        Returns:
            Default branch name
        """
        try:
            url = f"{self.base_url}/repos/{username}/{repo_name}"
            response = self.session.get(url)
            response.raise_for_status()
            repo_data = response.json()
            return repo_data.get('default_branch', 'main')
        except requests.RequestException as e:
            logger.warning(f"Error getting default branch: {str(e)}")
            return 'main'  # Default fallback
    
    def _get_default_branch(self, username: str, repo_name: str) -> str:
        """Internal method to get default branch with multiple strategies.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            
        Returns:
            Default branch name
        """
        # Try the API first
        try:
            return self.get_default_branch(username, repo_name)
        except Exception:
            # Fall back to scraping
            try:
                url = f"{self.web_url}/{username}/{repo_name}"
                response = self.session.get(url)
                response.raise_for_status()
                
                # Extract branch name from the branch selector button
                soup = BeautifulSoup(response.text, 'html.parser')
                branch_button = soup.find('summary', {'class': 'Button--secondary'})
                if branch_button:
                    branch_text = branch_button.text.strip()
                    return branch_text.split(':')[-1].strip()
            except Exception as e:
                logger.warning(f"Error scraping default branch: {str(e)}")
            
            return 'main'  # Default fallback
    
    @handle_rate_limit
    @cache_response(timeout=3600)  # Cache for 1 hour
    def get_repository_files(
        self, username: str, repo_name: str, branch: str = 'main', path: str = ''
    ) -> List[Dict[str, Any]]:
        """Get a list of files in a repository directory.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            branch: Branch name
            path: Directory path within the repository
            
        Returns:
            List of file information dictionaries
        """
        # Try API approach first
        try:
            url = f"{self.base_url}/repos/{username}/{repo_name}/contents/{path}"
            params = {"ref": branch}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            contents = response.json()
            files = []
            
            # Handle both array and single object responses
            if not isinstance(contents, list):
                contents = [contents]
                
            for item in contents:
                file_type = item["type"]  # "file" or "dir"
                name = item["name"]
                item_path = item["path"]
                download_url = item.get("download_url", "")
                
                files.append({
                    "name": name,
                    "path": item_path,
                    "type": file_type,  # Ensure this is "file" or "dir"
                    "url": download_url if file_type == "file" else "",
                    "size": item.get("size", 0),
                    "sha": item.get("sha", "")
                })
            
            # Sort: directories first, then files, both alphabetically
            return sorted(files, key=lambda x: (0 if x["type"] == "dir" else 1, x["name"].lower()))
            
        except requests.RequestException as e:
            logger.warning(f"API fetch failed, falling back to scraping: {str(e)}")
            # Fall back to web scraping
            return self._scrape_repository_files(username, repo_name, branch, path)
    
    def _scrape_repository_files(
        self, username: str, repo_name: str, branch: str = 'main', path: str = ''
    ) -> List[Dict[str, Any]]:
        """Scrape repository files from GitHub web interface.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            branch: Branch name
            path: Directory path within the repository
            
        Returns:
            List of file information dictionaries
        """
        files = []
        
        try:
            path_segment = f"/tree/{branch}/{path}" if path else f"/tree/{branch}"
            url = f"{self.web_url}/{username}/{repo_name}{path_segment}"
            
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find file and directory elements
            items = soup.find_all('tr', class_='react-directory-row')
            
            for item in items:
                icon = item.find('svg')
                file_type = "dir" if "icon-directory" in icon.get('class', []) else "file"
                
                link = item.find('a', class_='Link--primary')
                if link:
                    name = link.text.strip()
                    item_path = link['href'].split(f'/{username}/{repo_name}/')[1]
                    
                    # For files, construct a raw URL
                    download_url = ""
                    if file_type == "file":
                        raw_path = item_path.replace(f"blob/{branch}/", "")
                        download_url = f"{self.raw_url}/{username}/{repo_name}/{branch}/{raw_path.split('/', 1)[1] if '/' in raw_path else raw_path}"
                    
                    files.append({
                        "name": name,
                        "path": item_path.split('/', 2)[2] if len(item_path.split('/', 2)) > 2 else "",
                        "type": file_type,
                        "url": download_url if file_type == "file" else "",
                        "size": 0,  # Not easily available from scraping
                        "sha": ""  # Not easily available from scraping
                    })
            
            # Sort: directories first, then files, both alphabetically
            return sorted(files, key=lambda x: (0 if x["type"] == "dir" else 1, x["name"].lower()))
            
        except requests.RequestException as e:
            logger.warning(f"Error scraping repository files: {str(e)}")
            return []
    
    @handle_rate_limit
    @cache_response(timeout=3600)  # Cache for 1 hour
    def get_file_content(self, username: str, repo_name: str, path: str, branch: str = 'main') -> str:
        """Get the content of a file from a repository.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            path: File path within the repository
            branch: Branch name
                
        Returns:
            File content as string
        """
        try:
            # First try using the GitHub API to get the file content
            api_url = f"{self.base_url}/repos/{username}/{repo_name}/contents/{path}"
            params = {"ref": branch}
            
            logger.debug(f"Fetching file content API URL: {api_url}")
            response = self.session.get(api_url, params=params)
            response.raise_for_status()
            
            content_data = response.json()
            
            # GitHub API returns file content as base64 encoded string
            if "content" in content_data and content_data.get("encoding") == "base64":
                import base64
                content = base64.b64decode(content_data["content"]).decode("utf-8")
                return content
            
            # If not base64 encoded, try the download URL
            if "download_url" in content_data and content_data["download_url"]:
                download_url = content_data["download_url"]
                logger.debug(f"Using download URL: {download_url}")
                content_response = self.session.get(download_url)
                content_response.raise_for_status()
                return content_response.text
        
        except (requests.RequestException, ValueError, KeyError) as e:
            logger.warning(f"API method failed, trying raw URL: {str(e)}")
            
            # Fall back to raw URL
            try:
                # Try multiple branch variations if needed
                branches_to_try = [branch]
                if branch.lower() != "master":
                    branches_to_try.append("master")
                if branch.lower() != "main":
                    branches_to_try.append("main")
                    
                last_error = None
                for branch_name in branches_to_try:
                    try:
                        raw_url = f"{self.raw_url}/{username}/{repo_name}/{branch_name}/{path}"
                        logger.debug(f"Trying raw URL: {raw_url}")
                        raw_response = self.session.get(raw_url)
                        raw_response.raise_for_status()
                        return raw_response.text
                    except requests.RequestException as branch_error:
                        last_error = branch_error
                        continue
                        
                # If we tried all branches and still failed, try the web scraping approach
                html_url = f"{self.web_url}/{username}/{repo_name}/blob/{branch}/{path}"
                logger.debug(f"Trying web scraping: {html_url}")
                html_response = self.session.get(html_url)
                html_response.raise_for_status()
                
                # Parse the HTML to extract the file content
                soup = BeautifulSoup(html_response.text, 'html.parser')
                
                # Look for code content in the page
                code_element = soup.find('table', class_='highlight')
                if code_element:
                    lines = []
                    for line in code_element.find_all('tr'):
                        code_cell = line.find('td', class_='blob-code')
                        if code_cell:
                            lines.append(code_cell.get_text())
                    return '\n'.join(lines)
                    
                # If we couldn't parse the content, raise the last error
                if last_error:
                    raise last_error
                    
            except requests.RequestException as e:
                logger.error(f"Error getting file content: {str(e)}")
                return f"Error retrieving file content: {str(e)}"

        except Exception as e:
            logger.error(f"Unexpected error getting file content: {str(e)}")
            return f"Error retrieving file content: {str(e)}"
            
        return "Could not retrieve file content. The file may be binary or too large."
    
    def get_file_download_url(self, username: str, repo_name: str, path: str, branch: str = 'main') -> str:
        """Get the download URL for a file.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            path: File path within the repository
            branch: Branch name
            
        Returns:
            Download URL
        """
        return f"{self.raw_url}/{username}/{repo_name}/{branch}/{path}"
    
    @handle_rate_limit
    def get_directory_contents_recursive(
        self, username: str, repo_name: str, path: str = '', branch: str = 'main'
    ) -> List[Dict[str, Any]]:
        """Get all files in a directory recursively.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            path: Directory path within the repository
            branch: Branch name
            
        Returns:
            List of file information dictionaries
        """
        all_files = []
        
        try:
            # Get files in the current directory
            files = self.get_repository_files(username, repo_name, branch, path)
            
            for file_info in files:
                all_files.append(file_info)
                
                # If it's a directory, recursively get its contents
                if file_info["type"] == "dir":
                    subdir_path = file_info["path"]
                    subdir_files = self.get_directory_contents_recursive(
                        username, repo_name, subdir_path, branch
                    )
                    all_files.extend(subdir_files)
            
            return all_files
        except Exception as e:
            logger.error(f"Error getting directory contents recursively: {str(e)}")
            return []