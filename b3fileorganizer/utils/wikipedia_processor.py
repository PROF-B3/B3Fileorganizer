"""
Wikipedia Processor for B3FileOrganizer
Handles Wikipedia dump processing and integration with Zettelkasten system.
"""

import xml.etree.ElementTree as ET
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Generator
import re
from datetime import datetime
import gzip
import bz2

logger = logging.getLogger(__name__)

class WikipediaProcessor:
    """Processes Wikipedia dumps for Zettelkasten integration."""
    
    def __init__(self, ai_manager=None):
        self.ai_manager = ai_manager
        self.logger = logging.getLogger(__name__)
        self.processed_articles = []
        self.zettel_cards = []
    
    def process_wikipedia_dump(self, dump_path: str, output_dir: str = "databases/wikipedia") -> Dict[str, Any]:
        """Process Wikipedia XML dump and extract articles."""
        try:
            dump_path_obj = Path(dump_path)
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Processing Wikipedia dump: {dump_path}")
            
            # Determine file type and open accordingly
            if dump_path_obj.suffix == '.bz2':
                opener = bz2.open
            elif dump_path_obj.suffix == '.gz':
                opener = gzip.open
            else:
                opener = open
            
            # Process the dump
            articles = []
            total_processed = 0
            
            with opener(dump_path, 'rb') as f:
                # Use iterparse for memory efficiency
                context = ET.iterparse(f, events=('start', 'end'))
                
                for event, elem in context:
                    if event == 'end' and elem.tag.endswith('page'):
                        article = self._extract_article(elem)
                        if article:
                            articles.append(article)
                            total_processed += 1
                            
                            # Save in batches
                            if len(articles) >= 1000:
                                self._save_articles_batch(articles, output_path, total_processed)
                                articles = []
                        
                        # Clear element to free memory
                        elem.clear()
            
            # Save remaining articles
            if articles:
                self._save_articles_batch(articles, output_path, total_processed)
            
            self.logger.info(f"Processed {total_processed} articles from Wikipedia dump")
            
            return {
                "success": True,
                "total_articles": total_processed,
                "output_directory": str(output_path)
            }
            
        except Exception as e:
            self.logger.error(f"Error processing Wikipedia dump: {e}")
            return {"error": str(e)}
    
    def _extract_article(self, page_elem) -> Optional[Dict[str, Any]]:
        """Extract article data from XML element."""
        try:
            # Get basic page info
            title_elem = page_elem.find('.//title')
            ns_elem = page_elem.find('.//ns')
            text_elem = page_elem.find('.//text')
            
            if not title_elem or not text_elem:
                return None
            
            title = title_elem.text
            namespace = int(ns_elem.text) if ns_elem is not None else 0
            text = text_elem.text or ""
            
            # Only process main namespace articles (namespace 0)
            if namespace != 0:
                return None
            
            # Skip redirects and special pages
            if text.startswith('#REDIRECT') or text.startswith('#redirect'):
                return None
            
            # Clean and process text
            cleaned_text = self._clean_wiki_text(text)
            
            if len(cleaned_text) < 100:  # Skip very short articles
                return None
            
            return {
                "title": title,
                "text": cleaned_text,
                "length": len(cleaned_text),
                "extracted_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting article: {e}")
            return None
    
    def _clean_wiki_text(self, text: str) -> str:
        """Clean Wikipedia markup text."""
        # Remove wiki markup
        text = re.sub(r'\[\[([^|\]]*?)\]\]', r'\1', text)  # Simple links
        text = re.sub(r'\[\[([^|\]]*?)\|([^\]]*?)\]\]', r'\2', text)  # Named links
        text = re.sub(r'\[\[([^|\]]*?)\|([^\]]*?)\|([^\]]*?)\]\]', r'\3', text)  # Complex links
        text = re.sub(r'\[\[([^|\]]*?)\|([^\]]*?)\|([^\]]*?)\|([^\]]*?)\]\]', r'\4', text)  # Very complex links
        
        # Remove other wiki markup
        text = re.sub(r'{{[^}]*}}', '', text)  # Templates
        text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)  # References
        text = re.sub(r'<ref[^>]*/>', '', text)  # Self-closing references
        text = re.sub(r'==+([^=]+)==+', r'\1', text)  # Headers
        text = re.sub(r'__[^_]*__', '', text)  # Magic words
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)  # Comments
        
        # Clean up whitespace
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        text = text.strip()
        
        return text
    
    def _save_articles_batch(self, articles: List[Dict], output_path: Path, batch_num: int):
        """Save a batch of articles to JSON file."""
        batch_file = output_path / f"articles_batch_{batch_num:06d}.json"
        
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Saved batch {batch_num} with {len(articles)} articles")
    
    def create_zettel_cards(self, articles: List[Dict], output_dir: str = "databases/zettelkasten") -> Dict[str, Any]:
        """Create Zettelkasten cards from Wikipedia articles."""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Creating Zettelkasten cards from {len(articles)} articles")
            
            zettel_cards = []
            card_number = 1
            
            for article in articles:
                if self.ai_manager:
                    # Use AI to analyze and create structured card
                    card = self._create_ai_enhanced_card(article, card_number)
                else:
                    # Create basic card
                    card = self._create_basic_card(article, card_number)
                
                if card:
                    zettel_cards.append(card)
                    card_number += 1
            
            # Save cards
            cards_file = output_path / "zettel_cards.json"
            with open(cards_file, 'w', encoding='utf-8') as f:
                json.dump(zettel_cards, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Created {len(zettel_cards)} Zettelkasten cards")
            
            return {
                "success": True,
                "cards_created": len(zettel_cards),
                "output_file": str(cards_file)
            }
            
        except Exception as e:
            self.logger.error(f"Error creating Zettelkasten cards: {e}")
            return {"error": str(e)}
    
    def _create_basic_card(self, article: Dict, card_number: int) -> Dict[str, Any]:
        """Create a basic Zettelkasten card without AI enhancement."""
        # Extract key information
        title = article["title"]
        text = article["text"]
        
        # Create basic structure
        card = {
            "id": f"{card_number:04d}",
            "title": title,
            "content": text[:2000] + "..." if len(text) > 2000 else text,
            "type": "wikipedia_article",
            "source": "wikipedia_dump",
            "created_at": datetime.now().isoformat(),
            "tags": self._extract_basic_tags(title, text),
            "references": [],
            "cross_references": []
        }
        
        return card
    
    def _create_ai_enhanced_card(self, article: Dict, card_number: int) -> Dict[str, Any]:
        """Create an AI-enhanced Zettelkasten card."""
        try:
            title = article["title"]
            text = article["text"][:1500]  # Limit for AI processing
            
            # Use AI to analyze content
            prompt = f"""
            Analyze this Wikipedia article and create a Zettelkasten card:
            
            Title: {title}
            Content: {text}
            
            Please provide:
            1. Key themes and topics (comma-separated)
            2. Main concepts (3-5 key points)
            3. Related topics for cross-references
            4. Suggested tags
            
            Format as JSON with keys: themes, concepts, related_topics, tags
            """
            
            if self.ai_manager:
                response = self.ai_manager.generate_response(prompt, model_name="mixtral")
            else:
                response = "{}"
            
            # Parse AI response
            try:
                ai_analysis = json.loads(response)
            except json.JSONDecodeError:
                # Fallback to basic analysis
                ai_analysis = {
                    "themes": [],
                    "concepts": [],
                    "related_topics": [],
                    "tags": self._extract_basic_tags(title, text)
                }
            
            card = {
                "id": f"{card_number:04d}",
                "title": title,
                "content": text,
                "type": "wikipedia_article",
                "source": "wikipedia_dump",
                "created_at": datetime.now().isoformat(),
                "ai_enhanced": True,
                "themes": ai_analysis.get("themes", []),
                "concepts": ai_analysis.get("concepts", []),
                "related_topics": ai_analysis.get("related_topics", []),
                "tags": ai_analysis.get("tags", []),
                "references": [],
                "cross_references": []
            }
            
            return card
            
        except Exception as e:
            self.logger.error(f"Error creating AI-enhanced card: {e}")
            return self._create_basic_card(article, card_number)
    
    def _extract_basic_tags(self, title: str, text: str) -> List[str]:
        """Extract basic tags from title and text."""
        tags = []
        
        # Extract from title
        title_words = re.findall(r'\b[A-Z][a-z]+\b', title)
        tags.extend(title_words[:3])
        
        # Extract from text (first 500 chars)
        text_sample = text[:500]
        common_topics = [
            "history", "science", "technology", "culture", "geography",
            "politics", "economics", "art", "literature", "philosophy",
            "mathematics", "physics", "chemistry", "biology", "medicine"
        ]
        
        for topic in common_topics:
            if topic.lower() in text_sample.lower():
                tags.append(topic)
        
        return list(set(tags))[:5]  # Remove duplicates and limit
    
    def load_processed_articles(self, articles_dir: str) -> List[Dict]:
        """Load processed articles from directory."""
        articles = []
        articles_path = Path(articles_dir)
        
        if not articles_path.exists():
            return articles
        
        for json_file in articles_path.glob("articles_batch_*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    batch_articles = json.load(f)
                    articles.extend(batch_articles)
            except Exception as e:
                self.logger.error(f"Error loading {json_file}: {e}")
        
        return articles
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            "articles_processed": len(self.processed_articles),
            "zettel_cards_created": len(self.zettel_cards),
            "ai_enhanced_cards": len([c for c in self.zettel_cards if c.get("ai_enhanced", False)])
        } 