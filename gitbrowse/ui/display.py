"""
Terminal display utilities for the GitBrowse application.
"""

import os
import sys
import time
from typing import List, Dict, Any, Optional

from gitbrowse.ui.styles import (
    logo, BOX_STYLES, style_repo_name, style_stats, style_file_name,
    style_prompt, error_message, success_message, info_message,
    warning_message, format_title, RESET, WHITE, HEADER, SUCCESS, ERROR
)
from gitbrowse.ui.messages import Messages
from gitbrowse.utils.system import get_clear_command

from pygments import highlight
from pygments.lexers import guess_lexer_for_filename, TextLexer
from pygments.formatters import TerminalFormatter
from pygments.util import ClassNotFound


class Display:
    """Class to handle terminal display operations."""
    
    def __init__(self, messages: Messages):
        """Initialize the display with messages.
        
        Args:
            messages: Messages instance for internationalization
        """
        self.messages = messages
        self.clear_cmd = get_clear_command()
        self.terminal_width = self._get_terminal_width()
        self.last_status_message = None
    
    def _get_terminal_width(self) -> int:
        """Get the terminal width.
        
        Returns:
            Terminal width in characters
        """
        try:
            return os.get_terminal_size().columns
        except (AttributeError, OSError):
            return 80
    
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system(self.clear_cmd)
    
    def show_welcome(self) -> None:
        """Display the welcome screen with logo."""
        print(logo())
        print(BOX_STYLES["header"])
        print(info_message(self.messages.get("welcome")))
        print(BOX_STYLES["footer"])
        print()
    
    def show_message(self, message: str) -> None:
        """Display a message to the user.
        
        Args:
            message: Message to display
        """
        print(message)
    
    def show_error(self, message: str) -> None:
        """Display an error message.
        
        Args:
            message: Error message to display
        """
        print(error_message(message))
    
    def show_success(self, message: str) -> None:
        """Display a success message.
        
        Args:
            message: Success message to display
        """
        print(success_message(message))
    
    def show_info(self, message: str) -> None:
        """Display an info message.
        
        Args:
            message: Info message to display
        """
        print(info_message(message))
    
    def show_warning(self, message: str) -> None:
        """Display a warning message.
        
        Args:
            message: Warning message to display
        """
        print(warning_message(message))
    
    def show_no_internet_warning(self) -> None:
        """Display a warning about no internet connection."""
        self.show_warning(self.messages.get("no_internet"))
    
    def show_internet_status(self, connected: bool) -> None:
        """Display internet connection status if it changed.
        
        Args:
            connected: Whether internet is connected
        """
        if self.last_status_message != connected:
            if connected:
                self.show_success(self.messages.get("internet_established"))
            else:
                self.show_warning(self.messages.get("no_internet"))
            self.last_status_message = connected
    
    def prompt_for_username(self) -> str:
        """Prompt the user for a GitHub username.
        
        Returns:
            GitHub username
        """
        return input(style_prompt(self.messages.get("username_prompt")))
    
    def prompt_for_repository_choice(self) -> str:
        """Prompt the user for a repository choice.
        
        Returns:
            User's choice
        """
        return input(style_prompt(self.messages.get("choose_action")))
    
    def prompt_for_action(self) -> str:
        """Prompt the user for an action.
        
        Returns:
            User's choice
        """
        return input(style_prompt(self.messages.get("choose_action")))
    
    def prompt_for_file_choice(self) -> str:
        """Prompt the user for a file choice.
        
        Returns:
            User's choice
        """
        return input(style_prompt(self.messages.get("choose_file")))
    
    def prompt_for_file_action(self) -> str:
        """Prompt the user for a file action.
        
        Returns:
            User's choice
        """
        return input(style_prompt(self.messages.get("choose_action")))
    
    def confirm_download(self) -> bool:
        """Confirm if the user wants to download a file.
        
        Returns:
            True if confirmed, False otherwise
        """
        response = input(style_prompt(self.messages.get("download_prompt"))).lower()
        return response in ['y', 'yes', 's', 'sim']
    

    def show_main_menu(self) -> str:
        """Display the main menu and get user choice.
        
        Returns:
            User's choice
        """
        print(f"\n{BOX_STYLES['separator']}")
        print(self.messages.get("main_menu"))
        print(f"{BOX_STYLES['separator']}\n")
        
        return self.prompt_for_action()  # Use existing prompt method instead

    def style_prompt(self, text: str) -> str:
        """Style a prompt message.
        
        Args:
            text: Message text
            
        Returns:
            Styled prompt
        """
        return style_prompt(text)

    def show_language_menu(self) -> None:
        """Display the language selection menu."""
        print(f"\n{BOX_STYLES['separator']}")
        print(self.messages.get("language_menu"))
        print(f"{BOX_STYLES['separator']}\n")
    
    def show_repository_list(
        self, username: str, repositories: List[Dict[str, Any]], 
        current_page: int, total_pages: int
    ) -> None:
        """Display a list of repositories with pagination.
        
        Args:
            username: GitHub username
            repositories: List of repository information
            current_page: Current page number (0-based)
            total_pages: Total number of pages
        """
        print(format_title(f"{username}'s Repositories"))
        
        for i, repo in enumerate(repositories):
            # Get repository stats
            name = repo.get("name", "Unknown")
            stars = repo.get("stars", 0)
            forks = repo.get("forks", 0)
            
            # Format and display repository information
            print(f"{i + 1}. {style_repo_name(name)} {style_stats(stars, forks)}")
        
        print(f"\n{WHITE}Page {current_page + 1}/{total_pages}{RESET}")
        print(self.messages.get("page_instructions"))
        print()
    
    def show_repository_actions(self, repo_name: str) -> None:
        """Display available actions for a repository.
        
        Args:
            repo_name: Repository name
        """
        print(format_title(repo_name))
        print(self.messages.get("repo_options").format(repo_name=repo_name))
    
    def show_file_list(
        self, username: str, repo_name: str, files: List[Dict[str, Any]]
    ) -> None:
        """Display a list of files in a repository.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            files: List of file information
        """
        print(format_title(f"{username}/{repo_name}"))
        
        for i, file_info in enumerate(files):
            name = file_info.get("name", "Unknown")
            file_type = file_info.get("type", "file").lower()
            
            print(f"{i + 1}. {style_file_name(name, file_type)}")
        
        print()
    
    def show_file_actions(self, file_name: str, file_type: str) -> None:
        """Display available actions for a file.
        
        Args:
            file_name: File name
            file_type: File type (file/directory)
        """
        print(format_title(file_name))
        
        # Customize options based on file type
        if file_type.lower() in ["dir", "directory", "folder"]:
            print(self.messages.get("directory_options").format(dir_name=file_name))
        else:
            print(self.messages.get("file_options").format(file_name=file_name))
    
    def show_file_content(self, file_name: str, content: str) -> None:
        """Display file content with syntax highlighting.
        
        Args:
            file_name: File name
            content: File content
        """
        self.clear_screen()
        print(format_title(file_name))
        
        try:
            # Try to guess the lexer based on the file name
            lexer = guess_lexer_for_filename(file_name, content)
        except ClassNotFound:
            lexer = TextLexer()  # Default to plain text
        
        formatter = TerminalFormatter()
        highlighted_content = highlight(content, lexer, formatter)
        
        print(highlighted_content)
        print()
    
    def show_progress(self, message: str, progress: float) -> None:
        """Display a progress bar.
        
        Args:
            message: Progress message
            progress: Progress value (0.0 - 1.0)
        """
        bar_width = min(self.terminal_width - 20, 50)
        filled_width = int(progress * bar_width)
        
        bar = f"[{'#' * filled_width}{' ' * (bar_width - filled_width)}]"
        percent = int(progress * 100)
        
        sys.stdout.write(f"\r{message}: {bar} {percent}%")
        sys.stdout.flush()
        
        if progress >= 1.0:
            sys.stdout.write("\n")