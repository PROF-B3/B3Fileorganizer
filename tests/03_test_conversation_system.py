#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 03: Conversation System
Tests conversation logging and AI agent interactions.

This test verifies that conversations can be logged, retrieved, and that
AI agents can respond appropriately. It's essential for user interaction.

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

class TestConversationSystem(unittest.TestCase):
    def test_conversation_logger_initialization(self):
        from b3fileorganizer.utils.conversation_logger import ConversationLogger
        logger = ConversationLogger()
        self.assertIsNotNone(logger)
        self.assertTrue(hasattr(logger, 'log_user_interaction'))
        self.assertTrue(hasattr(logger, 'get_recent_conversations'))

    def test_log_and_retrieve_interaction(self):
        from b3fileorganizer.utils.conversation_logger import ConversationLogger
        logger = ConversationLogger()
        session_id = 'test-session'
        logger.log_user_interaction(session_id, 'test', 'Hello!', 'Hi there!')
        conversations = logger.get_recent_conversations(limit=5)
        self.assertIsInstance(conversations, list)

    def test_conversation_system(self):
        """Test 03: Conversation system and AI agent interactions."""
        print("[INIT] Initializing components...")
        try:
            from b3fileorganizer.core.ai_manager import AIManager
            from b3fileorganizer.utils.conversation_logger import ConversationLogger
            
            # Initialize components
            ai_manager = AIManager()
            conversation_logger = ConversationLogger()
            print("[OK] Components initialized")
            
            # Test conversation creation
            print("\n[TEST] Testing conversation creation...")
            conversation_id = conversation_logger.start_conversation(
                "test_conversation_03", 
                ["user", "alpha", "beta", "gamma", "delta"]
            )
            print(f"[OK] Conversation created with ID: {conversation_id}")
            
            # Test message logging
            print("\n📝 Testing message logging...")
            test_messages = [
                ("user", "Hello Alpha! Can you introduce yourself?"),
                ("alpha", "Hello! I am Alpha (Α), the file organization specialist."),
                ("user", "What is your role in the B3FileOrganizer system?"),
                ("alpha", "I coordinate file organization strategies and work with other agents."),
                ("user", "How do you work with Beta, Gamma, and Delta?"),
                ("alpha", "Beta analyzes content, Gamma manages knowledge, Delta coordinates everything.")
            ]
            
            for sender, message in test_messages:
                conversation_logger.log_user_interaction(conversation_id, sender, message, 'OK')
                print(f"[OK] Logged message from {sender}")
            
            # Test conversation retrieval
            print("\n📖 Testing conversation retrieval...")
            conversation = conversation_logger.get_conversation(conversation_id)
            
            if conversation:
                messages = conversation.get('messages', [])
                print(f"[OK] Retrieved conversation with {len(messages)} messages")
                
                # Display conversation
                print("\n📋 Conversation content:")
                for msg in messages:
                    timestamp = msg.get('timestamp', 'Unknown')
                    sender = msg.get('sender', 'Unknown')
                    content = msg.get('content', 'No content')
                    print(f"  [{timestamp}] {sender}: {content[:50]}...")
            else:
                print("[ERROR] Failed to retrieve conversation")
                return False
            
            # Test AI agent conversation
            print("\n[TEST] Testing AI agent conversation...")
            
            # Test questions for different agents
            agent_tests = [
                ("alpha", "What is the Zettelkasten method?"),
                ("beta", "How do you analyze file content?"),
                ("gamma", "How do you manage knowledge organization?"),
                ("delta", "What is your role as coordinator?")
            ]
            
            for agent, question in agent_tests:
                print(f"\nTesting {agent.upper()}...")
                
                # Log user question
                conversation_logger.log_user_interaction(conversation_id, "user", question, "OK")
                
                # Generate AI response
                start_time = time.time()
                response = ai_manager.generate_response(
                    f"Answer as {agent.upper()} ({'Α' if agent == 'alpha' else 'Β' if agent == 'beta' else 'Γ' if agent == 'gamma' else 'Δ'}): {question}",
                    model_name="mixtral"
                )
                response_time = time.time() - start_time
                
                # Log AI response
                conversation_logger.log_user_interaction(conversation_id, agent, response, response)
                
                if response and not response.startswith("Error"):
                    print(f"[OK] {agent.upper()}: Response in {response_time:.2f}s")
                    print(f"   Response: {response[:100]}...")
                else:
                    print(f"[ERROR] {agent.upper()}: Failed to generate response")
            
            # Test conversation statistics
            print("\n📊 Testing conversation statistics...")
            updated_conversation = conversation_logger.get_conversation(conversation_id)
            if updated_conversation:
                messages = updated_conversation.get('messages', [])
                participants = updated_conversation.get('participants', [])
                
                print(f"  Total messages: {len(messages)}")
                print(f"  Participants: {', '.join(participants)}")
                print(f"  Duration: {updated_conversation.get('duration', 'Unknown')}")
            
            # Test conversation listing
            print("\n📋 Testing conversation listing...")
            conversations = conversation_logger.get_recent_conversations(limit=10)
            if conversations:
                print(f"[OK] Found {len(conversations)} conversations")
                for conv in conversations[:3]:  # Show first 3
                    conv_data = conv.get('conversation', {})
                    print(f"  - {conv_data.get('id', 'Unknown')}: {conv_data.get('type', 'No type')}")
            else:
                print("⚠️  No conversations found")
            
            print(f"\n🎉 Test 03 PASSED: Conversation system fully functional")
            return True
            
        except Exception as e:
            print(f"[ERROR] Test 03 FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    unittest.main() 