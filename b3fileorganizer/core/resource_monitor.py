"""
Resource Monitor for B3Team
Monitors system resources and manages AI agent deployment.
"""

import psutil
import time
import threading
import logging
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SystemResources:
    cpu_percent: float
    memory_percent: float
    memory_available: int
    disk_usage: Dict[str, float]
    network_io: Dict[str, int]
    timestamp: datetime

@dataclass
class ResourceThresholds:
    cpu_warning: float = 80.0
    cpu_critical: float = 95.0
    memory_warning: float = 75.0
    memory_critical: float = 90.0
    disk_warning: float = 85.0
    disk_critical: float = 95.0

class ResourceMonitor:
    """Monitors system resources and provides health status."""
    
    def __init__(self, thresholds: Optional[ResourceThresholds] = None):
        self.thresholds = thresholds or ResourceThresholds()
        self.logger = logging.getLogger(__name__)
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.callbacks: List[Callable[[SystemResources], None]] = []
        self.history: List[SystemResources] = []
        self.max_history = 1000
        
    @property
    def is_monitoring(self) -> bool:
        """Property to check if monitoring is active (for test compatibility)."""
        return self.monitoring
    
    def start_monitoring(self, interval: float = 1.0):
        """Start continuous resource monitoring."""
        if self.monitoring:
            self.logger.warning("Monitoring already active")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        self.logger.info("Resource monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous resource monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        self.logger.info("Resource monitoring stopped")
    
    def _monitor_loop(self, interval: float):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                resources = self.get_current_resources()
                self.history.append(resources)
                
                # Keep history size manageable
                if len(self.history) > self.max_history:
                    self.history = self.history[-self.max_history:]
                
                # Check thresholds and trigger callbacks
                self._check_thresholds(resources)
                
                # Call registered callbacks
                for callback in self.callbacks:
                    try:
                        callback(resources)
                    except Exception as e:
                        self.logger.error(f"Callback error: {e}")
                
                time.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(interval)
    
    def get_current_resources(self) -> SystemResources:
        """Get current system resource usage."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available
            
            # Disk usage for all drives
            disk_usage = {}
            EXCLUDED_DRIVES = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'Y:', 'Z:']
            for partition in psutil.disk_partitions():
                if not (partition.device.upper().startswith('X:') or partition.device.upper().startswith('B:')):
                    continue
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_usage[partition.mountpoint] = (usage.used / usage.total) * 100
                except PermissionError:
                    continue
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            return SystemResources(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_available=memory_available,
                disk_usage=disk_usage,
                network_io=network_io,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Error getting system resources: {e}")
            return SystemResources(
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_available=0,
                disk_usage={},
                network_io={},
                timestamp=datetime.now()
            )
    
    def _check_thresholds(self, resources: SystemResources):
        """Check resource usage against thresholds."""
        warnings = []
        
        # CPU checks
        if resources.cpu_percent >= self.thresholds.cpu_critical:
            warnings.append(f"CRITICAL: CPU usage at {resources.cpu_percent:.1f}%")
        elif resources.cpu_percent >= self.thresholds.cpu_warning:
            warnings.append(f"WARNING: CPU usage at {resources.cpu_percent:.1f}%")
        
        # Memory checks
        if resources.memory_percent >= self.thresholds.memory_critical:
            warnings.append(f"CRITICAL: Memory usage at {resources.memory_percent:.1f}%")
        elif resources.memory_percent >= self.thresholds.memory_warning:
            warnings.append(f"WARNING: Memory usage at {resources.memory_percent:.1f}%")
        
        # Disk checks
        for drive, usage in resources.disk_usage.items():
            if usage >= self.thresholds.disk_critical:
                warnings.append(f"CRITICAL: Disk {drive} usage at {usage:.1f}%")
            elif usage >= self.thresholds.disk_warning:
                warnings.append(f"WARNING: Disk {drive} usage at {usage:.1f}%")
        
        # Log warnings
        for warning in warnings:
            self.logger.warning(warning)
    
    def add_callback(self, callback: Callable[[SystemResources], None]):
        """Add a callback function to be called with resource updates."""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback: Callable[[SystemResources], None]):
        """Remove a callback function."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def get_resource_summary(self) -> Dict:
        """Get a summary of current resource usage."""
        if not self.history:
            return {}
        
        latest = self.history[-1]
        
        # Calculate averages over last 10 readings
        recent = self.history[-10:] if len(self.history) >= 10 else self.history
        
        avg_cpu = sum(r.cpu_percent for r in recent) / len(recent)
        avg_memory = sum(r.memory_percent for r in recent) / len(recent)
        
        return {
            'current': {
                'cpu_percent': latest.cpu_percent,
                'memory_percent': latest.memory_percent,
                'memory_available_gb': latest.memory_available / (1024**3),
                'disk_usage': latest.disk_usage,
                'timestamp': latest.timestamp.isoformat()
            },
            'averages': {
                'cpu_percent': avg_cpu,
                'memory_percent': avg_memory
            },
            'status': self._get_system_status(latest)
        }
    
    def _get_system_status(self, resources: SystemResources) -> str:
        """Get overall system status."""
        if (resources.cpu_percent >= self.thresholds.cpu_critical or
            resources.memory_percent >= self.thresholds.memory_critical):
            return "CRITICAL"
        elif (resources.cpu_percent >= self.thresholds.cpu_warning or
              resources.memory_percent >= self.thresholds.memory_warning):
            return "WARNING"
        else:
            return "HEALTHY"
    
    def can_start_ai_agent(self, estimated_memory_mb: int = 2048) -> bool:
        """Check if system can handle starting a new AI agent."""
        if not self.history:
            return True
        
        latest = self.history[-1]
        available_memory_gb = latest.memory_available / (1024**3)
        required_memory_gb = estimated_memory_mb / 1024
        
        # Check if we have enough memory and CPU is not overloaded
        return (available_memory_gb >= required_memory_gb and 
                latest.cpu_percent < self.thresholds.cpu_warning)
    
    def get_process_info(self) -> List[Dict]:
        """Get information about running processes."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        return processes[:20]  # Return top 20 processes 