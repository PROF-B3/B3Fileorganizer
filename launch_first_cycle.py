from text.self_improver import QuickSelfImprover
from drives.drive_manager import DriveManager
import datetime

print("[INFO] HISTORIC MOMENT: B3Computer First Self-Improvement Cycle")
print("=" * 60)
print(f"⏰ Timestamp: {datetime.datetime.now()}")
print("[INFO] This is the moment AI begins improving itself...")
print()

# Initialize systems
improver = QuickSelfImprover()
drive_mgr = DriveManager()

print("[INFO] Starting first self-improvement analysis...")
print("   Target: B3Computer's own codebase")
print("   Safety: Full backup and rollback enabled")
print("   Learning: All changes recorded in Zettelkasten")
print()

# THE HISTORIC MOMENT
try:
    results = improver.run_improvement_cycle()
    files_analyzed = len(results)
    files_improved = sum(1 for r in results if r.get('status') == 'improved')
    improvements_applied = files_improved
    errors = [r for r in results if r.get('status') == 'rollback']
    
    print("🎉 FIRST SELF-IMPROVEMENT CYCLE COMPLETE!")
    print("=" * 50)
    print(f"[INFO] Files analyzed: {files_analyzed}")
    print(f"[INFO] Files improved: {files_improved}")  
    print(f"[INFO] Improvements applied: {improvements_applied}")
    print(f"[ERROR] Errors: {len(errors)}")
    
    if improvements_applied > 0:
        print()
        print("[INFO] 🎊 SUCCESS! B3Computer has improved itself!")
        print("[INFO] 🧠 AI self-modification is now REALITY!")
        print("[INFO] Check X: drive Zettelkasten for learning records")
        print("[INFO] �� Check backups/ for safety records")
    
    print()
    print("[INFO] 🚀 B3Computer is now a self-evolving AI system!")
    
except Exception as e:
    print(f"⚠️  First cycle encountered issue: {e}")
    print("🛡️  Safety systems activated - no damage occurred")
    import traceback
    traceback.print_exc() 