"""
Terminal styling and color definitions for GitBrowse UI.
"""

from typing import Dict, Any
from colorama import Fore, Back, Style

# Color definitions
RESET = Style.RESET_ALL
PREFIX_OUT = f"{Style.RESET_ALL}{Fore.LIGHTMAGENTA_EX}>> "
PREFIX_IN = f"{Style.RESET_ALL}{Fore.MAGENTA}<< "
ERROR = Fore.RED
SUCCESS = Fore.GREEN
INFO = Fore.CYAN
WARNING = Fore.YELLOW
WHITE = Fore.WHITE
HEADER = Fore.LIGHTMAGENTA_EX
FOOTER = Fore.MAGENTA
HIGHLIGHT = Fore.LIGHTYELLOW_EX
SECONDARY = Fore.LIGHTBLUE_EX
TERTIARY = Fore.LIGHTCYAN_EX

# Terminal symbols for different systems
SYMBOLS = {
    "arrow_right": "→",
    "arrow_left": "←",
    "star": "★",
    "fork": "⑂",
    "check": "✓",
    "cross": "✗",
    "warning": "⚠",
    "info": "ℹ",
    "folder": "📁",
    "file": "📄",
    "download": "⬇",
    "view": "👁",
    "clone": "📋",
    "back": "⬅",
    "next": "➡",
    "previous": "⬅",
}

# UI components
BOX_STYLES = {
    "header": f"{HEADER}{'═' * 60}{RESET}",
    "footer": f"{FOOTER}{'═' * 60}{RESET}",
    "separator": f"{WHITE}{'─' * 60}{RESET}",
    "thin_separator": f"{WHITE}{'─' * 30}{RESET}",
}

def logo() -> str:
    """Return the GitBrowse ASCII logo."""
    return f"""
{HEADER}   _____ _ _   ____                                {RESET}
{HEADER}  / ____(_) | |  _ \\                               {RESET}
{HEADER} | |  __ _| |_| |_) |_ __ _____  _    _  ___  ___  {RESET}
{HEADER} | | |_ | | __|  _ <| '__/ _ \\ \\ \\/\\/ / / __|/ _ \\ {RESET}
{HEADER} | |__| | | |_| |_) | | | (_) |\\ V  V /  \\__ \\  __/ {RESET}
{HEADER}  \\_____|_|\\__|____/|_|  \\___/  \\_/\\_/   |___/\\___| {RESET}
{HEADER}                                                    {RESET}
"""

def style_repo_name(name: str) -> str:
    """Style a repository name."""
    return f"{HEADER}{name}{RESET}"

def style_stats(stars: int, forks: int) -> str:
    """Style repository statistics (stars and forks)."""
    return f"{HIGHLIGHT}{SYMBOLS['star']} {WHITE}{stars}{RESET} {SECONDARY}{SYMBOLS['fork']} {WHITE}{forks}{RESET}"

def style_file_name(name: str, file_type: str) -> str:
    """Style a file name based on its type."""
    # Convert to lowercase and check for common directory type indicators
    type_lower = file_type.lower()
    is_directory = type_lower in ["dir", "directory", "folder"]
    
    icon = SYMBOLS["folder"] if is_directory else SYMBOLS["file"]
    color = SECONDARY if is_directory else TERTIARY
    return f"{color}{icon} {name}{RESET}"

def style_prompt(text: str) -> str:
    """Style a user prompt."""
    return f"{PREFIX_OUT} {WHITE}{text}: {RESET}"

def error_message(text: str) -> str:
    """Format an error message."""
    return f"{ERROR}{SYMBOLS['cross']} {text}{RESET}"

def success_message(text: str) -> str:
    """Format a success message."""
    return f"{SUCCESS}{SYMBOLS['check']} {text}{RESET}"

def info_message(text: str) -> str:
    """Format an info message."""
    return f"{INFO}{SYMBOLS['info']} {text}{RESET}"

def warning_message(text: str) -> str:
    """Format a warning message."""
    return f"{WARNING}{SYMBOLS['warning']} {text}{RESET}"

def format_title(text: str) -> str:
    """Format a title with decorations."""
    return f"\n{WHITE}{text.center(58)}{RESET}\n{BOX_STYLES['thin_separator']}\n"