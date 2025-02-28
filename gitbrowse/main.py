#!/usr/bin/env python3
"""
Main entry point for the GitBrowse application.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional

from gitbrowse.config import Config
from gitbrowse.ui.display import Display
from gitbrowse.services.network import NetworkService
from gitbrowse.services.repo import RepositoryService
from gitbrowse.ui.messages import Messages
from gitbrowse.api.github import GitHubAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("gitbrowse.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("gitbrowse")


class GitBrowse:
    """Main application class for GitBrowse."""

    def __init__(self) -> None:
        """Initialize the GitBrowse application."""
        self.config = Config()
        self.language = self.config.get_language()
        self.messages = Messages(self.language)
        self.display = Display(self.messages)
        self.network = NetworkService()
        self.github_api = GitHubAPI()
        self.repo_service = RepositoryService(self.github_api, self.network)

    def setup(self) -> None:
        """Set up the application environment."""
        # Ensure needed directories exist
        os.makedirs("downloads", exist_ok=True)
        os.makedirs("repositories", exist_ok=True)
        os.makedirs("cache", exist_ok=True)

    def run(self) -> None:
        """Run the main application loop."""
        self.setup()
        while True:  # Main app loop
            self.display.clear_screen()
            self.display.show_welcome()

            # Check for internet connection
            if not self.network.is_connected():
                self.display.show_no_internet_warning()

            # Show main menu
            choice = self.display.show_main_menu()
            
            if choice == '1':  # Browse repositories
                try:
                    self.browse_repositories_flow()
                except KeyboardInterrupt:
                    self.display.show_message(self.messages.get("operation_cancelled"))
                except Exception as e:
                    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
                    self.display.show_error(f"{self.messages.get('error')}: {str(e)}")
                    input(self.messages.get("press_enter"))
            elif choice == '2':  # Change language
                self.change_language()
            elif choice == '3':  # Exit
                break
            else:
                self.display.show_error(self.messages.get("invalid_option"))
                input(self.messages.get("press_enter"))
        
        self.display.show_message(self.messages.get("goodbye"))
    
    def browse_repositories_flow(self) -> None:
        """Flow for browsing repositories."""
        # Get username
        username = self.display.prompt_for_username()
        
        # Fetch repositories
        self.display.show_message(
            self.messages.get("searching_user").format(username=username)
        )
        
        repositories = self.repo_service.get_user_repositories(username)
        
        if not repositories:
            self.display.show_error(self.messages.get("user_not_found"))
            input(self.messages.get("press_enter"))
            return
        
        # Display repository browser
        self.browse_repositories(username, repositories)

    def change_language(self) -> None:
        """Allow the user to change the application language."""
        self.display.clear_screen()
        self.display.show_language_menu()
        
        choice = input(self.display.style_prompt(self.messages.get("choose_language")))
        
        if choice == '1' and self.language != 'en':
            self.language = 'en'
            self.config.set_language('en')
            self.messages = Messages('en')
            self.display = Display(self.messages)
            self.display.show_success(self.messages.get("language_changed"))
        elif choice == '2' and self.language != 'pt':
            self.language = 'pt'
            self.config.set_language('pt')
            self.messages = Messages('pt')
            self.display = Display(self.messages)
            self.display.show_success(self.messages.get("language_changed"))
        else:
            self.display.show_message(self.messages.get("no_change"))
        
        input(self.messages.get("press_enter"))

    def browse_repositories(self, username: str, repositories: list) -> None:
        """Browse and interact with user repositories.
        
        Args:
            username: GitHub username
            repositories: List of repository objects
        """
        current_page = 0
        repos_per_page = 10
        total_pages = (len(repositories) + repos_per_page - 1) // repos_per_page
        
        while True:
            self.display.clear_screen()
            self.display.show_internet_status(self.network.is_connected())
            
            # Calculate page bounds
            start = current_page * repos_per_page
            end = min(start + repos_per_page, len(repositories))
            
            # Display repositories for current page
            self.display.show_repository_list(
                username, repositories[start:end], current_page, total_pages
            )
            
            # Get user choice
            choice = self.display.prompt_for_repository_choice()
            
            # Handle pagination
            if choice == 'p' and current_page < total_pages - 1:
                current_page += 1
                continue
            elif choice == 'n' and current_page > 0:
                current_page -= 1
                continue
            elif choice == 'b':
                return
            
            # Handle repository selection
            try:
                repo_index = int(choice) - 1 + start
                if 0 <= repo_index < len(repositories):
                    self.repository_actions(username, repositories[repo_index])
                else:
                    self.display.show_error(self.messages.get("invalid_option"))
            except ValueError:
                self.display.show_error(self.messages.get("invalid_option"))

    def repository_actions(self, username: str, repository: Dict[str, Any]) -> None:
        """Handle actions for a selected repository.
        
        Args:
            username: GitHub username
            repository: Repository data dictionary
        """
        while True:
            self.display.clear_screen()
            self.display.show_repository_actions(repository["name"])
            
            action = self.display.prompt_for_action()
            
            if action == '1':  # View files
                if self.network.is_connected():
                    # Get the default branch
                    default_branch = repository.get("default_branch", "main")
                    
                    files = self.repo_service.get_repository_files(
                        username, repository["name"], default_branch
                    )
                    self.browse_files(username, repository["name"], files, default_branch)
                else:
                    self.display.show_error(self.messages.get("need_internet_for_files"))
            elif action == '2':  # Clone repository
                if self.network.is_connected():
                    self.repo_service.clone_repository(
                        username, repository["name"], repository.get("clone_url")
                    )
                    self.display.show_success(
                        self.messages.get("repo_cloned").format(repo_name=repository["name"])
                    )
                    input(self.messages.get("press_enter"))
                else:
                    self.display.show_error(self.messages.get("need_internet_for_clone"))
            elif action.lower() == 'b':
                return
            else:
                self.display.show_error(self.messages.get("invalid_option"))

    def browse_files(self, username: str, repo_name: str, files: list, default_branch: str) -> None:
        """Browse and interact with repository files.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            files: List of file objects
            default_branch: Default branch of the repository
        """
        while True:  # Add a loop here to continuously display files until user exits
            self.display.clear_screen()
            self.display.show_file_list(username, repo_name, files)
            
            choice = self.display.prompt_for_file_choice()
            
            if choice.lower() == 'b':
                return  # Exit the file browser and return to repository view
                    
            try:
                file_index = int(choice) - 1
                if 0 <= file_index < len(files):
                    file_info = files[file_index]
                    self.file_actions(username, repo_name, file_info, default_branch)
                    # No return here, so it will loop back and show the file list again
                else:
                    self.display.show_error(self.messages.get("invalid_file_number"))
                    input(self.messages.get("press_enter"))  # Wait for user acknowledgment
            except ValueError:
                self.display.show_error(self.messages.get("invalid_option"))
                input(self.messages.get("press_enter"))  # Wait for user acknowledgment

    def file_actions(self, username: str, repo_name: str, file_info: Dict[str, Any], default_branch: str) -> None:
        """Handle actions for a selected file.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            file_info: File information dictionary
            default_branch: Default branch of the repository
        """
        file_name = file_info.get("name", "")
        file_path = file_info.get("path", "")
        file_type = file_info.get("type", "").lower()
        file_url = file_info.get("url", "")
        
        # Determine if this is a directory
        is_directory = file_type in ["dir", "directory", "folder"]
        
        while True:
            self.display.clear_screen()
            self.display.show_file_actions(file_name, "directory" if is_directory else "file")
            
            action = self.display.prompt_for_file_action()
            
            if action.lower() == 'b':
                return  # Return to file list
            
            if action.lower() == 'v':
                if is_directory:
                    # If it's a directory, list its contents
                    self.display.show_message(f"Fetching contents of {file_name}...")
                    sub_files = self.repo_service.get_repository_files(
                        username, repo_name, default_branch, file_path
                    )
                    if sub_files:
                        self.browse_files(username, f"{repo_name}/{file_name}", sub_files, default_branch)
                        return  # Return to previous level after browsing subdirectory
                    else:
                        self.display.show_message(f"Directory {file_name} is empty.")
                        input(self.messages.get("press_enter"))
                else:
                    # If it's a regular file, show its content
                    content = self.repo_service.get_file_content(username, repo_name, file_path)
                    self.display.show_file_content(file_name, content)
                    
                    # Ask if user wants to download after viewing
                    if self.display.confirm_download():
                        self.repo_service.download_file(file_url, os.path.join("downloads", file_name))
                        self.display.show_success(
                            self.messages.get("file_downloaded").format(file_name=file_name)
                        )
                    
                    input(self.messages.get("press_enter"))  # Wait for user to read content
                
            elif action.lower() == 'd':
                if is_directory:
                    # Directory download
                    if self.display.confirm_download():
                        self.display.show_message(f"Downloading directory {file_name}...")
                        self.repo_service.download_directory(
                            username, repo_name, file_path, os.path.join("downloads", file_name), default_branch
                        )
                        self.display.show_success(
                            self.messages.get("dir_downloaded").format(dir_name=file_name)
                        )
                else:
                    # File download
                    self.display.show_message(f"Downloading file {file_name}...")
                    self.repo_service.download_file(file_url, os.path.join("downloads", file_name))
                    self.display.show_success(
                        self.messages.get("file_downloaded").format(file_name=file_name)
                    )
                
                input(self.messages.get("press_enter"))  # Wait for user acknowledgment
                
            else:
                self.display.show_error(self.messages.get("invalid_option"))
                input(self.messages.get("press_enter"))  # Wait for user acknowledgment


def main() -> None:
    """Entry point for the GitBrowse application."""
    app = GitBrowse()
    app.run()


if __name__ == "__main__":
    main()