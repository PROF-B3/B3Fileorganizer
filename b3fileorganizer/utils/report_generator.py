"""
Report Generator for B3FileOrganizer
Generates comprehensive reports in multiple formats (JSON, HTML, PDF).
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sqlite3

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generates comprehensive system reports."""
    
    def __init__(self, db_path: str = "databases/organization_history.db"):
        self.db_path = Path(db_path)
        self.logger = logging.getLogger(__name__)
    
    def generate_system_report(self, include_conversations: bool = True) -> Dict[str, Any]:
        """Generate comprehensive system report."""
        try:
            report = {
                "generated_at": datetime.now().isoformat(),
                "system_info": self._get_system_info(),
                "ai_models": self._get_ai_model_status(),
                "organization_stats": self._get_organization_stats(),
                "resource_usage": self._get_resource_usage(),
                "recent_activity": self._get_recent_activity()
            }
            
            if include_conversations:
                report["conversations"] = self._get_conversation_summary()
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating system report: {e}")
            return {"error": str(e)}
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get basic system information."""
        import psutil
        
        return {
            "cpu_count": psutil.cpu_count(),
            "memory_total_gb": psutil.virtual_memory().total / (1024**3),
            "disk_total_gb": psutil.disk_usage('/').total / (1024**3),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }
    
    def _get_ai_model_status(self) -> Dict[str, Any]:
        """Get AI model status."""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return {
                    "ollama_accessible": True,
                    "models_available": len(models),
                    "model_list": [model.get("name", "") for model in models]
                }
            else:
                return {"ollama_accessible": False, "error": f"Status {response.status_code}"}
        except Exception as e:
            return {"ollama_accessible": False, "error": str(e)}
    
    def _get_organization_stats(self) -> Dict[str, Any]:
        """Get organization statistics from database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total organizations
                cursor.execute("SELECT COUNT(*) FROM organization_history")
                total_organizations = cursor.fetchone()[0]
                
                # Recent organizations (last 24 hours)
                cursor.execute("""
                    SELECT COUNT(*) FROM organization_history 
                    WHERE timestamp > datetime('now', '-1 day')
                """)
                recent_organizations = cursor.fetchone()[0]
                
                # Organizations by category
                cursor.execute("""
                    SELECT category, COUNT(*) 
                    FROM organization_history 
                    GROUP BY category
                """)
                by_category = dict(cursor.fetchall())
                
                return {
                    "total_organizations": total_organizations,
                    "recent_organizations": recent_organizations,
                    "by_category": by_category
                }
                
        except Exception as e:
            self.logger.error(f"Error getting organization stats: {e}")
            return {"error": str(e)}
    
    def _get_resource_usage(self) -> Dict[str, Any]:
        """Get current resource usage."""
        import psutil
        
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": memory.percent,
            "memory_used_gb": memory.used / (1024**3),
            "memory_available_gb": memory.available / (1024**3),
            "disk_percent": disk.percent,
            "disk_used_gb": disk.used / (1024**3),
            "disk_free_gb": disk.free / (1024**3)
        }
    
    def _get_recent_activity(self) -> List[Dict[str, Any]]:
        """Get recent organization activity."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM organization_history 
                    ORDER BY timestamp DESC LIMIT 10
                """)
                activities = cursor.fetchall()
                
                return [
                    {
                        "timestamp": activity[1],
                        "original_name": activity[2],
                        "new_name": activity[3],
                        "category": activity[4],
                        "operation": activity[5]
                    }
                    for activity in activities
                ]
                
        except Exception as e:
            self.logger.error(f"Error getting recent activity: {e}")
            return []
    
    def _get_conversation_summary(self) -> Dict[str, Any]:
        """Get conversation summary."""
        try:
            from .conversation_logger import ConversationLogger
            logger = ConversationLogger()
            stats = logger.get_statistics()
            return stats
        except Exception as e:
            return {"error": str(e)}
    
    def save_report(self, report: Dict[str, Any], format: str = "json", 
                   filename: Optional[str] = None) -> Optional[str]:
        """Save report to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not filename:
            filename = f"reports/system_report_{timestamp}"
        
        try:
            if format == "json":
                filename = f"{filename}.json"
                Path(filename).parent.mkdir(parents=True, exist_ok=True)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
            
            elif format == "html":
                filename = f"{filename}.html"
                Path(filename).parent.mkdir(parents=True, exist_ok=True)
                
                html_content = self._generate_html_report(report)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            
            elif format == "txt":
                filename = f"{filename}.txt"
                Path(filename).parent.mkdir(parents=True, exist_ok=True)
                
                txt_content = self._generate_text_report(report)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(txt_content)
            
            self.logger.info(f"Report saved to {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")
            return None
    
    def _generate_html_report(self, report: Dict[str, Any]) -> str:
        """Generate HTML report."""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>B3FileOrganizer System Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .header {{ background-color: #f5f5f5; padding: 10px; margin-bottom: 20px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background-color: #e8f4f8; border-radius: 3px; }}
        .error {{ color: red; }}
        .success {{ color: green; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>B3FileOrganizer System Report</h1>
        <p>Generated: {report.get('generated_at', 'Unknown')}</p>
    </div>
    
    <div class="section">
        <h2>System Information</h2>
        <div class="metric">CPU Cores: {report.get('system_info', {}).get('cpu_count', 'N/A')}</div>
        <div class="metric">Memory: {report.get('system_info', {}).get('memory_total_gb', 0):.1f} GB</div>
        <div class="metric">Disk: {report.get('system_info', {}).get('disk_total_gb', 0):.1f} GB</div>
    </div>
    
    <div class="section">
        <h2>AI Models</h2>
        <p>Ollama Accessible: <span class="{'success' if report.get('ai_models', {}).get('ollama_accessible') else 'error'}">
            {report.get('ai_models', {}).get('ollama_accessible', False)}
        </span></p>
        <p>Models Available: {report.get('ai_models', {}).get('models_available', 0)}</p>
        <ul>
            {''.join(f'<li>{model}</li>' for model in report.get('ai_models', {}).get('model_list', []))}
        </ul>
    </div>
    
    <div class="section">
        <h2>Organization Statistics</h2>
        <div class="metric">Total Organizations: {report.get('organization_stats', {}).get('total_organizations', 0)}</div>
        <div class="metric">Recent (24h): {report.get('organization_stats', {}).get('recent_organizations', 0)}</div>
    </div>
    
    <div class="section">
        <h2>Resource Usage</h2>
        <div class="metric">CPU: {report.get('resource_usage', {}).get('cpu_percent', 0):.1f}%</div>
        <div class="metric">Memory: {report.get('resource_usage', {}).get('memory_percent', 0):.1f}%</div>
        <div class="metric">Disk: {report.get('resource_usage', {}).get('disk_percent', 0):.1f}%</div>
    </div>
    
    <div class="section">
        <h2>Recent Activity</h2>
        <table>
            <tr>
                <th>Timestamp</th>
                <th>Original Name</th>
                <th>New Name</th>
                <th>Category</th>
                <th>Operation</th>
            </tr>
            {''.join(f'''
            <tr>
                <td>{activity.get('timestamp', '')}</td>
                <td>{activity.get('original_name', '')}</td>
                <td>{activity.get('new_name', '')}</td>
                <td>{activity.get('category', '')}</td>
                <td>{activity.get('operation', '')}</td>
            </tr>
            ''' for activity in report.get('recent_activity', []))}
        </table>
    </div>
</body>
</html>
        """
        return html
    
    def _generate_text_report(self, report: Dict[str, Any]) -> str:
        """Generate text report."""
        text = f"""
B3FileOrganizer System Report
Generated: {report.get('generated_at', 'Unknown')}
{'='*60}

SYSTEM INFORMATION:
- CPU Cores: {report.get('system_info', {}).get('cpu_count', 'N/A')}
- Memory: {report.get('system_info', {}).get('memory_total_gb', 0):.1f} GB
- Disk: {report.get('system_info', {}).get('disk_total_gb', 0):.1f} GB

AI MODELS:
- Ollama Accessible: {report.get('ai_models', {}).get('ollama_accessible', False)}
- Models Available: {report.get('ai_models', {}).get('models_available', 0)}
- Model List: {', '.join(report.get('ai_models', {}).get('model_list', []))}

ORGANIZATION STATISTICS:
- Total Organizations: {report.get('organization_stats', {}).get('total_organizations', 0)}
- Recent (24h): {report.get('organization_stats', {}).get('recent_organizations', 0)}

RESOURCE USAGE:
- CPU: {report.get('resource_usage', {}).get('cpu_percent', 0):.1f}%
- Memory: {report.get('resource_usage', {}).get('memory_percent', 0):.1f}%
- Disk: {report.get('resource_usage', {}).get('disk_percent', 0):.1f}%

RECENT ACTIVITY:
"""
        
        for activity in report.get('recent_activity', []):
            text += f"- {activity.get('timestamp', '')}: {activity.get('original_name', '')} -> {activity.get('new_name', '')} ({activity.get('category', '')})\n"
        
        return text 