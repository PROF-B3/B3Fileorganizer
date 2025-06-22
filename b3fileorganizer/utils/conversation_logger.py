"""
Conversation Logger for B3FileOrganizer
Archives all AI conversations and user interactions for learning and review.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sqlite3
import uuid

logger = logging.getLogger(__name__)

class ConversationLogger:
    """Manages conversation archiving and retrieval."""
    
    def __init__(self, db_path: str = "databases/conversations.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self._init_database()
    
    def _init_database(self):
        """Initialize conversation database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create conversations table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id TEXT PRIMARY KEY,
                        session_id TEXT,
                        timestamp TEXT,
                        conversation_type TEXT,
                        participants TEXT,
                        summary TEXT,
                        metadata TEXT,
                        archived_at TEXT
                    )
                """)
                
                # Create messages table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id TEXT PRIMARY KEY,
                        conversation_id TEXT,
                        timestamp TEXT,
                        sender TEXT,
                        message_type TEXT,
                        content TEXT,
                        metadata TEXT,
                        FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                    )
                """)
                
                # Create user_interactions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_interactions (
                        id TEXT PRIMARY KEY,
                        session_id TEXT,
                        timestamp TEXT,
                        interaction_type TEXT,
                        user_input TEXT,
                        system_response TEXT,
                        metadata TEXT
                    )
                """)
                
                conn.commit()
                self.logger.info("Conversation database initialized")
                
        except Exception as e:
            self.logger.error(f"Error initializing conversation database: {e}")
    
    def start_conversation(self, conversation_type: str, participants: List[str]) -> str:
        """Start a new conversation session."""
        conversation_id = str(uuid.uuid4())
        session_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO conversations 
                    (id, session_id, timestamp, conversation_type, participants, archived_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    conversation_id,
                    session_id,
                    timestamp,
                    conversation_type,
                    json.dumps(participants),
                    timestamp
                ))
                conn.commit()
                
            self.logger.info(f"Started conversation {conversation_id} with {participants}")
            return conversation_id
            
        except Exception as e:
            self.logger.error(f"Error starting conversation: {e}")
            return None
    
    def log_message(self, conversation_id: str, sender: str, content: str, 
                   message_type: str = "text", metadata: Dict = None) -> bool:
        """Log a message in a conversation."""
        message_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO messages 
                    (id, conversation_id, timestamp, sender, message_type, content, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    message_id,
                    conversation_id,
                    timestamp,
                    sender,
                    message_type,
                    content,
                    json.dumps(metadata or {})
                ))
                conn.commit()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging message: {e}")
            return False
    
    def log_user_interaction(self, session_id: str, interaction_type: str, 
                           user_input: str, system_response: str, 
                           metadata: Dict = None) -> bool:
        """Log user interaction with the system."""
        interaction_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_interactions 
                    (id, session_id, timestamp, interaction_type, user_input, system_response, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    interaction_id,
                    session_id,
                    timestamp,
                    interaction_type,
                    user_input,
                    system_response,
                    json.dumps(metadata or {})
                ))
                conn.commit()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging user interaction: {e}")
            return False
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a complete conversation."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get conversation details
                cursor.execute("""
                    SELECT * FROM conversations WHERE id = ?
                """, (conversation_id,))
                conversation = cursor.fetchone()
                
                if not conversation:
                    return None
                
                # Get all messages
                cursor.execute("""
                    SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp
                """, (conversation_id,))
                messages = cursor.fetchall()
                
                return {
                    "conversation": {
                        "id": conversation[0],
                        "session_id": conversation[1],
                        "timestamp": conversation[2],
                        "type": conversation[3],
                        "participants": json.loads(conversation[4]),
                        "summary": conversation[5],
                        "metadata": json.loads(conversation[6]) if conversation[6] else {},
                        "archived_at": conversation[7]
                    },
                    "messages": [
                        {
                            "id": msg[0],
                            "timestamp": msg[2],
                            "sender": msg[3],
                            "type": msg[4],
                            "content": msg[5],
                            "metadata": json.loads(msg[6]) if msg[6] else {}
                        }
                        for msg in messages
                    ]
                }
                
        except Exception as e:
            self.logger.error(f"Error retrieving conversation: {e}")
            return None
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversations."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM conversations ORDER BY timestamp DESC LIMIT ?
                """, (limit,))
                conversations = cursor.fetchall()
                
                return [
                    {
                        "id": conv[0],
                        "session_id": conv[1],
                        "timestamp": conv[2],
                        "type": conv[3],
                        "participants": json.loads(conv[4]),
                        "summary": conv[5],
                        "metadata": json.loads(conv[6]) if conv[6] else {},
                        "archived_at": conv[7]
                    }
                    for conv in conversations
                ]
                
        except Exception as e:
            self.logger.error(f"Error retrieving recent conversations: {e}")
            return []
    
    def search_conversations(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search conversations by content."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT c.* FROM conversations c
                    JOIN messages m ON c.id = m.conversation_id
                    WHERE m.content LIKE ? OR c.summary LIKE ?
                    ORDER BY c.timestamp DESC LIMIT ?
                """, (f"%{query}%", f"%{query}%", limit))
                conversations = cursor.fetchall()
                
                return [
                    {
                        "id": conv[0],
                        "session_id": conv[1],
                        "timestamp": conv[2],
                        "type": conv[3],
                        "participants": json.loads(conv[4]),
                        "summary": conv[5],
                        "metadata": json.loads(conv[6]) if conv[6] else {},
                        "archived_at": conv[7]
                    }
                    for conv in conversations
                ]
                
        except Exception as e:
            self.logger.error(f"Error searching conversations: {e}")
            return []
    
    def export_conversation(self, conversation_id: str, format: str = "json") -> Optional[str]:
        """Export conversation to file."""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "json":
            filename = f"databases/conversations/conversation_{conversation_id}_{timestamp}.json"
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(conversation, f, indent=2, ensure_ascii=False)
            
            return filename
        
        elif format == "txt":
            filename = f"databases/conversations/conversation_{conversation_id}_{timestamp}.txt"
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Conversation: {conversation['conversation']['type']}\n")
                f.write(f"Participants: {', '.join(conversation['conversation']['participants'])}\n")
                f.write(f"Timestamp: {conversation['conversation']['timestamp']}\n")
                f.write("="*60 + "\n\n")
                
                for message in conversation['messages']:
                    f.write(f"[{message['timestamp']}] {message['sender']}:\n")
                    f.write(f"{message['content']}\n\n")
            
            return filename
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get conversation statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total conversations
                cursor.execute("SELECT COUNT(*) FROM conversations")
                total_conversations = cursor.fetchone()[0]
                
                # Total messages
                cursor.execute("SELECT COUNT(*) FROM messages")
                total_messages = cursor.fetchone()[0]
                
                # Total user interactions
                cursor.execute("SELECT COUNT(*) FROM user_interactions")
                total_interactions = cursor.fetchone()[0]
                
                # Conversations by type
                cursor.execute("""
                    SELECT conversation_type, COUNT(*) 
                    FROM conversations 
                    GROUP BY conversation_type
                """)
                conversations_by_type = dict(cursor.fetchall())
                
                return {
                    "total_conversations": total_conversations,
                    "total_messages": total_messages,
                    "total_user_interactions": total_interactions,
                    "conversations_by_type": conversations_by_type
                }
                
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {} 