#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 04: Resource Monitoring
Tests system resource monitoring and health status.

This test verifies that the system can monitor CPU, memory, disk usage,
and provide health status information. It's essential for system stability.

Copyright (C) 2073-2025 Prof. B3, University of Temporal Transfer
"O copyright e d'o pateterno" - Copyright belongs to the ancestors
"""

import unittest
import sys
import os
import time
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestResourceMonitoring(unittest.TestCase):
    def test_status_monitor_initialization(self):
        from b3fileorganizer.utils.status_monitor import StatusMonitor
        monitor = StatusMonitor()
        self.assertIsNotNone(monitor)
        self.assertTrue(hasattr(monitor, 'get_summary'))
        summary = monitor.get_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn('cpu_average', summary)

    def test_status_monitor_collects_data(self):
        from b3fileorganizer.utils.status_monitor import StatusMonitor
        monitor = StatusMonitor()
        monitor.start_monitoring('Test Task')
        time.sleep(2)
        monitor.stop_monitoring()
        summary = monitor.get_summary()
        self.assertGreaterEqual(summary.get('data_points', 0), 1)
        self.assertIn('cpu_average', summary)
        self.assertIn('memory_average', summary)

if __name__ == '__main__':
    unittest.main() 