"""
Code and text formatting utilities for GitBrowse.
"""

import os
import logging
import difflib
from typing import List, Dict, Any, Optional, Tuple

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename, TextLexer
from pygments.formatters import TerminalFormatter
from pygments.util import ClassNotFound

logger = logging.getLogger("gitbrowse.utils.formatter")


def highlight_code(code: str, file_path: Optional[str] = None, language: Optional[str] = None) -> str:
    """Highlight code using Pygments.
    
    Args:
        code: Code to highlight
        file_path: Optional file path for lexer guessing
        language: Optional language name for lexer selection
        
    Returns:
        Highlighted code as a string
    """
    try:
        # Try to determine the lexer
        lexer = None
        
        if language:
            # Use specified language
            try:
                lexer = get_lexer_by_name(language)
            except ClassNotFound:
                logger.warning(f"Lexer for language '{language}' not found")
        
        if not lexer and file_path:
            # Try to guess based on file name
            try:
                lexer = guess_lexer_for_filename(file_path, code)
            except ClassNotFound:
                logger.warning(f"Could not determine lexer for file: {file_path}")
        
        if not lexer:
            # Try to guess based on code content
            try:
                lexer = guess_lexer_for_filename("file.txt", code)
            except ClassNotFound:
                # Fall back to plain text
                lexer = TextLexer()
        
        # Format the code
        formatter = TerminalFormatter()
        highlighted_code = highlight(code, lexer, formatter)
        
        return highlighted_code
    except Exception as e:
        logger.warning(f"Error highlighting code: {str(e)}")
        return code


def format_diff(old_content: str, new_content: str, context_lines: int = 3) -> str:
    """Generate a colored diff between two strings.
    
    Args:
        old_content: Original content
        new_content: New content
        context_lines: Number of context lines to show
        
    Returns:
        Formatted diff as a string
    """
    from colorama import Fore, Style
    
    diff = difflib.unified_diff(
        old_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile='Original',
        tofile='Modified',
        n=context_lines
    )
    
    result = []
    for line in diff:
        if line.startswith('+'):
            result.append(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
        elif line.startswith('-'):
            result.append(f"{Fore.RED}{line}{Style.RESET_ALL}")
        elif line.startswith('@'):
            result.append(f"{Fore.CYAN}{line}{Style.RESET_ALL}")
        else:
            result.append(line)
    
    return ''.join(result)


def truncate_string(text: str, max_length: int = 80, ellipsis: str = "...") -> str:
    """Truncate a string to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        ellipsis: String to append when truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(ellipsis)] + ellipsis


def format_size(size_bytes: int) -> str:
    """Format a file size in a human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024 or unit == 'TB':
            if unit == 'B':
                return f"{size_bytes} {unit}"
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024


def format_table(data: List[Dict[str, Any]], columns: List[str], headers: Optional[List[str]] = None) -> str:
    """Format data as a text table.
    
    Args:
        data: List of dictionaries containing the data
        columns: List of column keys to include
        headers: Optional custom headers for columns
        
    Returns:
        Formatted table as a string
    """
    from colorama import Fore, Style
    
    if not data:
        return "No data to display"
    
    # Use column keys as headers if not provided
    headers = headers or columns
    
    # Calculate column widths
    widths = {col: len(str(headers[i])) for i, col in enumerate(columns)}
    for row in data:
        for col in columns:
            if col in row:
                widths[col] = max(widths[col], len(str(row.get(col, ""))))
    
    # Create the header
    header_line = " | ".join(
        f"{str(headers[i]):{widths[col]}s}" 
        for i, col in enumerate(columns)
    )
    separator = "-+-".join("-" * widths[col] for col in columns)
    
    # Format the table
    result = [
        f"{Fore.CYAN}{header_line}{Style.RESET_ALL}",
        separator
    ]
    
    # Add rows
    for row in data:
        row_str = " | ".join(
            f"{str(row.get(col, '')):{widths[col]}s}" 
            for col in columns
        )
        result.append(row_str)
    
    return "\n".join(result)


def wrap_text(text: str, width: int = 80) -> str:
    """Wrap text to a maximum width.
    
    Args:
        text: Text to wrap
        width: Maximum width
        
    Returns:
        Wrapped text
    """
    import textwrap
    return "\n".join(textwrap.wrap(text, width=width))


def format_time(seconds: float) -> str:
    """Format a time duration in a human-readable format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours:
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    else:
        return f"{int(minutes)}m {int(seconds)}s"