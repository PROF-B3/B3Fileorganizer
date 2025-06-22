import os
import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

CARD_INDEX_PATH = Path("b3fileorganizer/X/_metadata/card_index.json")
ZETTEL_DIR = Path("X")
DB_PATH = Path("b3fileorganizer/databases/zettel_index.db")

class ZettelIndexer:
    def __init__(self, db_path: Path = DB_PATH, card_index_path: Path = CARD_INDEX_PATH, zettel_dir: Path = ZETTEL_DIR):
        self.db_path = db_path
        self.card_index_path = card_index_path
        self.zettel_dir = zettel_dir
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()
        self.card_index = self._load_card_index()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS zettel_index (
            zettel_number TEXT PRIMARY KEY,
            title TEXT,
            category TEXT,
            tags TEXT,
            cross_references TEXT,
            file_path TEXT,
            content_preview TEXT
        )''')
        self.conn.commit()

    def _load_card_index(self) -> Dict[str, Any]:
        if self.card_index_path.exists():
            with open(self.card_index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def index_all(self):
        """Rebuild the entire index from scratch."""
        c = self.conn.cursor()
        c.execute('DELETE FROM zettel_index')
        for zettel_number, meta in self.card_index.items():
            file_path = Path(meta["file_path"])
            title = meta.get("title", "")
            category = meta.get("category", "")
            tags = json.dumps(meta.get("tags", []))
            cross_refs = json.dumps(meta.get("cross_references", []))
            content_preview = ""
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # Use first non-empty line as title if not in meta
                        if not title:
                            for line in lines:
                                if line.strip():
                                    title = line.strip()
                                    break
                        content_preview = ''.join(lines[:10])[:500]
                except Exception:
                    content_preview = "[Error reading file]"
            c.execute('''REPLACE INTO zettel_index (zettel_number, title, category, tags, cross_references, file_path, content_preview)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (zettel_number, title, category, tags, cross_refs, str(file_path), content_preview))
        self.conn.commit()

    def update_card(self, zettel_number: str):
        """Update a single card in the index."""
        meta = self.card_index.get(zettel_number)
        if not meta:
            return
        file_path = Path(meta["file_path"])
        title = meta.get("title", "")
        category = meta.get("category", "")
        tags = json.dumps(meta.get("tags", []))
        cross_refs = json.dumps(meta.get("cross_references", []))
        content_preview = ""
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if not title:
                        for line in lines:
                            if line.strip():
                                title = line.strip()
                                break
                    content_preview = ''.join(lines[:10])[:500]
            except Exception:
                content_preview = "[Error reading file]"
        c = self.conn.cursor()
        c.execute('''REPLACE INTO zettel_index (zettel_number, title, category, tags, cross_references, file_path, content_preview)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (zettel_number, title, category, tags, cross_refs, str(file_path), content_preview))
        self.conn.commit()

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search index by title, category, or tags."""
        c = self.conn.cursor()
        like = f"%{query}%"
        results = c.execute('''SELECT zettel_number, title, category, tags, cross_references, file_path, content_preview
                               FROM zettel_index
                               WHERE title LIKE ? OR category LIKE ? OR tags LIKE ?''',
                            (like, like, like)).fetchall()
        return [
            {
                "zettel_number": row[0],
                "title": row[1],
                "category": row[2],
                "tags": json.loads(row[3]),
                "cross_references": json.loads(row[4]),
                "file_path": row[5],
                "content_preview": row[6]
            }
            for row in results
        ]

    def get_card(self, zettel_number: str) -> Optional[Dict[str, Any]]:
        c = self.conn.cursor()
        row = c.execute('''SELECT zettel_number, title, category, tags, cross_references, file_path, content_preview
                           FROM zettel_index WHERE zettel_number = ?''', (zettel_number,)).fetchone()
        if not row:
            return None
        return {
            "zettel_number": row[0],
            "title": row[1],
            "category": row[2],
            "tags": json.loads(row[3]),
            "cross_references": json.loads(row[4]),
            "file_path": row[5],
            "content_preview": row[6]
        } 