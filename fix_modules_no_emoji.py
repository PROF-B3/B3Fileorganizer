print("B3Computer Manual Module Creation - Fixed Version")
print("=" * 50)

import os
from pathlib import Path

# Create modules directory
Path("modules").mkdir(exist_ok=True)
print("Created modules/ directory")

# Create __init__.py for modules
with open("modules/__init__.py", "w", encoding='utf-8') as f:
    f.write("# B3Computer Enhanced Modules\n")

# 1. Internet Access Module (no emojis in code)
internet_code = '''import requests
import urllib.parse
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("Note: BeautifulSoup not available, basic search only")

class InternetAccess:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 Academic Research Bot'})
    
    def search_scholar(self, query, max_results=5):
        """Search Google Scholar"""
        print(f"Searching Scholar for: {query}")
        try:
            url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(query)}"
            response = self.session.get(url, timeout=10)
            
            if BS4_AVAILABLE:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                for i, result in enumerate(soup.find_all('div', class_='gs_ri')[:max_results]):
                    title_elem = result.find('h3')
                    title = title_elem.get_text() if title_elem else f"Paper {i+1}"
                    results.append({'title': title[:100], 'source': 'Google Scholar'})
                return results
            else:
                return [{'title': f'Search result for: {query}', 'source': 'Scholar (basic)'}]
                
        except Exception as e:
            print(f"Search error: {e}")
            return [{'title': f'Search unavailable for: {query}', 'source': 'Error'}]
    
    def search_multiple_topics(self, topics):
        """Search multiple academic topics"""
        all_results = []
        for topic in topics:
            results = self.search_scholar(topic)
            all_results.extend(results)
        return all_results
'''

with open("modules/internet_access.py", "w", encoding='utf-8') as f:
    f.write(internet_code)
print("Created internet_access.py")

# 2. Deadline Manager
deadline_code = '''from datetime import datetime, timedelta
import json

class DeadlineManager:
    def __init__(self, target_pages=20):
        self.deadline = datetime.now() + timedelta(hours=26)  # Tomorrow evening
        self.target_pages = target_pages
        self.completed_pages = 0
        self.start_time = datetime.now()
    
    def get_status(self):
        """Get current project status"""
        now = datetime.now()
        remaining = self.deadline - now
        elapsed = now - self.start_time
        
        hours_remaining = max(0, remaining.total_seconds() / 3600)
        pages_remaining = max(0, self.target_pages - self.completed_pages)
        
        if hours_remaining > 0:
            pages_per_hour_needed = pages_remaining / hours_remaining
        else:
            pages_per_hour_needed = float('inf')
        
        urgency = "CRITICAL" if hours_remaining < 6 else "HIGH" if hours_remaining < 12 else "MEDIUM"
        
        return {
            "hours_remaining": hours_remaining,
            "pages_remaining": pages_remaining,
            "pages_per_hour_needed": pages_per_hour_needed,
            "urgency": urgency,
            "completion_rate": (self.completed_pages / self.target_pages) * 100
        }
    
    def update_progress(self, pages):
        """Update completed pages"""
        self.completed_pages = pages
        status = self.get_status()
        print(f"Progress: {pages}/{self.target_pages} pages ({status['completion_rate']:.1f}%)")
        print(f"Time remaining: {status['hours_remaining']:.1f} hours")
        print(f"Need to write: {status['pages_per_hour_needed']:.1f} pages/hour")
        return status
    
    def get_recommendations(self):
        """Get writing recommendations based on status"""
        status = self.get_status()
        
        if status['urgency'] == 'CRITICAL':
            return [
                "EMERGENCY MODE: Focus only on core content",
                "Use bullet points and shorter paragraphs", 
                "Heavily quote existing sources",
                "Skip detailed citations for now"
            ]
        elif status['urgency'] == 'HIGH':
            return [
                "SPEED MODE: Write first, edit later",
                "Use AI to help generate content",
                "Extract heavily from existing papers",
                "Set hourly writing targets"
            ]
        else:
            return [
                "QUALITY MODE: Focus on good structure",
                "Thorough research and citations", 
                "Edit as you go",
                "Regular progress checks"
            ]
'''

with open("modules/deadline_manager.py", "w", encoding='utf-8') as f:
    f.write(deadline_code)
print("Created deadline_manager.py")

# 3. Academic Coordinator
coordinator_code = '''import os
from pathlib import Path
from modules.internet_access import InternetAccess
from modules.deadline_manager import DeadlineManager

class AcademicCoordinator:
    def __init__(self):
        try:
            self.internet = InternetAccess()
        except Exception as e:
            print(f"Internet module error: {e}")
            self.internet = None
            
        self.deadline_mgr = DeadlineManager()
        self.project_data = {
            "existing_files": [],
            "papers_found": [],
            "topics_researched": [],
            "content_synthesized": 0
        }
    
    def analyze_existing_work(self, directory="./"):
        """Analyze user's existing exposees and papers"""
        print(f"Analyzing existing work in: {directory}")
        
        extensions = ['.pdf', '.doc', '.docx', '.txt', '.md']
        files = []
        
        for ext in extensions:
            found = list(Path(directory).glob(f"**/*{ext}"))
            files.extend(found)
        
        self.project_data["existing_files"] = [str(f) for f in files]
        
        print(f"Found {len(files)} existing documents:")
        for f in files[:10]:  # Show first 10
            print(f"  - {f.name}")
        
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more")
            
        return files
    
    def search_academic_papers(self, topics):
        """Search for relevant academic papers"""
        print(f"Searching for papers on {len(topics)} topics...")
        
        if not self.internet:
            print("Internet access not available")
            return []
        
        all_papers = []
        for topic in topics:
            try:
                papers = self.internet.search_scholar(topic)
                all_papers.extend(papers)
                print(f"  Found {len(papers)} papers for: {topic}")
            except Exception as e:
                print(f"  Search failed for {topic}: {e}")
        
        self.project_data["papers_found"] = all_papers
        self.project_data["topics_researched"] = topics
        return all_papers
    
    def get_project_status(self):
        """Get comprehensive project status"""
        deadline_status = self.deadline_mgr.get_status()
        
        return {
            **deadline_status,
            "existing_files": len(self.project_data["existing_files"]),
            "papers_found": len(self.project_data["papers_found"]),
            "topics_researched": len(self.project_data["topics_researched"]),
            "ready_for_writing": len(self.project_data["existing_files"]) > 0 or len(self.project_data["papers_found"]) > 0,
            "recommendations": self.deadline_mgr.get_recommendations()
        }
    
    def generate_content_plan(self):
        """Generate a plan for the 20 pages"""
        status = self.get_project_status()
        
        plan = {
            "introduction": 2,
            "literature_review": 4, 
            "methodology": 3,
            "main_content": 8,
            "conclusion": 2,
            "references": 1
        }
        
        print("SUGGESTED 20-PAGE STRUCTURE:")
        for section, pages in plan.items():
            print(f"  {section.title()}: {pages} pages")
            
        return plan
'''

with open("modules/academic_coordinator.py", "w", encoding='utf-8') as f:
    f.write(coordinator_code)
print("Created academic_coordinator.py")

print("\nAll B3Computer academic modules created successfully!")
print("Created in modules/ directory:")
print("  - internet_access.py")
print("  - deadline_manager.py") 
print("  - academic_coordinator.py")

print("\nB3Computer is now enhanced for academic research!")