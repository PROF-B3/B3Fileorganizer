"""
B3Team Core Library
Shared components and utilities for all B3Team agents.
"""

from .ai_manager import AIManager
from .resource_monitor import ResourceMonitor
from .database_manager import DatabaseManager
from .config_manager import ConfigManager
from .progress_tracker import ProgressTracker
from .zettelkasten import ZettelkastenManager
from .orchestrator import AgentOrchestrator

__version__ = "1.0.0"
__author__ = "B3Team"

__all__ = [
    'AIManager',
    'ResourceMonitor', 
    'DatabaseManager',
    'ConfigManager',
    'ProgressTracker',
    'ZettelkastenManager',
    'AgentOrchestrator'
] 