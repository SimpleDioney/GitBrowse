"""
System utility functions for GitBrowse.
"""

import os
import sys
import platform
import logging
import subprocess
import tempfile
import uuid
from typing import Optional, Tuple, List

logger = logging.getLogger("gitbrowse.utils.system")


def get_clear_command() -> str:
    """Get the appropriate clear command for the current operating system.
    
    Returns:
        Clear command string
    """
    system = platform.system().lower()
    
    if system in ["linux", "darwin", "freebsd", "openbsd", "netbsd"]:
        return "clear"
    elif system == "windows":
        return "cls"
    
    # Unknown system, try to determine a reasonable default
    if os.name == "posix":
        return "clear"
    elif os.name == "nt":
        return "cls"
    
    # Default to an empty string if we can't determine
    logger.warning(f"Could not determine clear command for system: {system}")
    return ""


def check_command_exists(command: str) -> bool:
    """Check if a command exists in the system PATH.
    
    Args:
        command: Command to check
        
    Returns:
        True if the command exists, False otherwise
    """
    try:
        # Use 'where' on Windows, 'which' on other systems
        if platform.system().lower() == "windows":
            subprocess.run(
                ["where", command], 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
        else:
            subprocess.run(
                ["which", command], 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def check_git_installed() -> bool:
    """Check if Git is installed on the system.
    
    Returns:
        True if Git is installed, False otherwise
    """
    return check_command_exists("git")


def get_temp_file_path(prefix: str = "gitbrowse_", suffix: str = "") -> str:
    """Get a path for a temporary file.
    
    Args:
        prefix: Prefix for the temporary file
        suffix: Suffix/extension for the temporary file
        
    Returns:
        Path to a temporary file
    """
    fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    os.close(fd)  # Close the file descriptor
    return path


def get_unique_filename(base_path: str) -> str:
    """Generate a unique filename if the original already exists.
    
    Args:
        base_path: Base file path to check
        
    Returns:
        Unique file path
    """
    if not os.path.exists(base_path):
        return base_path
    
    directory, filename = os.path.split(base_path)
    name, ext = os.path.splitext(filename)
    
    counter = 1
    while True:
        new_path = os.path.join(directory, f"{name}_{counter}{ext}")
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def execute_command(
    command: List[str], cwd: Optional[str] = None, timeout: Optional[float] = None
) -> Tuple[bool, str, str]:
    """Execute a system command with error handling.
    
    Args:
        command: Command to execute as a list of strings
        cwd: Working directory for the command
        timeout: Timeout in seconds
        
    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            capture_output=True,
            text=True,
            check=False
        )
        
        return (
            result.returncode == 0,
            result.stdout.strip(),
            result.stderr.strip()
        )
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", f"Error executing command: {str(e)}"


def get_system_info() -> dict:
    """Get information about the current system.
    
    Returns:
        Dictionary with system information
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "username": os.getlogin() if hasattr(os, 'getlogin') else "Unknown",
        "home_directory": os.path.expanduser("~"),
        "working_directory": os.getcwd()
    }


def open_file_with_default_app(file_path: str) -> bool:
    """Open a file with the default system application.
    
    Args:
        file_path: Path to the file to open
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if platform.system().lower() == "windows":
            os.startfile(file_path)
        elif platform.system().lower() == "darwin":  # macOS
            subprocess.run(["open", file_path], check=True)
        else:  # Linux and other Unix-like systems
            subprocess.run(["xdg-open", file_path], check=True)
        return True
    except Exception as e:
        logger.error(f"Error opening file {file_path}: {str(e)}")
        return False