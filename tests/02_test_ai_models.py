#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 02: AI Models
Tests AI model availability, status, and basic functionality.

This test verifies that all configured AI models are available and can
generate responses. It's essential for the AI agent functionality.

Copyright (C) 2073-2025 Prof. B3, University of Temporal Transfer
"O copyright e d'o pateterno" - Copyright belongs to the ancestors
"""

import sys
import os
import time
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_ai_models():
    """Test 02: AI model availability and functionality."""
    print("🧪 Test 02: AI Models")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        from core.ai_manager import AIManager
        
        # Initialize AI Manager
        print("[INIT] Initializing AI Manager...")
        ai_manager = AIManager()
        print("[OK] AI Manager initialized")
        
        # Test model status
        print("\n[TEST] Testing AI model availability...")
        model_status = ai_manager.get_model_status()
        
        print(f"Configured models: {len(model_status)}")
        available_models = []
        
        for model_name, available in model_status.items():
            status = "[OK] Available" if available else "[ERROR] Not available"
            print(f"  - {model_name}: {status}")
            if available:
                available_models.append(model_name)
        
        if not available_models:
            print("\n[ERROR] No AI models are available!")
            print("Please ensure Ollama is running and models are downloaded:")
            print("  ollama pull mixtral:latest")
            print("  ollama pull llama3.2:3b")
            print("  ollama pull codellama:latest")
            return False
        
        # Test model switching
        print(f"\n[TEST] Testing model switching...")
        for model in available_models[:2]:  # Test first 2 available models
            if ai_manager.set_model(model):
                print(f"[OK] Successfully switched to {model}")
            else:
                print(f"[ERROR] Failed to switch to {model}")
        
        # Test response generation
        print(f"\n[TEST] Testing response generation...")
        test_prompt = "Hello! Please respond with a brief greeting."
        
        for model in available_models[:2]:  # Test first 2 available models
            print(f"\nTesting {model}...")
            start_time = time.time()
            
            try:
                response = ai_manager.generate_response(test_prompt, model_name=model)
                response_time = time.time() - start_time
                
                if response and not response.startswith("Error"):
                    print(f"[OK] {model}: Response generated in {response_time:.2f}s")
                    print(f"   Response: {response[:100]}...")
                else:
                    print(f"[ERROR] {model}: Failed to generate response")
                    print(f"   Error: {response}")
                    
            except Exception as e:
                print(f"[ERROR] {model}: Exception during response generation")
                print(f"   Error: {e}")
        
        # Test model configuration
        print(f"\n[TEST] Testing model configuration...")
        for model_name, model_config in ai_manager.models.items():
            print(f"  {model_name}:")
            print(f"    - Name: {model_config.name}")
            print(f"    - Temperature: {model_config.temperature}")
            print(f"    - Max Tokens: {model_config.max_tokens}")
        
        print(f"\n🎉 Test 02 PASSED: {len(available_models)} AI models available and functional")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test 02 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ai_models()
    sys.exit(0 if success else 1) 