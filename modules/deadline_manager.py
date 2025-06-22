from datetime import datetime, timedelta
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
