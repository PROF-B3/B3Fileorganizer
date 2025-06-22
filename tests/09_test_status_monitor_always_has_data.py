import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestStatusMonitorAlwaysHasData(unittest.TestCase):
    def test_status_monitor_initial_data_point(self):
        from b3fileorganizer.utils.status_monitor import StatusMonitor
        monitor = StatusMonitor()
        summary = monitor.get_summary()
        self.assertGreaterEqual(summary.get('data_points', 0), 1)

if __name__ == '__main__':
    unittest.main() 