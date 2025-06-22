print("📊 B3COMPUTER REAL-TIME STATUS MONITOR")
print("=" * 45)
print("Terminal 3: System Status & Performance")
print()

import time
import psutil
from datetime import datetime
from pathlib import Path

def get_system_status():
    """Get comprehensive system status"""
    # System resources
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    # B3Computer status
    modules_active = len(list(Path("modules").glob("*.py"))) if Path("modules").exists() else 0
    config_files = len(list(Path("config").glob("*.json"))) if Path("config").exists() else 0
    
    # Academic progress indicators
    academic_files = len(list(Path(".").glob("**/*.pdf"))) + len(list(Path(".").glob("**/*.docx")))
    
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "cpu_percent": cpu,
        "memory_percent": memory.percent,
        "memory_available_gb": memory.available / (1024**3),
        "modules_active": modules_active,
        "config_files": config_files,
        "academic_files": academic_files
    }

print("🟢 B3Computer Status Monitor Active")
print("⏰ Updating every 30 seconds...")
print()

while True:
    try:
        status = get_system_status()
        
        # Clear and redraw status
        print(f"\n🤖 B3COMPUTER STATUS - {status['timestamp']}")
        print("=" * 45)
        
        print(f"🖥️  SYSTEM RESOURCES:")
        print(f"   CPU Usage: {status['cpu_percent']:.1f}%")
        print(f"   Memory: {status['memory_percent']:.1f}% used")
        print(f"   Available: {status['memory_available_gb']:.1f} GB")
        
        print(f"\n🧠 B3COMPUTER STATUS:")
        print(f"   Active Modules: {status['modules_active']}")
        print(f"   Config Files: {status['config_files']}")
        print(f"   Academic Files: {status['academic_files']}")
        
        # Calculate urgency based on time
        from modules.deadline_manager import DeadlineManager
        deadline_mgr = DeadlineManager()
        deadline_status = deadline_mgr.get_status()
        
        print(f"\n📅 DEADLINE STATUS:")
        print(f"   Hours Remaining: {deadline_status['hours_remaining']:.1f}")
        print(f"   Urgency Level: {deadline_status['urgency']}")
        print(f"   Completion Rate: {deadline_status['completion_rate']:.1f}%")
        
        # Performance indicators
        if status['cpu_percent'] > 80:
            print("⚠️  HIGH CPU USAGE")
        if status['memory_percent'] > 85:
            print("⚠️  HIGH MEMORY USAGE")
        if deadline_status['urgency'] == 'CRITICAL':
            print("🚨 CRITICAL DEADLINE ALERT!")
        
        print("\n⏰ Next update in 30 seconds...")
        time.sleep(30)
        
    except KeyboardInterrupt:
        print("\n🛑 Status monitoring stopped")
        break
    except Exception as e:
        print(f"⚠️ Status error: {e}")
        time.sleep(30)
        