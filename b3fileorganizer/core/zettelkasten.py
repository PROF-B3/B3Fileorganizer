#!/usr/bin/env python3
"""
Zettelkasten Manager - Implements Niklas Luhmann's knowledge organization method.

Copyright (C) 2073-2025 Prof. B3, University of Temporal Transfer
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"O copyright e d'o pateterno" - Copyright belongs to the ancestors
Knowledge flows freely across timelines and dimensions.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re

class ZettelkastenManager:
    """Manages Luhmann Zettelkasten system with proper numbering and cross-references."""
    
    def __init__(self, base_path: str = "X", metadata_path: str = "X/_metadata", rules_path: str = "b3fileorganizer/config/file_and_zettel_rules.json"):
        self.base_path = Path(base_path)
        self.metadata_path = Path(metadata_path)
        self.logger = logging.getLogger(__name__)
        self.rules_path = rules_path
        self.zettel_numbering_rules = self._load_numbering_rules()
        
        # Ensure base structure exists
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        
        # Load or initialize metadata
        self.cross_references = self._load_metadata("cross_references.json", {})
        self.numbering_scheme = self._load_metadata("numbering_scheme.json", {})
        self.thematic_connections = self._load_metadata("thematic_connections.json", {})
        self.card_index = self._load_metadata("card_index.json", {})
        
        # Initialize basic structure
        self._initialize_structure()
    
    def _load_metadata(self, filename: str, default: Any) -> Any:
        """Load metadata from JSON file."""
        file_path = self.metadata_path / filename
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading {filename}: {e}")
        return default
    
    def _save_metadata(self, filename: str, data: Any):
        """Save metadata to JSON file."""
        file_path = self.metadata_path / filename
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving {filename}: {e}")
    
    def _initialize_structure(self):
        """Initialize basic Zettelkasten folder structure."""
        # Create main sections
        sections = ["1", "2", "3", "4", "5", "A", "Z"]
        for section in sections:
            section_path = self.base_path / section
            section_path.mkdir(exist_ok=True)
        
        # Create metadata files if they don't exist
        if not self.numbering_scheme:
            self.numbering_scheme = {
                "main_topics": [],
                "subtopics": {},
                "frequently_accessed": [],
                "quotes_excerpts": [],
                "last_main_topic": 0,
                "last_frequent": 0,
                "last_quote": 0
            }
            self._save_metadata("numbering_scheme.json", self.numbering_scheme)
    
    def _load_numbering_rules(self):
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                rules = json.load(f)
            return rules.get("zettel_numbering_rules", {})
        except Exception as e:
            self.logger.error(f"Error loading numbering rules: {e}")
            return {}
    
    def reload_rules(self):
        self.zettel_numbering_rules = self._load_numbering_rules()
    
    def generate_zettel_number(self, content: str, category: str = "main") -> str:
        """Generate appropriate Zettelkasten number based on content and category using config rules."""
        rules = self.zettel_numbering_rules
        if category in rules:
            rule = rules[category]
            prefix = rule.get("prefix", "")
            increment_field = rule.get("increment_field", None)
            if increment_field:
                self.numbering_scheme[increment_field] += 1
                number = f"{prefix}{self.numbering_scheme[increment_field]}"
                # Track in list if present
                list_field = None
                if category == "main":
                    list_field = "main_topics"
                elif category == "frequent":
                    list_field = "frequently_accessed"
                elif category == "quote":
                    list_field = "quotes_excerpts"
                if list_field:
                    self.numbering_scheme[list_field].append(number)
            else:
                number = "unknown"
        elif category == "subtopic" and "subtopic" in rules:
            # Subtopic logic
            parent = "1"  # default parent
            if "/" in category:
                parent = category.split("/")[0]
            if parent not in self.numbering_scheme["subtopics"]:
                self.numbering_scheme["subtopics"][parent] = []
            existing = self.numbering_scheme["subtopics"][parent]
            next_letter = self._get_next_subtopic_letter(existing)
            number = f"{parent}{next_letter}"
            self.numbering_scheme["subtopics"][parent].append(number)
        else:
            # Fallback to original logic (copied from previous version)
            if category == "frequent":
                self.numbering_scheme["last_frequent"] += 1
                number = f"A{self.numbering_scheme['last_frequent']}"
                self.numbering_scheme["frequently_accessed"].append(number)
            elif category == "quote":
                self.numbering_scheme["last_quote"] += 1
                number = f"Z{self.numbering_scheme['last_quote']}"
                self.numbering_scheme["quotes_excerpts"].append(number)
            else:
                # Main topic or subtopic
                if category == "main":
                    self.numbering_scheme["last_main_topic"] += 1
                    number = str(self.numbering_scheme["last_main_topic"])
                    self.numbering_scheme["main_topics"].append(number)
                else:
                    # Subtopic
                    parent = category.split("/")[0]
                    if parent not in self.numbering_scheme["subtopics"]:
                        self.numbering_scheme["subtopics"][parent] = []
                    existing = self.numbering_scheme["subtopics"][parent]
                    next_letter = self._get_next_subtopic_letter(existing)
                    number = f"{parent}{next_letter}"
                    self.numbering_scheme["subtopics"][parent].append(number)
        self._save_metadata("numbering_scheme.json", self.numbering_scheme)
        return number
    
    def _get_next_subtopic_letter(self, existing: List[str]) -> str:
        """Get next available subtopic letter."""
        if not existing:
            return "a"
        
        # Extract letters and find next
        letters = [item[-1] for item in existing if item[-1].isalpha()]
        if not letters:
            return "a"
        
        # Find next letter in sequence
        for i in range(26):
            letter = chr(ord('a') + i)
            if letter not in letters:
                return letter
        
        # If all letters used, start with aa, ab, etc.
        return "aa"
    
    def create_zettel_card(self, content: str, title: str, category: str = "main", 
                          cross_references: Optional[List[str]] = None, tags: Optional[List[str]] = None,
                          extra_folder_path: Optional[str] = None) -> Dict[str, Any]:
        """Create a Zettelkasten card with proper numbering and metadata. Optionally also write to an extra folder."""
        if tags is None:
            tags = []
        if cross_references is None:
            cross_references = []
        # Generate number
        zettel_number = self.generate_zettel_number(content, category)
        
        # Create card metadata
        card_data = {
            "number": zettel_number,
            "title": title,
            "content": content,
            "category": category,
            "cross_references": cross_references,
            "tags": tags,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }
        
        # Determine folder path
        if category == "frequent":
            folder_path = self.base_path / "A"
        elif category == "quote":
            folder_path = self.base_path / "Z"
        else:
            # Main topic or subtopic
            if "/" in category:
                folder_path = self.base_path / category.split("/")[0]
            else:
                folder_path = self.base_path / category
        
        # Create folder if it doesn't exist
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create card file in Zettelkasten
        card_file = folder_path / f"{zettel_number}.md"
        card_content = self._format_card_content(card_data)
        
        try:
            with open(card_file, 'w', encoding='utf-8') as f:
                f.write(card_content)
            
            # Also write to extra folder if provided
            if extra_folder_path:
                extra_folder = Path(extra_folder_path)
                extra_folder.mkdir(parents=True, exist_ok=True)
                extra_file = extra_folder / "00_zettel.md"
                with open(extra_file, 'w', encoding='utf-8') as f:
                    f.write(card_content)
            
            # Update card index
            self.card_index[zettel_number] = {
                "file_path": str(card_file),
                "title": title,
                "category": category,
                "created": card_data["created"]
            }
            
            # Add cross-references
            self._add_cross_references(zettel_number, cross_references)
            
            # Save metadata
            self._save_metadata("card_index.json", self.card_index)
            
            self.logger.info(f"Created Zettelkasten card: {zettel_number}")
            return card_data
            
        except Exception as e:
            self.logger.error(f"Error creating card {zettel_number}: {e}")
            return {"error": str(e)}
    
    def _format_card_content(self, card_data: Dict[str, Any]) -> str:
        """Format card content in Markdown with User/AI/Further Thoughts/Connections sections."""
        content = f"# {card_data['title']}\n\n"
        content += f"**Zettel Number:** {card_data['number']}  \n"
        content += f"**Category:** {card_data['category']}  \n"
        content += f"**Created:** {card_data['created']}  \n"
        content += f"**Modified:** {card_data['modified']}  \n\n"
        content += "---\n\n"
        # Kurz-Zusammenfassung
        content += "## Kurz-Zusammenfassung\n"
        content += card_data['content'].strip() + "\n\n---\n\n"
        # Weitere Gedanken
        content += "## Weitere Gedanken\n\n"
        # User section (template)
        content += "### User\n"
        content += "- #review #structure #future\n"
        content += "- (Hier kann der Benutzer eigene Gedanken, Hinweise oder Fragen eintragen.)\n\n"
        # AI section (auto-generated)
        content += "### AI\n"
        ai_hashtags, ai_comment = self._generate_ai_thoughts(card_data)
        content += f"- {ai_hashtags}\n"
        content += f"- {ai_comment}\n\n---\n\n"
        # Verbindungen zu anderen Zetteln
        content += "## Verbindungen zu anderen Zetteln\n\n"
        connections = self._find_zettel_connections(card_data)
        if connections:
            for zettel_num, hashtags, desc in connections:
                content += f"- **#{zettel_num}**: {hashtags} – {desc}\n"
        else:
            content += "- (Keine direkten Verbindungen gefunden.)\n"
        content += "\n---\n"
        return content

    def _generate_ai_thoughts(self, card_data: Dict[str, Any]) -> tuple:
        """Generate AI hashtags and a short actionable comment."""
        # Use tags and category for hashtags
        tags = card_data.get('tags', [])
        category = card_data.get('category', '')
        hashtags = [f"#{t.strip().replace(' ', '_')}" for t in tags if t]
        if category and f"#{category}" not in hashtags:
            hashtags.append(f"#{category}")
        hashtags = hashtags[:3] if hashtags else ['#organization']
        hashtags_str = ' '.join(hashtags)
        # Short comment (could be AI-generated, here templated)
        comment = f"Die KI empfiehlt, die Inhalte regelmäßig zu überprüfen und nach Bedarf zu unterteilen, um die Übersichtlichkeit zu erhöhen."
        return hashtags_str, comment

    def _find_zettel_connections(self, card_data: Dict[str, Any]) -> list:
        """Find related Zettel by keyword/tag overlap, return list of (number, hashtags, short description)."""
        results = []
        this_tags = set(card_data.get('tags', []))
        this_title_words = set(card_data.get('title', '').lower().split())
        for num, info in self.card_index.items():
            if num == card_data['number']:
                continue
            # Gather tags and title words
            tags = set(info.get('tags', []))
            title_words = set(info.get('title', '').lower().split())
            # Overlap logic
            if this_tags & tags or this_title_words & title_words:
                hashtags = ' '.join([f"#{t.strip().replace(' ', '_')}" for t in list(tags)[:3]])
                desc_words = (info.get('title', '') + ' ' + info.get('category', '')).split()[:7]
                desc = ' '.join(desc_words)
                results.append((num, hashtags, desc))
        return results
    
    def _add_cross_references(self, source_number: str, target_numbers: List[str]):
        """Add cross-references between cards."""
        if not target_numbers:
            return
        for target in target_numbers:
            # Bidirectional reference
            if source_number not in self.cross_references:
                self.cross_references[source_number] = []
            if target not in self.cross_references:
                self.cross_references[target] = []
            if target not in self.cross_references[source_number]:
                self.cross_references[source_number].append(target)
            if source_number not in self.cross_references[target]:
                self.cross_references[target].append(source_number)
        self._save_metadata("cross_references.json", self.cross_references)
    
    def find_thematic_connections(self, content: str, existing_cards: List[str] = None) -> List[str]:
        """Find thematic connections between content and existing cards."""
        if not existing_cards:
            existing_cards = list(self.card_index.keys())
        
        connections = []
        
        # Simple keyword matching (can be enhanced with AI)
        content_lower = content.lower()
        content_words = set(re.findall(r'\b\w+\b', content_lower))
        
        for card_number in existing_cards:
            if card_number in self.card_index:
                card_info = self.card_index[card_number]
                card_title = card_info.get("title", "").lower()
                card_title_words = set(re.findall(r'\b\w+\b', card_title))
                
                # Check for word overlap
                overlap = content_words.intersection(card_title_words)
                if len(overlap) >= 2:  # At least 2 words in common
                    connections.append(card_number)
        
        return connections
    
    def expand_thematic_structure(self, base_topic: str, new_content: str) -> str:
        """Expand thematic structure by creating new subtopics."""
        # Check if base topic exists
        if base_topic not in self.numbering_scheme["main_topics"]:
            # Create new main topic
            self.numbering_scheme["last_main_topic"] += 1
            base_topic = str(self.numbering_scheme["last_main_topic"])
            self.numbering_scheme["main_topics"].append(base_topic)
        
        # Create subtopic
        if base_topic not in self.numbering_scheme["subtopics"]:
            self.numbering_scheme["subtopics"][base_topic] = []
        
        next_letter = self._get_next_subtopic_letter(self.numbering_scheme["subtopics"][base_topic])
        subtopic = f"{base_topic}{next_letter}"
        self.numbering_scheme["subtopics"][base_topic].append(subtopic)
        
        self._save_metadata("numbering_scheme.json", self.numbering_scheme)
        return subtopic
    
    def get_card(self, zettel_number: str) -> Optional[Dict[str, Any]]:
        """Get card data by zettel number."""
        card_info = self.card_index.get(zettel_number)
        if not card_info:
            return None
        # Ensure lists are not None
        if card_info.get('tags') is None:
            card_info['tags'] = []
        if card_info.get('cross_references') is None:
            card_info['cross_references'] = []
        return card_info
    
    def search_cards(self, query: str) -> List[Dict[str, Any]]:
        """Search cards by query string."""
        results = []
        for card_number, card_info in self.card_index.items():
            # Ensure lists are not None
            if card_info.get('tags') is None:
                card_info['tags'] = []
            if card_info.get('cross_references') is None:
                card_info['cross_references'] = []
            if query.lower() in card_info.get('title', '').lower() or query.lower() in card_info.get('content', '').lower():
                results.append(card_info)
        return results
    
    def list_directories(self) -> list:
        """List all directories under the base_path (X)."""
        return [str(p) for p in self.base_path.iterdir() if p.is_dir()]

    def get_statistics(self) -> Dict[str, Any]:
        """Get Zettelkasten statistics, including directory list."""
        stats = {
            "total_cards": len(self.card_index),
            "main_topics": len(self.numbering_scheme["main_topics"]),
            "frequently_accessed": len(self.numbering_scheme["frequently_accessed"]),
            "quotes_excerpts": len(self.numbering_scheme["quotes_excerpts"]),
            "cross_references": len(self.cross_references),
            "subtopics": sum(len(subtopics) for subtopics in self.numbering_scheme["subtopics"].values()),
            "directories": self.list_directories()
        }
        return stats
    
    def create_frequently_accessed_card(self, file_path: str, description: str) -> str:
        """Create a card for frequently accessed files."""
        content = f"Frequently accessed file: {file_path}\n\n{description}"
        title = f"Frequently Accessed: {Path(file_path).name}"
        
        card_data = self.create_zettel_card(
            content=content,
            title=title,
            category="frequent",
            tags=["frequently-accessed", "file-reference"]
        )
        
        return card_data.get("number", "")
    
    def create_quote_card(self, quote: str, source: str, context: str = "") -> str:
        """Create a quote/excerpt card."""
        content = f"**Quote:** {quote}\n\n**Source:** {source}\n\n**Context:** {context}"
        title = f"Quote: {source}"
        
        card_data = self.create_zettel_card(
            content=content,
            title=title,
            category="quote",
            tags=["quote", "excerpt", source]
        )
        
        return card_data.get("number", "")

    def create_card(self, content: str, title: str, category: str = "main", tags: list = None) -> Dict[str, Any]:
        """Alias for create_zettel_card for compatibility"""
        if tags is None:
            tags = []
        return self.create_zettel_card(content, title, category, tags=tags) 