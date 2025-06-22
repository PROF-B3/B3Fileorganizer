print("🤖 B3COMPUTER SELF-IMPROVEMENT MONITOR")
print("=" * 45)
print("Terminal 1: Active Self-Enhancement")
print()

from text.self_improver import QuickSelfImprover
import time
from datetime import datetime

# Initialize B3Computer self-improvement
improver = QuickSelfImprover()

print("🧠 B3Computer Self-Improvement Active")
print("⏰ Monitoring for enhancement opportunities...")
print()

cycle_count = 0
while True:
    try:
        cycle_count += 1
        print(f"\n🔄 Self-Improvement Cycle #{cycle_count}")
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
        
        # Run improvement cycle focused on academic capabilities
        results = improver.run_improvement_cycle()
        
        print(f"📊 Cycle Results:")
        print(f"  Files analyzed: {results.get('files_analyzed', 0)}")
        print(f"  Improvements: {results.get('improvements_applied', 0)}")
        print(f"  Errors: {len(results.get('errors', []))}")
        
        if results.get('improvements_applied', 0) > 0:
            print("✨ B3Computer enhanced itself!")
        
        print("💤 Waiting 5 minutes for next cycle...")
        time.sleep(300)  # 5 minutes between cycles
        
    except KeyboardInterrupt:
        print("\n🛑 Self-improvement monitoring stopped")
        break
    except Exception as e:
        print(f"⚠️ Cycle error: {e}")
        time.sleep(60)  # Wait 1 minute on error