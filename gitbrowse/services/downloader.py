"""
File download service for GitBrowse.
"""

import os
import logging
import threading
import time
from typing import Dict, Optional, List, Any
from queue import Queue
import requests
from tqdm import tqdm

logger = logging.getLogger("gitbrowse.services.downloader")


class DownloadTask:
    """Represents a single download task."""
    
    def __init__(
        self, url: str, destination: str, 
        description: Optional[str] = None, callback=None
    ):
        """Initialize a download task.
        
        Args:
            url: URL to download from
            destination: Path to save the file
            description: Optional description for the progress bar
            callback: Function to call when download completes
        """
        self.url = url
        self.destination = destination
        self.description = description or os.path.basename(destination)
        self.callback = callback
        self.success = False
        self.error = None


class DownloadService:
    """Service for downloading files with progress tracking."""
    
    def __init__(self, max_workers: int = 5):
        """Initialize the download service.
        
        Args:
            max_workers: Maximum number of concurrent downloads
        """
        self.max_workers = max_workers
        self.queue = Queue()
        self.active_downloads = {}
        self.lock = threading.Lock()
        self.workers = []
        self._stop_event = threading.Event()
        
        # Start worker threads
        for i in range(max_workers):
            worker = threading.Thread(target=self._download_worker, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def download_file(
        self, url: str, destination: str, 
        description: Optional[str] = None, callback=None
    ) -> str:
        """Queue a file for download.
        
        Args:
            url: URL to download from
            destination: Path to save the file
            description: Optional description for the progress bar
            callback: Function to call when download completes
            
        Returns:
            Task ID for tracking
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(destination)), exist_ok=True)
        
        # Create and queue the task
        task_id = f"task_{time.time()}_{hash(url)}"
        task = DownloadTask(url, destination, description, callback)
        
        with self.lock:
            self.active_downloads[task_id] = task
        
        self.queue.put((task_id, task))
        return task_id
    
    def download_files(
        self, files: List[Dict[str, Any]], base_dir: str = "downloads"
    ) -> List[str]:
        """Queue multiple files for download.
        
        Args:
            files: List of file info dictionaries with 'url' and 'path' keys
            base_dir: Base directory for downloads
            
        Returns:
            List of task IDs
        """
        task_ids = []
        
        for file_info in files:
            url = file_info.get("url")
            path = file_info.get("path")
            
            if url and path:
                destination = os.path.join(base_dir, path)
                task_id = self.download_file(url, destination)
                task_ids.append(task_id)
        
        return task_ids
    
    def get_download_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of a download task.
        
        Args:
            task_id: Task ID
            
        Returns:
            Dictionary with task status
        """
        with self.lock:
            task = self.active_downloads.get(task_id)
            
            if task:
                return {
                    "url": task.url,
                    "destination": task.destination,
                    "description": task.description,
                    "success": task.success,
                    "error": str(task.error) if task.error else None,
                    "completed": task.success or task.error is not None
                }
            
            return {"error": "Task not found", "completed": True}
    
    def wait_for_downloads(self, task_ids: List[str], timeout: Optional[float] = None) -> bool:
        """Wait for downloads to complete.
        
        Args:
            task_ids: List of task IDs to wait for
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if all downloads completed successfully, False otherwise
        """
        start_time = time.time()
        
        while task_ids:
            remaining_ids = []
            
            for task_id in task_ids:
                status = self.get_download_status(task_id)
                
                if not status.get("completed", False):
                    remaining_ids.append(task_id)
            
            task_ids = remaining_ids
            
            if not task_ids:
                break
            
            if timeout and (time.time() - start_time) > timeout:
                return False
            
            time.sleep(0.5)
        
        # Check if all tasks were successful
        with self.lock:
            return all(
                self.active_downloads.get(task_id, DownloadTask("", "")).success 
                for task_id in task_ids
            )
    
    def _download_worker(self) -> None:
        """Worker thread function for processing download tasks."""
        while not self._stop_event.is_set():
            try:
                # Get the next task from the queue
                task_id, task = self.queue.get(timeout=1.0)
                
                try:
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(os.path.abspath(task.destination)), exist_ok=True)
                    
                    # Make the request with streaming enabled
                    with requests.get(task.url, stream=True, allow_redirects=True) as response:
                        response.raise_for_status()
                        
                        # Get the total file size if available
                        total_size = int(response.headers.get('content-length', 0))
                        
                        # Create progress bar
                        with tqdm(
                            total=total_size, unit='B', unit_scale=True, 
                            desc=task.description, leave=False
                        ) as progress_bar:
                            
                            # Write the file
                            with open(task.destination, 'wb') as out_file:
                                for chunk in response.iter_content(chunk_size=8192):
                                    out_file.write(chunk)
                                    progress_bar.update(len(chunk))
                    
                    # Mark task as successful
                    with self.lock:
                        task.success = True
                    
                    # Call the callback if provided
                    if task.callback:
                        task.callback(task_id, True, None)
                
                except Exception as e:
                    logger.error(f"Error downloading {task.url}: {str(e)}")
                    
                    # Store the error and call the callback
                    with self.lock:
                        task.error = e
                    
                    if task.callback:
                        task.callback(task_id, False, str(e))
                
                finally:
                    # Mark the task as done
                    self.queue.task_done()
            
            except (TimeoutError, OSError):
                # Queue.get can time out, which is expected
                pass
            except Exception as e:
                logger.error(f"Unexpected error in download worker: {str(e)}")
    
    def stop(self) -> None:
        """Stop all download workers."""
        self._stop_event.set()
        
        for worker in self.workers:
            worker.join(timeout=1.0)