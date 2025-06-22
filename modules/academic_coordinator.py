import os
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
