#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 01: System Initialization
Tests basic system component loading and initialization.

This test verifies that all core components can be imported and initialized
without errors. It's the foundation for all other tests.

Copyright (C) 2073-2025 Prof. B3, University of Temporal Transfer
"O copyright e d'o pateterno" - Copyright belongs to the ancestors
"""

import sys
import os
import unittest
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSystemInitialization(unittest.TestCase):
    def test_system_initialization(self):
        """Test 01: System initialization and component loading."""
        print("🧪 Test 01: System Initialization")
        print("=" * 50)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        components = {}
        success = True
        try:
            # Test core component imports
            print("📋 Testing core component imports...")
            from b3fileorganizer.core.ai_manager import AIManager
            from b3fileorganizer.core.database_manager import DatabaseManager
            from b3fileorganizer.core.resource_monitor import ResourceMonitor
            from b3fileorganizer.core.config_manager import ConfigManager
            from b3fileorganizer.core.progress_tracker import ProgressTracker
            from b3fileorganizer.core.zettelkasten import ZettelkastenManager
            from b3fileorganizer.core.enhanced_orchestrator import ErweiterterOrchestrator
            print("[OK] Core components imported successfully")
            # Test utility component imports
            print("\n📋 Testing utility component imports...")
            from b3fileorganizer.utils.file_operations import FileOperations
            from b3fileorganizer.utils.conversation_logger import ConversationLogger
            from b3fileorganizer.utils.report_generator import ReportGenerator
            from b3fileorganizer.utils.status_monitor import StatusMonitor
            from b3fileorganizer.utils.wikipedia_processor import WikipediaProcessor
            print("[OK] Utility components imported successfully")
            # Initialize components
            print("\n🔧 Initializing components...")
            components['ai_manager'] = AIManager()
            print("[OK] AI Manager initialized")
            components['db_manager'] = DatabaseManager()
            print("[OK] Database Manager initialized")
            components['resource_monitor'] = ResourceMonitor()
            print("[OK] Resource Monitor initialized")
            components['config_manager'] = ConfigManager()
            print("[OK] Configuration Manager initialized")
            components['progress_tracker'] = ProgressTracker()
            print("[OK] Progress Tracker initialized")
            components['zettel_manager'] = ZettelkastenManager()
            print("[OK] Zettelkasten Manager initialized")
            components['orchestrator'] = ErweiterterOrchestrator()
            print("[OK] Enhanced Orchestrator initialized")
            components['file_ops'] = FileOperations()
            print("[OK] File Operations initialized")
            components['conversation_logger'] = ConversationLogger()
            print("[OK] Conversation Logger initialized")
            components['report_generator'] = ReportGenerator()
            print("[OK] Report Generator initialized")
            components['status_monitor'] = StatusMonitor()
            print("[OK] Status Monitor initialized")
            components['wikipedia_processor'] = WikipediaProcessor()
            print("[OK] Wikipedia Processor initialized")
            print(f"\n[OK] All {len(components)} components initialized successfully")
            # Test component attributes
            print("\n🔍 Testing component attributes...")
            for name, component in components.items():
                if hasattr(component, '__class__'):
                    print(f"[OK] {name}: {component.__class__.__name__}")
                else:
                    print(f"[ERROR] {name}: Missing class attribute")
                    success = False
            self.assertTrue(success, "Some components have issues")
        except ImportError as e:
            self.fail(f"Import error: {e}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.fail(f"Initialization error: {e}") 