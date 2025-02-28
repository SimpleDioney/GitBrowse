"""
Utility functions for API interactions.
"""

import os
import json
import time
import logging
import functools
from typing import Any, Callable, Dict, Optional, TypeVar

import requests

logger = logging.getLogger("gitbrowse.api.utils")

# Define type for decorated functions
T = TypeVar('T')


def handle_rate_limit(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to handle GitHub API rate limiting.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        retries = 3
        
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.HTTPError as e:
                response = e.response
                
                # Check if rate limited
                if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
                    remaining = int(response.headers['X-RateLimit-Remaining'])
                    
                    if remaining == 0:
                        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                        wait_time = max(reset_time - time.time(), 0) + 1
                        
                        logger.warning(f"Rate limit exceeded. Waiting {wait_time:.1f} seconds.")
                        
                        # If wait time is reasonable, wait and retry
                        if wait_time < 300:  # 5 minutes max wait
                            time.sleep(wait_time)
                            continue
                        else:
                            logger.error("Rate limit wait time too long.")
                            raise
                
                # For other HTTP errors, retry a few times with exponential backoff
                if attempt < retries - 1:
                    sleep_time = (2 ** attempt) + 1
                    logger.warning(f"HTTP error {e.response.status_code}. Retrying in {sleep_time} seconds.")
                    time.sleep(sleep_time)
                else:
                    raise
    
    return wrapper


def cache_response(timeout: int = 3600) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to cache API responses to disk.
    
    Args:
        timeout: Cache timeout in seconds (default: 1 hour)
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a cache key based on function name and arguments
            cache_key = f"{func.__name__}_{hash(str(args) + str(sorted(kwargs.items())))}"
            cache_dir = os.path.join(os.getcwd(), "cache")
            cache_file = os.path.join(cache_dir, f"{cache_key}.json")
            
            # Create cache directory if it doesn't exist
            os.makedirs(cache_dir, exist_ok=True)
            
            # Check if cached result exists and is still valid
            try:
                if os.path.exists(cache_file):
                    file_age = time.time() - os.path.getmtime(cache_file)
                    
                    # If cache is still valid
                    if file_age < timeout:
                        with open(cache_file, 'r') as f:
                            logger.debug(f"Using cached result for {func.__name__}")
                            return json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"Error reading cache: {str(e)}")
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            
            try:
                with open(cache_file, 'w') as f:
                    json.dump(result, f)
            except OSError as e:
                logger.warning(f"Error writing cache: {str(e)}")
            
            return result
        
        return wrapper
    
    return decorator


def extract_username_repo(url: str) -> tuple:
    """Extract username and repository name from a GitHub URL.
    
    Args:
        url: GitHub URL
        
    Returns:
        Tuple of (username, repository_name)
    """
    parts = url.strip('/').split('/')
    
    # Handle different URL formats
    if 'github.com' in parts:
        github_index = parts.index('github.com')
        if len(parts) > github_index + 2:
            return parts[github_index + 1], parts[github_index + 2]
    elif len(parts) >= 2:
        # Handle simple format like 'username/repo'
        return parts[-2], parts[-1]
    
    return None, None


def format_api_error(error: Exception) -> str:
    """Format an API error for display.
    
    Args:
        error: Exception object
        
    Returns:
        Formatted error message
    """
    if isinstance(error, requests.exceptions.HTTPError):
        status_code = error.response.status_code
        message = error.response.text
        
        try:
            # Try to parse the error message from JSON
            error_data = error.response.json()
            if "message" in error_data:
                message = error_data["message"]
        except json.JSONDecodeError:
            pass
        
        return f"HTTP Error {status_code}: {message}"
    
    return str(error)