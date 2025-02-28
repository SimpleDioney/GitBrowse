"""
Network connectivity service for GitBrowse.
"""

import socket
import time
import threading
import logging
from typing import Callable, Optional

logger = logging.getLogger("gitbrowse.services.network")


class NetworkService:
    """Network connectivity service for checking internet connection."""
    
    def __init__(self, check_interval: int = 30):
        """Initialize the network service.
        
        Args:
            check_interval: Interval in seconds for automatic connection checks
        """
        self._connected = True  # Assume connected until first check
        self._lock = threading.Lock()
        self._check_interval = check_interval
        self._callback = None  # Callback function for connection state changes
        self._stop_event = threading.Event()
        self._monitor_thread = threading.Thread(target=self._connection_monitor, daemon=True)
        self._monitor_thread.start()
    
    def is_connected(self) -> bool:
        """Check if the device is currently connected to the internet.
        
        Returns:
            True if connected, False otherwise
        """
        with self._lock:
            return self._connected
    
    def check_connection(self) -> bool:
        """Force a connection check and return the result.
        
        Returns:
            True if connected, False otherwise
        """
        connected = self._check_internet_connection()
        with self._lock:
            old_state = self._connected
            self._connected = connected
            
            # If state changed and callback is set, call it
            if old_state != connected and self._callback:
                try:
                    self._callback(connected)
                except Exception as e:
                    logger.error(f"Error in connection callback: {str(e)}")
        
        return connected
    
    def set_connection_callback(self, callback: Optional[Callable[[bool], None]]) -> None:
        """Set a callback function to be called when connection state changes.
        
        Args:
            callback: Function that takes a boolean parameter (connected)
        """
        self._callback = callback
    
    def _check_internet_connection(self) -> bool:
        """Check if the device can connect to a remote server.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            # Try to create a socket connection to Google's DNS
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            # Try an alternative host
            try:
                socket.create_connection(("1.1.1.1", 53), timeout=3)
                return True
            except OSError:
                return False
    
    def _connection_monitor(self) -> None:
        """Background thread that periodically checks the connection."""
        while not self._stop_event.is_set():
            try:
                self.check_connection()
            except Exception as e:
                logger.error(f"Error checking connection: {str(e)}")
            
            # Sleep for the check interval or until stopped
            self._stop_event.wait(self._check_interval)
    
    def stop(self) -> None:
        """Stop the connection monitoring thread."""
        self._stop_event.set()
        self._monitor_thread.join(timeout=1.0)