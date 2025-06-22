import json
from text.self_improver import QuickSelfImprover
from pathlib import Path

print("🔍 B3Computer Targeting Analysis")
print("=" * 40)

# Check current configuration
with open('config/self_improvement_config.json', 'r') as f:
    config = json.load(f)

print("📋 Current Settings:")
print(f"   Target directories: {config['improvement_settings']['target_directories']}")
print(f"   Max files per cycle: {config['improvement_settings']['max_files_per_cycle']}")
print(f"   Excluded files: {config['improvement_settings']['excluded_files']}")

# Check what files exist in target directories
target_dirs = config['improvement_settings']['target_directories']
for target_dir in target_dirs:
    target_path = Path(target_dir)
    if target_path.exists():
        py_files = list(target_path.glob("*.py"))
        print(f"   📂 {target_dir}/: {len(py_files)} Python files found")
        for py_file in py_files[:3]:  # Show first 3
            print(f"      - {py_file.name}")
    else:
        print(f"   ❌ {target_dir}/ does not exist")

# Check B: drive for Python files to improve
b_drive = Path("B:/b3FileOrganizer")
if b_drive.exists():
    b_py_files = list(b_drive.glob("**/*.py"))
    print(f"   📂 B:/b3FileOrganizer: {len(b_py_files)} Python files found")

print("\n🔧 Suggested Configuration Update:")
print("Update target_directories to include actual code locations:")
suggested_config = {
    "target_directories": ["text", "core", "utils", "B:/b3FileOrganizer/text", "B:/b3FileOrganizer/core"],
    "max_files_per_cycle": 2,  # Start small
    "excluded_files": ["__init__.py", "test_*.py"]
}
print(json.dumps(suggested_config, indent=2)) 