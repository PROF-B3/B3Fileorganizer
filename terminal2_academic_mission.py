print("🎓 B3COMPUTER ACADEMIC RESEARCH MISSION")
print("=" * 45)
print("Terminal 2: Academic Research Coordination")
print("📅 Deadline: Tomorrow Evening")
print("📄 Target: 20 Pages")
print()

from modules.academic_coordinator import AcademicCoordinator
import time
from datetime import datetime

# Initialize Academic Coordinator
coordinator = AcademicCoordinator()

print("🚀 Academic Mission Initiated")
print()

# Phase 1: Analyze Existing Work
print("📁 PHASE 1: Analyzing Existing Documents")
print("-" * 40)
existing_files = coordinator.analyze_existing_work("./")
print(f"✅ Found {len(existing_files)} existing documents")

# Phase 2: Research Keywords
print("\n🔍 PHASE 2: Academic Research")
print("-" * 40)

# You can modify these topics based on your actual research
research_topics = [
    "artificial intelligence research methodology",
    "machine learning academic writing",
    "computational linguistics",
    "natural language processing",
    "academic paper structure"
]

print("🌐 Searching academic databases...")
papers = coordinator.search_academic_papers(research_topics)
print(f"✅ Found {len(papers)} relevant papers")

# Phase 3: Content Planning
print("\n📋 PHASE 3: Content Strategy")
print("-" * 40)
content_plan = coordinator.generate_content_plan()

# Phase 4: Continuous Monitoring
print("\n⏰ PHASE 4: Deadline Monitoring")
print("-" * 40)

while True:
    try:
        status = coordinator.get_project_status()
        
        print(f"\n📊 PROJECT STATUS - {datetime.now().strftime('%H:%M:%S')}")
        print(f"⏰ Hours remaining: {status['hours_remaining']:.1f}")
        print(f"📄 Pages remaining: {status['pages_remaining']}")
        print(f"⚡ Writing pace needed: {status['pages_per_hour_needed']:.1f} pages/hour")
        print(f"🚨 Urgency: {status['urgency']}")
        
        print("\n💡 Current Recommendations:")
        for rec in status['recommendations']:
            print(f"  • {rec}")
        
        print("\n" + "="*50)
        time.sleep(600)  # Update every 10 minutes
        
    except KeyboardInterrupt:
        print("\n🛑 Academic mission monitoring stopped")
        break
    except Exception as e:
        print(f"⚠️ Mission error: {e}")
        time.sleep(60)