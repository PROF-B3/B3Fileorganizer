import json
from text.self_improver import QuickSelfImprover

print("[B3Computer] Targeted Improvement Cycle")
print("=" * 45)

# Update config for better targeting
config_updates = {
    "improvement_settings": {
        "max_files_per_cycle": 2,
        "target_directories": ["text", "core", "utils", "B:/b3FileOrganizer/text", "B:/b3FileOrganizer/core"],
        "excluded_files": ["__init__.py", "test_*.py", "deploy_*.py"]
    }
}

# Load and update config
with open('config/self_improvement_config.json', 'r') as f:
    config = json.load(f)

config.update(config_updates)

with open('config/self_improvement_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print("[OK] Configuration updated for better targeting")

# Run targeted improvement cycle
improver = QuickSelfImprover()
print("[INFO] Running targeted self-improvement cycle...")

results = improver.run_improvement_cycle()

files_analyzed = len(results)
files_improved = sum(1 for r in results if r.get('status') == 'improved')
improvements_applied = files_improved

print("\n[TARGETED CYCLE RESULTS]:")
print(f"   Files analyzed: {files_analyzed}")
print(f"   Files improved: {files_improved}")
print(f"   Improvements applied: {improvements_applied}")

if improvements_applied > 0:
    print("\n🎊 SUCCESS! B3Computer has modified itself!")
    print("[INFO] First AI self-modification achieved!")
elif files_analyzed > 0:
    print("\n[OK] Analysis complete - files examined but no changes needed")
else:
    print("\n[INFO] Still no files found - need to adjust targeting further") 