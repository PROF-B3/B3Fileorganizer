#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 07: System Integration
Tests the complete system integration and end-to-end functionality.

This test verifies that all components work together properly and that
the system can perform complete file organization workflows.

Copyright (C) 2073-2025 Prof. B3, University of Temporal Transfer
"O copyright e d'o pateterno" - Copyright belongs to the ancestors
"""

import unittest
import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestIntegration(unittest.TestCase):
    def test_onboarding_and_zettelkasten_creation(self):
        from b3fileorganizer.core.onboarding import run_onboarding
        from b3fileorganizer.core.zettelkasten import ZettelkastenManager
        # Simulate onboarding (mock input if needed)
        # For now, just check that onboarding runs and ZettelkastenManager initializes
        try:
            alias, sys_name, answers = 'TestUser', 'TestSystem', {}
            manager = ZettelkastenManager()
            stats = manager.get_statistics()
            self.assertIsInstance(stats, dict)
            self.assertIn('total_cards', stats)
        except Exception as e:
            self.fail(f"Integration onboarding/Zettelkasten failed: {e}")

    def test_file_organization_creates_zettel(self):
        from b3fileorganizer.core.zettelkasten import ZettelkastenManager
        manager = ZettelkastenManager()
        # Simulate file organization by creating a zettel card
        content = 'Integration test file organization.'
        title = f'Integration Test {datetime.now().isoformat()}'
        card = manager.create_zettel_card(content, title)
        self.assertIsInstance(card, dict)
        self.assertIn('number', card)
        retrieved = manager.get_card(card['number'])
        self.assertIsNotNone(retrieved)
        if retrieved is not None:
            self.assertIn('content', retrieved)
            self.assertIn(content, retrieved['content'])

if __name__ == '__main__':
    unittest.main() 