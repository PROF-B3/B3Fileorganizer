
"""
B3Computer Research Module - Dynamically Generated
Topic: the narrative preconditions of european nations in history focusing on Bakunin's biography
Field: history, kulturwissenschaften
Generated: 2025-06-22 20:09:05
"""

from modules.academic_coordinator import AcademicCoordinator
import json

class SpecializedResearchAssistant:
    def __init__(self):
        self.research_config = {'main_topic': "the narrative preconditions of european nations in history focusing on Bakunin's biography", 'keywords': ['nations', 'nationhood', 'nationalism', 'anarchy', 'historiography', 'philosophy of history', 'literature', 'culture', 'politics', 'economics and the arts'], 'directories': ['B:'], 'main_question': 'I want to explain that nations are essentially narrative constructs so it is more important to understand how they are narrated and built through narration rather than what the material preconditions were that people built on', 'field': 'history, kulturwissenschaften', 'constraints': 'I need to basically expand on two papers, history manifesto and the dissertation exposees to deliver 20 pages that summarize the first two chapters and the initial paragraph of each chapter'}
        self.coordinator = AcademicCoordinator()
        
    def get_research_info(self):
        return {
            "topic": "the narrative preconditions of european nations in history focusing on Bakunin's biography",
            "keywords": ['nations', 'nationhood', 'nationalism', 'anarchy', 'historiography', 'philosophy of history', 'literature', 'culture', 'politics', 'economics and the arts'],
            "main_question": "I want to explain that nations are essentially narrative constructs so it is more important to understand how they are narrated and built through narration rather than what the material preconditions were that people built on",
            "field": "history, kulturwissenschaften",
            "directories": ['B:'],
            "constraints": "I need to basically expand on two papers, history manifesto and the dissertation exposees to deliver 20 pages that summarize the first two chapters and the initial paragraph of each chapter"
        }
    
    def search_specialized_papers(self):
        """Search for papers specific to user's research"""
        print(f"🔍 Searching for papers on: the narrative preconditions of european nations in history focusing on Bakunin's biography")
        
        # Enhanced search based on user's specific topic
        search_terms = [
            "the narrative preconditions of european nations in history focusing on Bakunin's biography",
            f"the narrative preconditions of european nations in history focusing on Bakunin's biography history, kulturwissenschaften",
            "I want to explain that nations are essentially narrative constructs so it is more important to understand how they are narrated and built through narration rather than what the material preconditions were that people built on"
        ] + ['nations', 'nationhood', 'nationalism', 'anarchy', 'historiography', 'philosophy of history', 'literature', 'culture', 'politics', 'economics and the arts']
        
        all_papers = []
        for term in search_terms:
            papers = self.coordinator.search_academic_papers([term])
            all_papers.extend(papers)
        
        return all_papers
    
    def analyze_user_documents(self):
        """Analyze user's specific documents"""
        all_files = []
        for directory in ['B:']:
            files = self.coordinator.analyze_existing_work(directory)
            all_files.extend(files)
        return all_files
    
    def generate_research_outline(self):
        """Generate outline specific to user's research"""
        outline = {
            "title": "Research on the narrative preconditions of european nations in history focusing on Bakunin's biography",
            "introduction": {
                "pages": 2,
                "focus": "Introduce the narrative preconditions of european nations in history focusing on Bakunin's biography and research question"
            },
            "literature_review": {
                "pages": 4,
                "focus": "Review existing work on nations, nationhood, nationalism"
            },
            "methodology": {
                "pages": 3,
                "focus": "Approach to studying the narrative preconditions of european nations in history focusing on Bakunin's biography"
            },
            "main_analysis": {
                "pages": 8,
                "focus": "Deep dive into I want to explain that nations are essentially narrative constructs so it is more important to understand how they are narrated and built through narration rather than what the material preconditions were that people built on"
            },
            "conclusion": {
                "pages": 2,
                "focus": "Findings and implications"
            },
            "references": {
                "pages": 1,
                "focus": "Citations and bibliography"
            }
        }
        
        return outline
    
    def get_field_specific_advice(self):
        """Get advice specific to the academic field"""
        field_advice = {
            "computer science": [
                "Include algorithmic complexity analysis",
                "Provide code examples and implementations",
                "Reference recent conferences (ICML, NeurIPS, etc.)"
            ],
            "linguistics": [
                "Include phonetic/syntactic examples", 
                "Reference corpus analysis",
                "Follow linguistic notation standards"
            ],
            "philosophy": [
                "Engage with primary sources",
                "Address counterarguments",
                "Use formal logic where appropriate"
            ]
        }
        
        return field_advice.get("history, kulturwissenschaften", [
            "Follow standard academic format",
            "Cite recent and seminal works",
            "Maintain clear argumentation"
        ])
