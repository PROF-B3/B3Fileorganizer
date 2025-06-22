"""
Progress Tracker for B3Team
Tracks progress of operations and provides time estimates.
"""

import time
import logging
from typing import Dict, Optional
from datetime import datetime

class ProgressTracker:
    """Tracks progress of operations and provides time estimates."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_operation: Optional[str] = None
        self.start_time: Optional[float] = None
        self.current_progress: float = 0.0
        self.operation_history: Dict[str, Dict] = {}
    
    def start_operation(self, operation_name: str, details: str = ""):
        """Start tracking a new operation."""
        self.current_operation = operation_name
        self.start_time = time.time()
        self.current_progress = 0.0
        
        self.operation_history[operation_name] = {
            'start_time': self.start_time,
            'details': details,
            'progress': 0.0,
            'status': 'running'
        }
        
        self.logger.info(f"Started operation: {operation_name} - {details}")
    
    def update_progress(self, progress_percent: float):
        """Update the progress of the current operation."""
        if not self.current_operation:
            self.logger.warning("No active operation to update progress")
            return
        
        self.current_progress = max(0.0, min(100.0, progress_percent))
        
        if self.current_operation in self.operation_history:
            self.operation_history[self.current_operation]['progress'] = self.current_progress
        
        self.logger.info(f"Progress for {self.current_operation}: {self.current_progress:.1f}%")
    
    def end_operation(self):
        """End the current operation."""
        if not self.current_operation:
            self.logger.warning("No active operation to end")
            return
        
        end_time = time.time()
        duration = end_time - self.start_time if self.start_time else 0
        
        if self.current_operation in self.operation_history:
            self.operation_history[self.current_operation].update({
                'end_time': end_time,
                'duration': duration,
                'progress': 100.0,
                'status': 'completed'
            })
        
        self.logger.info(f"Completed operation: {self.current_operation} in {duration:.2f}s")
        
        self.current_operation = None
        self.start_time = None
        self.current_progress = 0.0
    
    def get_current_progress(self) -> Dict:
        """Get current operation progress."""
        if not self.current_operation:
            return {}
        
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        # Estimate remaining time
        if self.current_progress > 0:
            estimated_total = elapsed / (self.current_progress / 100.0)
            remaining = estimated_total - elapsed
        else:
            remaining = 0
        
        return {
            'operation': self.current_operation,
            'progress': self.current_progress,
            'elapsed_time': elapsed,
            'estimated_remaining': remaining,
            'details': self.operation_history.get(self.current_operation, {}).get('details', '')
        }
    
    def get_operation_history(self) -> Dict:
        """Get history of all operations."""
        return self.operation_history.copy() 