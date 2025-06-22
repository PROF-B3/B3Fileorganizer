"""
Database Manager for B3Team
Handles SQLite database operations and learning system.
"""

import sqlite3
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import threading

class DatabaseManager:
    """Manages SQLite databases for learning and organization tracking."""
    
    def __init__(self, db_path: str = "databases/b3team.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.lock = threading.Lock()
        self.init_database()
    
    def init_database(self):
        """Initialize database tables."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Organization history table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS organization_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_path TEXT NOT NULL,
                        original_name TEXT NOT NULL,
                        new_name TEXT,
                        category TEXT,
                        zettel_number TEXT,
                        confidence_score REAL,
                        user_approved BOOLEAN,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        agent_name TEXT DEFAULT 'B3FileOrganizer'
                    )
                ''')
                
                # Learning patterns table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS learning_patterns (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pattern_type TEXT NOT NULL,
                        pattern_data TEXT NOT NULL,
                        success_count INTEGER DEFAULT 0,
                        failure_count INTEGER DEFAULT 0,
                        last_used DATETIME DEFAULT CURRENT_TIMESTAMP,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Agent interactions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS agent_interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source_agent TEXT NOT NULL,
                        target_agent TEXT NOT NULL,
                        interaction_type TEXT NOT NULL,
                        request_data TEXT,
                        response_data TEXT,
                        status TEXT DEFAULT 'pending',
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Video metadata table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS video_metadata (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_path TEXT NOT NULL,
                        duration REAL,
                        resolution TEXT,
                        codec TEXT,
                        bitrate INTEGER,
                        transcription TEXT,
                        summary TEXT,
                        tags TEXT,
                        processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Code snippets table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS code_snippets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        snippet_type TEXT NOT NULL,
                        language TEXT NOT NULL,
                        code TEXT NOT NULL,
                        description TEXT,
                        tags TEXT,
                        usage_count INTEGER DEFAULT 0,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_used DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # System configuration table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS system_config (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        description TEXT,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                self.logger.info("Database initialized successfully")
    
    def add_organization_record(self, file_path: str, original_name: str, 
                              new_name: Optional[str] = None, category: Optional[str] = None,
                              zettel_number: Optional[str] = None, confidence_score: Optional[float] = None,
                              user_approved: Optional[bool] = None, agent_name: str = "B3FileOrganizer"):
        """Add a record of file organization."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO organization_history 
                    (file_path, original_name, new_name, category, zettel_number, 
                     confidence_score, user_approved, agent_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (file_path, original_name, new_name, category, zettel_number, 
                     confidence_score, user_approved, agent_name))
                conn.commit()
    
    def get_organization_history(self, limit: int = 100, agent_name: Optional[str] = None) -> List[Dict]:
        """Get organization history."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if agent_name:
                    cursor.execute('''
                        SELECT * FROM organization_history 
                        WHERE agent_name = ? 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    ''', (agent_name, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM organization_history 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    ''', (limit,))
                
                return [dict(row) for row in cursor.fetchall()]
    
    def add_learning_pattern(self, pattern_type: str, pattern_data: Dict, 
                           success: bool = True):
        """Add or update a learning pattern."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if pattern exists
                cursor.execute('''
                    SELECT id, success_count, failure_count FROM learning_patterns 
                    WHERE pattern_type = ? AND pattern_data = ?
                ''', (pattern_type, json.dumps(pattern_data)))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing pattern
                    pattern_id, success_count, failure_count = existing
                    if success:
                        success_count += 1
                    else:
                        failure_count += 1
                    
                    cursor.execute('''
                        UPDATE learning_patterns 
                        SET success_count = ?, failure_count = ?, last_used = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (success_count, failure_count, pattern_id))
                else:
                    # Create new pattern
                    success_count = 1 if success else 0
                    failure_count = 0 if success else 1
                    
                    cursor.execute('''
                        INSERT INTO learning_patterns 
                        (pattern_type, pattern_data, success_count, failure_count)
                        VALUES (?, ?, ?, ?)
                    ''', (pattern_type, json.dumps(pattern_data), success_count, failure_count))
                
                conn.commit()
    
    def get_learning_patterns(self, pattern_type: str, limit: int = 10) -> List[Dict]:
        """Get learning patterns by type, ordered by success rate."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT *, 
                           (success_count * 1.0 / (success_count + failure_count)) as success_rate
                    FROM learning_patterns 
                    WHERE pattern_type = ? 
                    ORDER BY success_rate DESC, last_used DESC
                    LIMIT ?
                ''', (pattern_type, limit))
                
                return [dict(row) for row in cursor.fetchall()]
    
    def add_agent_interaction(self, source_agent: str, target_agent: str, 
                            interaction_type: str, request_data: Dict,
                            response_data: Optional[Dict] = None, status: str = "pending"):
        """Record an interaction between agents."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO agent_interactions 
                    (source_agent, target_agent, interaction_type, request_data, response_data, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (source_agent, target_agent, interaction_type, 
                     json.dumps(request_data), 
                     json.dumps(response_data) if response_data else None,
                     status))
                conn.commit()
    
    def get_agent_interactions(self, agent_name: Optional[str] = None, 
                             status: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Get agent interactions."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                query = "SELECT * FROM agent_interactions WHERE 1=1"
                params = []
                
                if agent_name:
                    query += " AND (source_agent = ? OR target_agent = ?)"
                    params.extend([agent_name, agent_name])
                
                if status:
                    query += " AND status = ?"
                    params.append(status)
                
                query += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
    
    def add_video_metadata(self, file_path: str, duration: Optional[float] = None,
                          resolution: Optional[str] = None, codec: Optional[str] = None,
                          bitrate: Optional[int] = None, transcription: Optional[str] = None,
                          summary: Optional[str] = None, tags: Optional[List[str]] = None):
        """Add video metadata."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO video_metadata 
                    (file_path, duration, resolution, codec, bitrate, transcription, summary, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (file_path, duration, resolution, codec, bitrate, transcription, summary,
                     json.dumps(tags) if tags else None))
                conn.commit()
    
    def get_video_metadata(self, file_path: Optional[str] = None) -> List[Dict]:
        """Get video metadata."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if file_path:
                    cursor.execute('SELECT * FROM video_metadata WHERE file_path = ?', (file_path,))
                else:
                    cursor.execute('SELECT * FROM video_metadata ORDER BY processed_at DESC')
                
                return [dict(row) for row in cursor.fetchall()]
    
    def add_code_snippet(self, snippet_type: str, language: str, code: str,
                        description: Optional[str] = None, tags: Optional[List[str]] = None):
        """Add a code snippet."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO code_snippets 
                    (snippet_type, language, code, description, tags)
                    VALUES (?, ?, ?, ?, ?)
                ''', (snippet_type, language, code, description,
                     json.dumps(tags) if tags else None))
                conn.commit()
    
    def get_code_snippets(self, snippet_type: Optional[str] = None, 
                         language: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Get code snippets."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                query = "SELECT * FROM code_snippets WHERE 1=1"
                params = []
                
                if snippet_type:
                    query += " AND snippet_type = ?"
                    params.append(snippet_type)
                
                if language:
                    query += " AND language = ?"
                    params.append(language)
                
                query += " ORDER BY usage_count DESC, last_used DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
    
    def set_config(self, key: str, value: Any, description: Optional[str] = None):
        """Set a configuration value."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO system_config (key, value, description)
                    VALUES (?, ?, ?)
                ''', (key, json.dumps(value), description))
                conn.commit()
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT value FROM system_config WHERE key = ?', (key,))
                result = cursor.fetchone()
                
                if result:
                    try:
                        return json.loads(result[0])
                    except json.JSONDecodeError:
                        return result[0]
                return default
    
    def record_organization(self, original_name: str, new_name: str, 
                           category: str, operation: str):
        """Record a file organization operation (alias for add_organization_record)."""
        self.add_organization_record(
            file_path=original_name,
            original_name=original_name,
            new_name=new_name,
            category=category,
            agent_name="B3FileOrganizer"
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Count records in each table
                tables = ['organization_history', 'learning_patterns', 'agent_interactions', 
                         'video_metadata', 'code_snippets', 'system_config']
                
                for table in tables:
                    cursor.execute(f'SELECT COUNT(*) FROM {table}')
                    stats[f'{table}_count'] = cursor.fetchone()[0]
                
                # Get recent activity
                cursor.execute('''
                    SELECT COUNT(*) FROM organization_history 
                    WHERE timestamp > datetime('now', '-24 hours')
                ''')
                stats['recent_organizations'] = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT COUNT(*) FROM agent_interactions 
                    WHERE timestamp > datetime('now', '-24 hours')
                ''')
                stats['recent_interactions'] = cursor.fetchone()[0]
                
                return stats 