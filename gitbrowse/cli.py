"""
Command-line interface for GitBrowse.
"""

import os
import sys
import logging
import argparse
from typing import Optional, List, Dict, Any

from gitbrowse.config import Config
from gitbrowse.api.github import GitHubAPI
from gitbrowse.services.network import NetworkService
from gitbrowse.services.repo import RepositoryService
from gitbrowse.ui.messages import Messages
from gitbrowse.ui.display import Display
from gitbrowse.utils.system import check_git_installed, open_file_with_default_app

logger = logging.getLogger("gitbrowse.cli")


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration.
    
    Args:
        verbose: Whether to enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("gitbrowse.log"),
            logging.StreamHandler(sys.stdout) if verbose else logging.NullHandler()
        ]
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="GitBrowse - Browse GitHub repositories from your terminal"
    )
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Browse command
    browse_parser = subparsers.add_parser("browse", help="Browse repositories interactively")
    browse_parser.add_argument("username", nargs="?", help="GitHub username to browse")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List repositories for a user")
    list_parser.add_argument("username", help="GitHub username")
    list_parser.add_argument("--count", "-c", type=int, default=10, help="Number of repositories to show")
    
    # View command
    view_parser = subparsers.add_parser("view", help="View a file from a repository")
    view_parser.add_argument("repo", help="Repository in format username/repo")
    view_parser.add_argument("path", help="Path to the file")
    view_parser.add_argument("--branch", "-b", default=None, help="Branch name")
    
    # Download command
    download_parser = subparsers.add_parser("download", help="Download a file from a repository")
    download_parser.add_argument("repo", help="Repository in format username/repo")
    download_parser.add_argument("path", help="Path to the file or directory")
    download_parser.add_argument("--output", "-o", help="Output path")
    download_parser.add_argument("--branch", "-b", default=None, help="Branch name")
    
    # Clone command
    clone_parser = subparsers.add_parser("clone", help="Clone a repository")
    clone_parser.add_argument("repo", help="Repository in format username/repo")
    clone_parser.add_argument("--output", "-o", help="Output directory")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Configure GitBrowse")
    config_parser.add_argument("--language", "-l", choices=["en", "pt"], help="Set language")
    config_parser.add_argument("--token", "-t", help="Set GitHub API token")
    
    # General options
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    return parser.parse_args()


def extract_repo_parts(repo_arg: str) -> tuple:
    """Extract username and repository name from a repo argument.
    
    Args:
        repo_arg: Repository argument in format username/repo
        
    Returns:
        Tuple of (username, repo_name)
    """
    parts = repo_arg.split("/", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid repository format: {repo_arg}. Expected format: username/repo")
    
    return parts[0], parts[1]


def cmd_browse(args: argparse.Namespace, services: Dict[str, Any]) -> int:
    """Handle the browse command.
    
    Args:
        args: Parsed arguments
        services: Dictionary of service instances
        
    Returns:
        Exit code
    """
    # Start the interactive browser in browse mode
    from gitbrowse.main import GitBrowse
    app = GitBrowse()
    
    # If username is provided, go directly to repository browsing
    if args.username:
        app.setup()
        app.display.show_welcome()
        
        if not app.network.is_connected():
            app.display.show_no_internet_warning()
        
        app.display.show_message(
            app.messages.get("searching_user").format(username=args.username)
        )
        
        repositories = app.repo_service.get_user_repositories(args.username)
        
        if not repositories:
            app.display.show_error(app.messages.get("user_not_found"))
            return 1
        
        app.browse_repositories(args.username, repositories)
        app.display.show_message(app.messages.get("goodbye"))
    else:
        # Start the interactive browser normally
        app.run()
    
    return 0


def cmd_list(args: argparse.Namespace, services: Dict[str, Any]) -> int:
    """Handle the list command.
    
    Args:
        args: Parsed arguments
        services: Dictionary of service instances
        
    Returns:
        Exit code
    """
    display = services["display"]
    repo_service = services["repo_service"]
    
    username = args.username
    count = args.count
    
    display.show_message(f"Fetching repositories for {username}...")
    
    repos = repo_service.get_user_repositories(username)
    
    if not repos:
        display.show_error(f"No repositories found for {username}")
        return 1
    
    # Show the repositories
    display.clear_screen()
    display.show_message(f"Found {len(repos)} repositories for {username}")
    print()
    
    # Show up to count repositories
    for i, repo in enumerate(repos[:count]):
        stars = repo.get("stars", 0)
        forks = repo.get("forks", 0)
        description = repo.get("description", "")
        
        display.show_message(f"{i + 1}. {repo['name']} - ★ {stars}, ⑂ {forks}")
        if description:
            display.show_message(f"   {description}")
    
    return 0


def cmd_view(args: argparse.Namespace, services: Dict[str, Any]) -> int:
    """Handle the view command.
    
    Args:
        args: Parsed arguments
        services: Dictionary of service instances
        
    Returns:
        Exit code
    """
    display = services["display"]
    repo_service = services["repo_service"]
    github_api = services["github_api"]
    
    try:
        username, repo_name = extract_repo_parts(args.repo)
    except ValueError as e:
        display.show_error(str(e))
        return 1
    
    file_path = args.path
    branch = args.branch
    
    # If branch is not specified, get the default branch
    if not branch:
        branch = github_api.get_default_branch(username, repo_name)
    
    display.show_message(f"Fetching file {file_path} from {username}/{repo_name}...")
    
    # Get the file content
    content = repo_service.get_file_content(username, repo_name, file_path, branch)
    
    # Show the file content
    display.clear_screen()
    display.show_file_content(file_path, content)
    
    return 0


def cmd_download(args: argparse.Namespace, services: Dict[str, Any]) -> int:
    """Handle the download command.
    
    Args:
        args: Parsed arguments
        services: Dictionary of service instances
        
    Returns:
        Exit code
    """
    display = services["display"]
    repo_service = services["repo_service"]
    github_api = services["github_api"]
    
    try:
        username, repo_name = extract_repo_parts(args.repo)
    except ValueError as e:
        display.show_error(str(e))
        return 1
    
    file_path = args.path
    output_path = args.output
    branch = args.branch
    
    # If branch is not specified, get the default branch
    if not branch:
        branch = github_api.get_default_branch(username, repo_name)
    
    # Check if it's a file or directory
    try:
        # Try to get file content to check if it's a file
        github_api.get_file_content(username, repo_name, file_path, branch)
        is_file = True
    except Exception:
        # If not a file, assume it's a directory
        is_file = False
    
    if is_file:
        display.show_message(f"Downloading file {file_path} from {username}/{repo_name}...")
        
        # If output path is not specified, use the file name
        if not output_path:
            output_path = os.path.join("downloads", file_path)
        
        # Get the download URL
        download_url = github_api.get_file_download_url(username, repo_name, file_path, branch)
        
        # Download the file
        success = repo_service.download_file(download_url, output_path)
        
        if success:
            display.show_success(f"File downloaded to {output_path}")
            return 0
        else:
            display.show_error("Failed to download file")
            return 1
    else:
        display.show_message(f"Downloading directory {file_path} from {username}/{repo_name}...")
        
        # If output path is not specified, use the directory name
        if not output_path:
            output_path = os.path.join("downloads", file_path)
        
        # Download the directory
        success = repo_service.download_directory(username, repo_name, file_path, output_path, branch)
        
        if success:
            display.show_success(f"Directory downloaded to {output_path}")
            return 0
        else:
            display.show_error("Failed to download directory")
            return 1


def cmd_clone(args: argparse.Namespace, services: Dict[str, Any]) -> int:
    """Handle the clone command.
    
    Args:
        args: Parsed arguments
        services: Dictionary of service instances
        
    Returns:
        Exit code
    """
    display = services["display"]
    repo_service = services["repo_service"]
    
    # Check if Git is installed
    if not check_git_installed():
        display.show_error("Git is not installed. Please install Git to use the clone command.")
        return 1
    
    try:
        username, repo_name = extract_repo_parts(args.repo)
    except ValueError as e:
        display.show_error(str(e))
        return 1
    
    output_path = args.output
    
    display.show_message(f"Cloning repository {username}/{repo_name}...")
    
    # Clone the repository
    success = repo_service.clone_repository(username, repo_name)
    
    if success:
        clone_path = output_path or os.path.join("repositories", repo_name)
        display.show_success(f"Repository cloned to {clone_path}")
        return 0
    else:
        display.show_error("Failed to clone repository")
        return 1


def cmd_config(args: argparse.Namespace, services: Dict[str, Any]) -> int:
    """Handle the config command.
    
    Args:
        args: Parsed arguments
        services: Dictionary of service instances
        
    Returns:
        Exit code
    """
    config = services["config"]
    display = services["display"]
    messages = services["messages"]
    
    # Set language if specified
    if args.language:
        config.set_language(args.language)
        messages.set_language(args.language)
        display.show_success(messages.get("language_changed"))
    
    # Set GitHub token if specified
    if args.token:
        config.set_github_token(args.token)
        display.show_success("GitHub API token set")
    
    # If no options specified, show current configuration
    if not args.language and not args.token:
        language = config.get_language()
        token = config.get_github_token()
        token_display = "set" if token else "not set"
        
        display.show_message("Current configuration:")
        display.show_message(f"Language: {language}")
        display.show_message(f"GitHub API token: {token_display}")
    
    return 0


def main() -> int:
    """Main entry point for the CLI.
    
    Returns:
        Exit code
    """
    # Make gitbrowse with no args default to 'browse' command
    if len(sys.argv) == 1:
        sys.argv.append('browse')
        
    args = parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    # Initialize services
    config = Config()
    language = config.get_language()
    messages = Messages(language)
    display = Display(messages)
    network_service = NetworkService()
    github_api = GitHubAPI(token=config.get_github_token())
    repo_service = RepositoryService(github_api, network_service)
    
    # Create a services dictionary
    services = {
        "config": config,
        "messages": messages,
        "display": display,
        "network_service": network_service,
        "github_api": github_api,
        "repo_service": repo_service
    }
    
    # Check for internet connection
    if not network_service.is_connected() and args.command not in [None, "config"]:
        display.show_warning(messages.get("no_internet"))
    
    # Handle commands
    if args.command == "browse":
        return cmd_browse(args, services)
    elif args.command == "list":
        return cmd_list(args, services)
    elif args.command == "view":
        return cmd_view(args, services)
    elif args.command == "download":
        return cmd_download(args, services)
    elif args.command == "clone":
        return cmd_clone(args, services)
    elif args.command == "config":
        return cmd_config(args, services)
    else:
        display.show_error(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())