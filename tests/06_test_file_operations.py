#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 06: File Operations
Tests file operations, directory scanning, and file management.

This test verifies that the system can scan directories, analyze files,
and perform basic file operations. It's essential for file organization.

Copyright (C) 2073-2025 Prof. B3, University of Temporal Transfer
"O copyright e d'o pateterno" - Copyright belongs to the ancestors
"""

import unittest
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestFileOperations(unittest.TestCase):
    def setUp(self):
        self.test_file = Path('test_temp_file.txt')
        self.test_file.write_text('Hello, world!')

    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()

    def test_file_exists_and_read(self):
        from b3fileorganizer.utils.file_operations import FileOperations
        ops = FileOperations()
        self.assertTrue(self.test_file.exists())
        content = self.test_file.read_text()
        self.assertEqual(content, 'Hello, world!')

    def test_file_move_and_rename(self):
        from b3fileorganizer.utils.file_operations import FileOperations
        ops = FileOperations()
        move_path = Path('test_temp_file_moved.txt')
        try:
            # Move file
            result = ops.move_file(str(self.test_file), str(move_path))
            self.assertTrue(result)
            self.assertTrue(move_path.exists())
            # Rename file
            result = ops.rename_file(str(move_path), 'test_temp_file_renamed.txt')
            self.assertTrue(result)
            renamed_path = Path('test_temp_file_renamed.txt')
            self.assertTrue(renamed_path.exists())
        finally:
            for p in [self.test_file, move_path, Path('test_temp_file_renamed.txt')]:
                if p.exists():
                    p.unlink()

if __name__ == '__main__':
    unittest.main() 