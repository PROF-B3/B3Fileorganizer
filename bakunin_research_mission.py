print("🎓 B3COMPUTER SPECIALIZED MISSION: BAKUNIN & NARRATIVE NATIONS")
print("=" * 65)
print("🇪🇺 Topic: Narrative preconditions of European nations")
print("⚡ Focus: Bakunin's biography as case study")
print("📚 Field: History, Kulturwissenschaften")
print()

from modules.my_research_assistant import SpecializedResearchAssistant
from modules.academic_coordinator import AcademicCoordinator
import time
from datetime import datetime

# Initialize your specialized research assistant
assistant = SpecializedResearchAssistant()
coordinator = AcademicCoordinator()

print("🔍 Phase 1: Analyzing YOUR existing documents on B: drive...")
print("-" * 60)

# Scan B: drive for your exposés and papers
b_drive_files = coordinator.analyze_existing_work("B:")
print(f"✅ Found {len(b_drive_files)} documents on B: drive")

# Look specifically for your mentioned documents
history_manifesto_files = [f for f in b_drive_files if 'history' in str(f).lower() or 'manifesto' in str(f).lower()]
dissertation_files = [f for f in b_drive_files if 'dissertation' in str(f).lower() or 'expose' in str(f).lower()]

print(f"📄 History Manifesto related: {len(history_manifesto_files)} files")
print(f"📄 Dissertation exposés: {len(dissertation_files)} files")

print("\n🌐 Phase 2: Searching for academic papers on YOUR research...")
print("-" * 60)

# Search for papers specific to your research
specialized_search_terms = [
    "narrative construction of nations",
    "Bakunin biography anarchism",
    "nationalism as narrative historiography", 
    "cultural studies nationhood",
    "philosophy of history narrative theory",
    "European nationalism 19th century",
    "anarchist critique of nationalism",
    "Bakunin political philosophy",
    "nation building narrative",
    "historiography narrative turn"
]

all_papers = []
for term in specialized_search_terms:
    print(f"  🔍 Searching: {term}")
    papers = coordinator.search_academic_papers([term])
    all_papers.extend(papers)
    print(f"    Found: {len(papers)} papers")

print(f"\n✅ Total papers found: {len(all_papers)}")

print("\n📋 Phase 3: YOUR 20-Page Structure for Bakunin Research...")
print("-" * 60)

bakunin_outline = {
    "Introduction (2 pages)": {
        "focus": "Nations as narrative constructs thesis + Bakunin case study introduction",
        "content": "- Thesis: narrative > material conditions\n- Bakunin as exemplar of anti-nationalist narrative\n- Research question and methodology"
    },
    "Chapter 1 Summary (4 pages)": {
        "focus": "From History Manifesto - narrative turn in historiography", 
        "content": "- Summarize first chapter of History Manifesto\n- Connect to narrative theory\n- Opening paragraph analysis"
    },
    "Chapter 2 Summary (4 pages)": {
        "focus": "From Dissertation Exposé - Bakunin's anti-nationalist narrative",
        "content": "- Summarize second chapter of dissertation\n- Bakunin's critique of nation-building\n- Opening paragraph analysis"
    },
    "Synthesis Analysis (6 pages)": {
        "focus": "How Bakunin's narrative challenges European nation-building",
        "content": "- Bakunin's alternative to nationalist narratives\n- Case studies from his biography\n- Impact on European political thought"
    },
    "Theoretical Framework (3 pages)": {
        "focus": "Narrative theory applied to historiography",
        "content": "- Why narrative matters more than material conditions\n- Kulturwissenschaften methodology\n- Literature review integration"
    },
    "Conclusion (1 page)": {
        "focus": "Implications for understanding European nationalism",
        "content": "- Summary of findings\n- Future research directions"
    }
}

print("📖 YOUR SPECIALIZED 20-PAGE STRUCTURE:")
for section, details in bakunin_outline.items():
    print(f"\n{section}:")
    print(f"  Focus: {details['focus']}")
    print(f"  Content: {details['content']}")

print("\n⏰ Phase 4: Deadline Management for YOUR Research...")
print("-" * 60)

# Monitor your specific deadline
while True:
    try:
        status = coordinator.get_project_status()
        
        print(f"\n🇪🇺 BAKUNIN RESEARCH STATUS - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)
        print(f"⏰ Hours remaining: {status['hours_remaining']:.1f}")
        print(f"📄 Pages to write: {status['pages_remaining']}")
        print(f"✍️  Writing pace needed: {status['pages_per_hour_needed']:.1f} pages/hour")
        print(f"🚨 Urgency: {status['urgency']}")
        
        print(f"\n📚 YOUR RESOURCES:")
        print(f"  • Documents on B: drive: {len(b_drive_files)}")
        print(f"  • Academic papers found: {len(all_papers)}")
        print(f"  • History Manifesto files: {len(history_manifesto_files)}")
        print(f"  • Dissertation files: {len(dissertation_files)}")
        
        print(f"\n💡 BAKUNIN RESEARCH RECOMMENDATIONS:")
        print("  • Start with Chapter 1 summary from History Manifesto")
        print("  • Extract key quotes about narrative vs. material conditions")
        print("  • Focus on Bakunin's biographical moments that challenge nationalism")
        print("  • Use Kulturwissenschaften methodology throughout")
        print("  • Emphasize the narrative construction thesis")
        
        if status['urgency'] == 'CRITICAL':
            print(f"\n🚨 CRITICAL: Focus on core Bakunin narrative!")
            print("  • Skip extensive literature review")
            print("  • Use direct quotes from your exposés")
            print("  • Emphasize biographical narrative moments")
        
        print("\n" + "="*60)
        time.sleep(300)  # Update every 5 minutes
        
    except KeyboardInterrupt:
        print("\n✅ Bakunin research mission monitoring stopped")
        break
    except Exception as e:
        print(f"⚠️ Mission error: {e}")
        time.sleep(60)