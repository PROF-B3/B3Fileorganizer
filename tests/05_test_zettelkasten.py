#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 05: Zettelkasten System
Tests the Zettelkasten knowledge organization system.

This test verifies that the Zettelkasten system can create, manage, and
organize knowledge cards with proper numbering and cross-references.

Copyright (C) 2073-2025 Prof. B3, University of Temporal Transfer
"O copyright e d'o pateterno" - Copyright belongs to the ancestors
"""

import unittest
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestZettelkasten(unittest.TestCase):
    def test_zettelkasten_manager_initialization(self):
        from b3fileorganizer.core.zettelkasten import ZettelkastenManager
        manager = ZettelkastenManager()
        self.assertIsNotNone(manager)
        self.assertTrue(hasattr(manager, 'create_zettel_card'))
        self.assertTrue(hasattr(manager, 'get_statistics'))
        stats = manager.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_cards', stats)

    def test_create_and_retrieve_zettel_card(self):
        from b3fileorganizer.core.zettelkasten import ZettelkastenManager
        manager = ZettelkastenManager()
        content = 'Test Zettel Content'
        title = f'Test Zettel {datetime.now().isoformat()}'
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