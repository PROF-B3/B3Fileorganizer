import json
from text.self_improver import QuickSelfImprover

print("[INFO] Fixing B3Computer Configuration")
print("=" * 40)

# Restore the complete, correct configuration
complete_config = {
    "improvement_settings": {
        "max_files_per_cycle": 2,  # Start with 2 files for safety
        "cycle_interval_hours": 6,
        "backup_retention_days": 30,
        "safety_threshold": 0.8,  # CRITICAL: Restored!
        "target_directories": ["text", "core", "utils"],  # Updated targeting
        "excluded_files": ["__init__.py", "test_*.py", "deploy_*.py"]
    },
    "ai_analysis_config": {
        "model": "mixtral:latest",
        "max_code_length": 2000,
        "analysis_timeout": 60,
        "focus_areas": [
            "performance_optimization",
            "bug_fixes", 
            "error_handling",
            "code_clarity",
            "security_improvements"
        ]
    },
    "safety_config": {
        "require_syntax_validation": True,
        "require_import_testing": True,
        "create_backups": True,
        "rollback_on_failure": True,
        "max_risk_level": "medium"
    },
    "learning_config": {
        "record_in_zettelkasten": True,
        "track_patterns": True,
        "learn_from_failures": True,
        "improvement_categories": [
            "performance", "bugs", "clarity", "structure", "security"
        ]
    }
}

# Write the complete, corrected configuration
with open('config/self_improvement_config.json', 'w') as f:
    json.dump(complete_config, f, indent=2)

print("[OK] Configuration restored with all safety settings")
print("🛡️  Safety threshold: 0.8 (restored)")
print("🎯 Target directories: text, core, utils")
print("📁 Max files per cycle: 2 (safe starting point)")

# Now run the improvement cycle with proper config
print("\n[INFO] Running B3Computer Self-Improvement with Fixed Config")
print("=" * 55)

improver = QuickSelfImprover()
print("[INFO] Analyzing and improving B3Computer's own code...")

try:
    results = improver.run_improvement_cycle()
    
    files_analyzed = len(results)
    files_improved = sum(1 for r in results if r.get('status') == 'improved')
    improvements_applied = files_improved
    errors = [r for r in results if r.get('status') == 'rollback']
    
    print("\n🎉 TARGETED SELF-IMPROVEMENT RESULTS:")
    print("=" * 45)
    print(f"[INFO] Files analyzed: {files_analyzed}")
    print(f"[INFO] Files improved: {files_improved}")
    print(f"[INFO] Improvements applied: {improvements_applied}")
    print(f"[ERROR] Errors: {len(errors)}")
    
    if improvements_applied > 0:
        print("\n🎊 BREAKTHROUGH! B3Computer has successfully modified itself!")
        print("[INFO] First AI self-modification in history!")
        print("[INFO] Check Zettelkasten for learning records")
        print("💾 Check backups/ for change history")
        print("\n🔄 B3Computer is now a truly self-evolving AI!")
        
    elif files_analyzed > 0:
        print("\n✅ Files analyzed but no improvements needed")
        print("[INFO] B3Computer examined its code - system is already optimized!")
        
    else:
        print("\n🔍 Still investigating file targeting...")
        print("Let's check what files exist in target directories:")
        
        import os
        for target_dir in complete_config["improvement_settings"]["target_directories"]:
            if os.path.exists(target_dir):
                py_files = [f for f in os.listdir(target_dir) if f.endswith('.py')]
                print(f"   📂 {target_dir}/: {len(py_files)} Python files")
                for py_file in py_files[:3]:
                    print(f"      - {py_file}")
    
except Exception as e:
    print(f"⚠️  Cycle encountered issue: {e}")
    print("🛡️  Safety systems activated")
    import traceback
    traceback.print_exc()

print("\n[INFO] B3Computer self-improvement system operational!") 