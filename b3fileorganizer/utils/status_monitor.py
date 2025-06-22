"""
Status Monitor for B3FileOrganizer
Provides real-time monitoring of AI operations, resource usage, and system status.
"""

import time
import threading
import psutil
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class StatusMonitor:
    """Real-time status monitoring for AI operations and system resources."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.monitoring = False
        self.current_task = None
        self.progress = 0
        self.status_message = "Idle"
        self.start_time = None
        self.estimated_completion = None
        self.resource_history = []
        self.max_history = 100
        # Collect an initial data point
        self.resource_history.append(self._collect_resource_data())
        
    def start_monitoring(self, task_name: str = "AI Operation"):
        """Start monitoring with a specific task."""
        self.monitoring = True
        self.current_task = task_name
        self.progress = 0
        self.status_message = f"Starting {task_name}..."
        self.start_time = datetime.now()
        self.estimated_completion = None
        self.resource_history = []
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info(f"Started monitoring: {task_name}")
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.monitoring = False
        self.current_task = None
        self.status_message = "Monitoring stopped"
        self.logger.info("Stopped monitoring")
    
    def update_progress(self, progress: int, message: Optional[str] = None):
        """Update progress percentage and status message."""
        self.progress = max(0, min(100, progress))
        if message:
            self.status_message = message
        
        # Estimate completion time
        if self.start_time and self.progress > 0:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            if self.progress > 0:
                total_estimated = (elapsed / self.progress) * 100
                remaining = total_estimated - elapsed
                self.estimated_completion = datetime.now().timestamp() + remaining
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                # Collect resource data
                resource_data = self._collect_resource_data()
                self.resource_history.append(resource_data)
                
                # Keep history size manageable
                if len(self.resource_history) > self.max_history:
                    self.resource_history.pop(0)
                
                # Display status
                self._display_status()
                
                time.sleep(1)  # Update every second
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)
    
    def _collect_resource_data(self) -> Dict[str, Any]:
        """Collect current system resource data."""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage(str(Path.cwd()))
            
            # Get GPU info if available
            gpu_info = self._get_gpu_info()
            
            try:
                memory_used = float(memory.used)
            except Exception:
                memory_used = 0.0
            try:
                memory_total = float(memory.total)
            except Exception:
                memory_total = 0.0
            try:
                disk_used = float(disk.used)
            except Exception:
                disk_used = 0.0
            try:
                disk_total = float(disk.total)
            except Exception:
                disk_total = 0.0
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_gb": memory_used / (1024**3),
                "memory_total_gb": memory_total / (1024**3),
                "disk_percent": disk.percent,
                "disk_used_gb": disk_used / (1024**3),
                "disk_total_gb": disk_total / (1024**3),
                "gpu_info": gpu_info
            }
        except Exception as e:
            self.logger.error(f"Error collecting resource data: {e}")
            return {"timestamp": datetime.now().isoformat(), "error": str(e)}
    
    def _get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU information if available."""
        try:
            # Try to get GPU info using nvidia-ml-py if available
            try:
                import pynvml
                pynvml.nvmlInit()
                gpu_count = pynvml.nvmlDeviceGetCount()
                gpu_info = []
                
                for i in range(gpu_count):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    name = pynvml.nvmlDeviceGetName(handle).decode('utf-8')
                    memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    
                    gpu_info.append({
                        "name": name,
                        "memory_used_mb": memory.used / (1024**2),
                        "memory_total_mb": memory.total / (1024**2),
                        "gpu_utilization": utilization.gpu,
                        "memory_utilization": utilization.memory
                    })
                
                return {"gpus": gpu_info}
                
            except (ImportError, ModuleNotFoundError):
                # Fallback: try to get basic GPU info
                return {"status": "nvidia-ml-py not available"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def _display_status(self):
        """Display current status and resource usage."""
        if not self.resource_history:
            return
        
        current = self.resource_history[-1]
        
        # Clear screen (works on most terminals)
        print("\033[2J\033[H", end="")
        
        # Display header
        print("=" * 80)
        print(f"B3FileOrganizer - AI Status Monitor")
        print("=" * 80)
        
        # Display current task
        if self.current_task:
            print(f"\nCurrent Task: {self.current_task}")
            print(f"Status: {self.status_message}")
            print(f"Progress: {self.progress}%")
            
            if self.start_time:
                elapsed = datetime.now() - self.start_time
                print(f"Elapsed Time: {str(elapsed).split('.')[0]}")
                
                if self.estimated_completion:
                    remaining = self.estimated_completion - datetime.now().timestamp()
                    if remaining > 0:
                        remaining_str = str(int(remaining)) + "s"
                        print(f"Estimated Remaining: {remaining_str}")
        
        # Display resource usage
        print(f"\nSystem Resources:")
        print(f"CPU Usage: {current.get('cpu_percent', 'N/A')}%")
        print(f"Memory: {current.get('memory_used_gb', 0):.1f}GB / {current.get('memory_total_gb', 0):.1f}GB ({current.get('memory_percent', 0):.1f}%)")
        print(f"Disk: {current.get('disk_used_gb', 0):.1f}GB / {current.get('disk_total_gb', 0):.1f}GB ({current.get('disk_percent', 0):.1f}%)")
        
        # Display GPU info if available
        gpu_info = current.get('gpu_info', {})
        if 'gpus' in gpu_info:
            print(f"\nGPU Information:")
            for i, gpu in enumerate(gpu_info['gpus']):
                print(f"  GPU {i}: {gpu['name']}")
                print(f"    Utilization: {gpu['gpu_utilization']}%")
                print(f"    Memory: {gpu['memory_used_mb']:.0f}MB / {gpu['memory_total_mb']:.0f}MB ({gpu['memory_utilization']}%)")
        
        # Display progress bar
        if self.progress > 0:
            bar_length = 50
            filled_length = int(bar_length * self.progress // 100)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            print(f"\nProgress: [{bar}] {self.progress}%")
        
        print("\n" + "=" * 80)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get monitoring summary."""
        if not self.resource_history:
            return {"error": "No monitoring data available"}
        
        # Calculate averages
        cpu_avg = sum(r.get('cpu_percent', 0) for r in self.resource_history) / len(self.resource_history)
        memory_avg = sum(r.get('memory_percent', 0) for r in self.resource_history) / len(self.resource_history)
        
        # Get peak values
        cpu_peak = max(r.get('cpu_percent', 0) for r in self.resource_history)
        memory_peak = max(r.get('memory_percent', 0) for r in self.resource_history)
        
        return {
            "task": self.current_task,
            "duration": str(datetime.now() - self.start_time).split('.')[0] if self.start_time else "N/A",
            "progress": self.progress,
            "cpu_average": cpu_avg,
            "cpu_peak": cpu_peak,
            "memory_average": memory_avg,
            "memory_peak": memory_peak,
            "data_points": len(self.resource_history)
        }
    
    def save_report(self, filename: Optional[str] = None):
        """Save monitoring report to file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"monitoring_report_{timestamp}.json"
        
        report = {
            "summary": self.get_summary(),
            "resource_history": self.resource_history,
            "generated_at": datetime.now().isoformat()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            self.logger.info(f"Monitoring report saved to {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")
            return None

# Global status monitor instance
status_monitor = StatusMonitor()

def start_ai_operation(task_name: str, operation_func: Callable, *args, **kwargs):
    """Wrapper to run AI operations with monitoring."""
    try:
        # Start monitoring
        status_monitor.start_monitoring(task_name)
        
        # Run the operation
        result = operation_func(*args, **kwargs)
        
        # Stop monitoring
        status_monitor.stop_monitoring()
        
        return result
        
    except Exception as e:
        status_monitor.stop_monitoring()
        raise e 