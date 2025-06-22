print("🤖 B3COMPUTER INTERACTIVE ACADEMIC SETUP")
print("=" * 45)
print("I'll ask you about your research and create the modules I need!")
print()

from text.self_improver import QuickSelfImprover
import json
from pathlib import Path

# Initialize B3Computer
improver = QuickSelfImprover()

print("🧠 B3Computer: Hello! I'm going to help you with your 20-page deadline.")
print("First, I need to understand your research so I can enhance myself accordingly.")
print()

# Interactive research gathering
research_data = {}

print("📚 What is your main research topic or subject?")
research_data['main_topic'] = input("Topic: ").strip()

print(f"\n🔍 What specific aspects of '{research_data['main_topic']}' are you focusing on?")
print("(Enter keywords separated by commas)")
keywords_input = input("Keywords: ").strip()
research_data['keywords'] = [k.strip() for k in keywords_input.split(',') if k.strip()]

print(f"\n📁 Where are your existing exposés and documents located?")
print("(Enter directory paths separated by commas, or just press Enter for current directory)")
dirs_input = input("Directories: ").strip()
if dirs_input:
    research_data['directories'] = [d.strip() for d in dirs_input.split(',')]
else:
    research_data['directories'] = ['./']

print(f"\n🎯 What's the main question or thesis you're exploring?")
research_data['main_question'] = input("Research question: ").strip()

print(f"\n📖 What academic field is this for?")
research_data['field'] = input("Field: ").strip()

print(f"\n⏰ Any specific requirements or constraints I should know about?")
research_data['constraints'] = input("Requirements: ").strip()

print("\n🧠 B3Computer: Perfect! Now I'll enhance myself for your specific research...")

# Create specialized research module based on user input
research_module_code = f'''
"""
B3Computer Research Module - Dynamically Generated
Topic: {research_data['main_topic']}
Field: {research_data['field']}
Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

from modules.academic_coordinator import AcademicCoordinator
import json

class SpecializedResearchAssistant:
    def __init__(self):
        self.research_config = {research_data}
        self.coordinator = AcademicCoordinator()
        
    def get_research_info(self):
        return {{
            "topic": "{research_data['main_topic']}",
            "keywords": {research_data['keywords']},
            "main_question": "{research_data['main_question']}",
            "field": "{research_data['field']}",
            "directories": {research_data['directories']},
            "constraints": "{research_data['constraints']}"
        }}
    
    def search_specialized_papers(self):
        """Search for papers specific to user's research"""
        print(f"🔍 Searching for papers on: {research_data['main_topic']}")
        
        # Enhanced search based on user's specific topic
        search_terms = [
            "{research_data['main_topic']}",
            f"{research_data['main_topic']} {research_data['field']}",
            "{research_data['main_question']}"
        ] + {research_data['keywords']}
        
        all_papers = []
        for term in search_terms:
            papers = self.coordinator.search_academic_papers([term])
            all_papers.extend(papers)
        
        return all_papers
    
    def analyze_user_documents(self):
        """Analyze user's specific documents"""
        all_files = []
        for directory in {research_data['directories']}:
            files = self.coordinator.analyze_existing_work(directory)
            all_files.extend(files)
        return all_files
    
    def generate_research_outline(self):
        """Generate outline specific to user's research"""
        outline = {{
            "title": "Research on {research_data['main_topic']}",
            "introduction": {{
                "pages": 2,
                "focus": "Introduce {research_data['main_topic']} and research question"
            }},
            "literature_review": {{
                "pages": 4,
                "focus": "Review existing work on {', '.join(research_data['keywords'][:3])}"
            }},
            "methodology": {{
                "pages": 3,
                "focus": "Approach to studying {research_data['main_topic']}"
            }},
            "main_analysis": {{
                "pages": 8,
                "focus": "Deep dive into {research_data['main_question']}"
            }},
            "conclusion": {{
                "pages": 2,
                "focus": "Findings and implications"
            }},
            "references": {{
                "pages": 1,
                "focus": "Citations and bibliography"
            }}
        }}
        
        return outline
    
    def get_field_specific_advice(self):
        """Get advice specific to the academic field"""
        field_advice = {{
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
        }}
        
        return field_advice.get("{research_data['field'].lower()}", [
            "Follow standard academic format",
            "Cite recent and seminal works",
            "Maintain clear argumentation"
        ])
'''

# Write the specialized module
Path("modules").mkdir(exist_ok=True)
with open("modules/my_research_assistant.py", "w", encoding='utf-8') as f:
    f.write(research_module_code)

print("✅ Created specialized research module!")

# Save research config
with open("my_research_config.json", "w") as f:
    json.dump(research_data, f, indent=2)

print("✅ Saved your research configuration!")

print("\n🚀 B3Computer has enhanced itself for your specific research!")
print(f"Topic: {research_data['main_topic']}")
print(f"Field: {research_data['field']}")
print(f"Keywords: {', '.join(research_data['keywords'])}")

print("\n🎯 Now launching specialized academic mission...")

# Test the new module
try:
    exec("from modules.my_research_assistant import SpecializedResearchAssistant")
    assistant = eval("SpecializedResearchAssistant()")
    
    print("\n📊 Your Research Profile:")
    info = assistant.get_research_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print(f"\n📋 Generating research outline...")
    outline = assistant.generate_research_outline()
    print("Suggested structure:")
    for section, details in outline.items():
        if isinstance(details, dict):
            print(f"  {section}: {details['pages']} pages - {details['focus']}")
    
    print(f"\n💡 Field-specific advice for {research_data['field']}:")
    advice = assistant.get_field_specific_advice()
    for tip in advice:
        print(f"  • {tip}")
    
except Exception as e:
    print(f"⚠️ Module creation error: {e}")

print("\n🎉 B3Computer is now specialized for YOUR research!")
print("🔄 Restart your terminals with the new configuration")