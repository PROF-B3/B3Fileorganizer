#!/usr/bin/env python3
"""
B3Computer Self-Improvement Engine
Main engine for recursive self-improvement of the B3FileOrganizer codebase.
"""
import os
import sys
import time
import json
import shutil
import logging
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from colorama import Fore, Style
from b3fileorganizer.core.ai_manager import AIManager
from b3fileorganizer.core.zettelkasten import ZettelkastenManager
from b3fileorganizer.core.database_manager import DatabaseManager
from b3fileorganizer.utils.file_operations import FileOperations
from b3fileorganizer.utils.status_monitor import StatusMonitor

CONFIG_PATH = "config/self_improvement_config.json"
WORKFLOW_PATH = "config/improvement_workflow.json"
SAFETY_PATH = "config/safety_rules.json"
LEARNING_PATH = "config/learning_patterns.json"
AGENT_PATH = "config/agent_capabilities.json"

class QuickSelfImprover:
    def __init__(self):
        self.logger = logging.getLogger("B3Computer.SelfImprover")
        self.config = self._load_json(CONFIG_PATH)
        self.workflow = self._load_json(WORKFLOW_PATH)
        self.safety = self._load_json(SAFETY_PATH)
        self.learning = self._load_json(LEARNING_PATH)
        self.agent = self._load_json(AGENT_PATH)
        self.ai_manager = AIManager()
        self.zettelkasten = ZettelkastenManager()
        self.db_manager = DatabaseManager()
        self.file_ops = FileOperations()
        self.status_monitor = StatusMonitor()
        self.backup_dir = Path("backups")
        self.log_dir = Path("logs")
        self.backup_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
        self.target_dirs = self.config["improvement_settings"]["target_directories"]
        self.excluded_files = self.config["improvement_settings"]["excluded_files"]
        self.max_files = self.config["improvement_settings"]["max_files_per_cycle"]
        self.safety_threshold = self.config["improvement_settings"]["safety_threshold"]
        
        # Module creation settings
        self.modules_dir = Path("b3fileorganizer/core")
        self.cli_file = Path("b3fileorganizer/text/run_organize.py")
        self.dynamic_modules_file = Path("b3fileorganizer/core/dynamic_modules.json")

    def _load_json(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file {path} not found, using defaults")
            return {}

    def create_new_module(self, module_name: str, purpose: str, requirements: List[str]) -> Dict[str, Any]:
        """Create a new module based on requirements."""
        try:
            # Validate module name
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', module_name):
                raise ValueError(f"Invalid module name: {module_name}")
            
            # Create module file
            module_path = self.modules_dir / f"{module_name}.py"
            if module_path.exists():
                raise FileExistsError(f"Module {module_name} already exists")
            
            # Generate module code
            module_code = self._generate_module_code(module_name, purpose, requirements)
            used_fallback = False
            if not module_code or "AI service is currently unavailable" in module_code or "Auto-generated module template" in module_code:
                # If AI failed, use fallback/template
                from b3fileorganizer.core.ai_manager import AIManager
                module_code = AIManager()._generate_fallback_module_code("")
                used_fallback = True
            
            # Validate and create
            if self._validate_code(module_code):
                with open(module_path, 'w', encoding='utf-8') as f:
                    f.write(module_code)
                
                # Register module
                self._register_dynamic_module(module_name, purpose, requirements)
                
                # Create Zettelkasten card
                self._record_module_creation(module_name, purpose, requirements, module_code)
                
                msg = f"Created new module: {module_name}"
                if used_fallback:
                    msg += " (using fallback/template code due to AI unavailability)"
                self.logger.info(msg)
                return {
                    "success": True,
                    "module_name": module_name,
                    "file_path": str(module_path),
                    "purpose": purpose,
                    "used_fallback": used_fallback
                }
            else:
                raise ValueError("Generated module code failed validation")
                
        except Exception as e:
            self.logger.error(f"Failed to create module {module_name}: {e}")
            return {"success": False, "error": str(e)}

    def _generate_module_code(self, module_name: str, purpose: str, requirements: List[str]) -> str:
        """Generate Python code for a new module."""
        prompt = f"""
        Create a Python module named '{module_name}' with the following specifications:
        
        Purpose: {purpose}
        Requirements: {', '.join(requirements)}
        
        The module should:
        1. Follow B3FileOrganizer coding standards
        2. Include proper docstrings and type hints
        3. Have error handling and logging
        4. Be compatible with the existing system architecture
        5. Include a main class or function that can be called from the CLI
        
        Generate complete, working Python code for this module.
        """
        
        return self.ai_manager.generate_code(prompt)

    def integrate_module_into_cli(self, module_name: str, menu_option: str, menu_number: Optional[int] = None) -> Dict[str, Any]:
        """Add new module to the CLI menu system."""
        try:
            if not self.cli_file.exists():
                raise FileNotFoundError("CLI file not found")
            
            # Backup CLI file
            backup_path = self._backup_file(self.cli_file)
            
            # Read current CLI content
            with open(self.cli_file, 'r', encoding='utf-8') as f:
                cli_content = f.read()
            
            # Generate integration code
            integration_code = self._generate_cli_integration(module_name, menu_option, menu_number)
            
            # Apply integration
            updated_content = self._apply_cli_integration(cli_content, integration_code, menu_number, menu_option)
            
            # Validate and apply
            if self._validate_code(updated_content):
                with open(self.cli_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                self.logger.info(f"Integrated module {module_name} into CLI")
                return {"success": True, "module_name": module_name}
            else:
                # Rollback
                self._rollback(self.cli_file, backup_path)
                raise ValueError("CLI integration failed validation")
                
        except Exception as e:
            self.logger.error(f"Failed to integrate module {module_name}: {e}")
            return {"success": False, "error": str(e)}

    def _generate_cli_integration(self, module_name: str, menu_option: str, menu_number: Optional[int]) -> str:
        """Generate code to integrate module into CLI menu."""
        if menu_number is None:
            # Find next available menu number
            menu_number = self._find_next_menu_number()
        
        integration_code = f"""
    def option_{menu_number}_{module_name.lower()}(self):
        \"\"\"Option {menu_number}: {menu_option}\"\"\"
        print(f"\\n{{Fore.CYAN}}{{Style.BRIGHT}}{menu_option}{{Style.RESET_ALL}}")
        print("="*60)
        
        try:
            from b3fileorganizer.core.{module_name} import {module_name.title()}Manager
            {module_name}_manager = {module_name.title()}Manager()
            
            # Add your module-specific logic here
            print(f"Module {module_name} loaded successfully")
            
        except Exception as e:
            print(f"{{Fore.RED}}Error loading {module_name} module: {{e}}{{Style.RESET_ALL}}")
        
        input("\\nDrücke Enter zum Fortfahren...")
"""
        return integration_code

    def _find_next_menu_number(self) -> int:
        """Find the next available menu number in the CLI."""
        try:
            with open(self.cli_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find existing option numbers
            option_pattern = r'def option_(\d+)_'
            existing_numbers = [int(n) for n in re.findall(option_pattern, content)]
            
            if existing_numbers:
                return max(existing_numbers) + 1
            else:
                return 8  # Default if no existing options found
                
        except Exception:
            return 8

    def _apply_cli_integration(self, cli_content: str, integration_code: str, menu_number: Optional[int], menu_option: str) -> str:
        """Apply integration code to CLI content."""
        if menu_number is None:
            menu_number = self._find_next_menu_number()
            
        # Find the display_menu method
        menu_pattern = r'(def display_menu\(self\):.*?)(?=def|\Z)'
        match = re.search(menu_pattern, cli_content, re.DOTALL)
        
        if not match:
            raise ValueError("Could not find display_menu method")
        
        menu_method = match.group(1)
        
        # Add menu option
        menu_line = f'        print(f"{menu_number}. {menu_option}")'
        updated_menu = menu_method.replace(
            '        print(f"0. 🚪 Exit")',
            f'        print(f"{menu_number}. {menu_option}")\n        print(f"0. 🚪 Exit")'
        )
        
        # Add method definition before the run method
        run_pattern = r'(def run\(self\):.*?)(?=def|\Z)'
        run_match = re.search(run_pattern, cli_content, re.DOTALL)
        
        if not run_match:
            raise ValueError("Could not find run method")
        
        # Insert the new method before run method
        updated_content = cli_content.replace(
            run_match.group(1),
            integration_code + "\n" + run_match.group(1)
        )
        
        # Update the menu display
        updated_content = updated_content.replace(menu_method, updated_menu)
        
        return updated_content

    def _register_dynamic_module(self, module_name: str, purpose: str, requirements: List[str]):
        """Register a new dynamic module in the registry."""
        try:
            if self.dynamic_modules_file.exists():
                with open(self.dynamic_modules_file, 'r', encoding='utf-8') as f:
                    modules = json.load(f)
            else:
                modules = {}
            
            modules[module_name] = {
                "purpose": purpose,
                "requirements": requirements,
                "created": datetime.now().isoformat(),
                "file_path": str(self.modules_dir / f"{module_name}.py"),
                "cli_integrated": False
            }
            
            with open(self.dynamic_modules_file, 'w', encoding='utf-8') as f:
                json.dump(modules, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Failed to register module {module_name}: {e}")

    def _record_module_creation(self, module_name: str, purpose: str, requirements: List[str], code: str):
        """Record module creation in Zettelkasten."""
        try:
            content = f"""
Module: {module_name}
Purpose: {purpose}
Requirements: {', '.join(requirements)}
Created: {datetime.now().isoformat()}

Code Preview:
```python
{code[:1000]}...
```

This module was automatically generated by the self-improvement system.
"""
            
            self.zettelkasten.create_card(
                content=content,
                title=f"Module Creation: {module_name}",
                category="self_improvement",
                tags=["module-creation", "ai-generated", module_name]
            )
            
        except Exception as e:
            self.logger.error(f"Failed to record module creation: {e}")

    def create_research_assistant_module(self) -> Dict[str, Any]:
        """Create a specialized research assistant module."""
        requirements = [
            "Long-form content generation with chunking",
            "PDF processing for research papers",
            "Citation management and bibliography generation",
            "Project management with deadlines",
            "Integration with existing Zettelkasten",
            "Outline generation and chapter structuring"
        ]
        
        result = self.create_new_module("research_assistant", "Academic research and writing assistant", requirements)
        
        if result["success"]:
            # Integrate into CLI
            cli_result = self.integrate_module_into_cli("research_assistant", "📚 Research Assistant & Academic Writing")
            if cli_result["success"]:
                result["cli_integrated"] = True
        
        return result

    def list_dynamic_modules(self) -> Dict[str, Any]:
        """List all dynamically created modules."""
        try:
            if self.dynamic_modules_file.exists():
                with open(self.dynamic_modules_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"Failed to list dynamic modules: {e}")
            return {}

    def run_improvement_cycle(self):
        """Run a full improvement cycle."""
        results = []
        files = self._discover_files()
        for file_path in files[:self.max_files]:
            backup_path = self._backup_file(file_path)
            analysis = self._analyze_code(file_path)
            if not self._is_safe(analysis):
                self.logger.warning(f"Skipping {file_path}: safety threshold not met.")
                continue
            improved_code = self._generate_improvement(file_path, analysis)
            if improved_code and self._validate_code(improved_code):
                self._apply_improvement(file_path, improved_code)
                self._record_in_zettelkasten(file_path, analysis, improved_code)
                results.append({"file": str(file_path), "status": "improved"})
            else:
                self._rollback(file_path, backup_path)
                results.append({"file": str(file_path), "status": "rollback"})
        return results

    def _discover_files(self) -> List[Path]:
        """Scan target directories for Python files."""
        found = []
        for d in self.target_dirs:
            for root, _, files in os.walk(d):
                for f in files:
                    if f.endswith(".py") and f not in self.excluded_files:
                        found.append(Path(root) / f)
        return found

    def _backup_file(self, file_path: Path) -> Path:
        backup_path = self.backup_dir / f"{file_path.name}.{int(time.time())}.bak"
        shutil.copy2(file_path, backup_path)
        return backup_path

    def _analyze_code(self, file_path: Path) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        prompt = f"""
        Analyze the following Python code for improvement opportunities:
        {code[:self.config.get('ai_analysis_config', {}).get('max_code_length', 2000)]}
        Focus areas: {', '.join(self.config.get('ai_analysis_config', {}).get('focus_areas', ['performance_optimization', 'bug_fixes']))}
        """
        return self.ai_manager.analyze_code(prompt)

    def _is_safe(self, analysis: Dict[str, Any]) -> bool:
        # Dummy safety check for now
        return analysis.get("risk_score", 0) <= self.safety_threshold

    def _generate_improvement(self, file_path: Path, analysis: Dict[str, Any]) -> str:
        prompt = f"""
        Based on this analysis, generate an improved version of the code:
        {analysis.get('suggestions', '')}
        """
        return self.ai_manager.generate_code(prompt)

    def _validate_code(self, code: str) -> bool:
        # Syntax validation
        try:
            compile(code, "<string>", "exec")
            return True
        except Exception as e:
            self.logger.error(f"Syntax validation failed: {e}")
            return False

    def _apply_improvement(self, file_path: Path, code: str):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        self.logger.info(f"Applied improvement to {file_path}")

    def _rollback(self, file_path: Path, backup_path: Path):
        shutil.copy2(backup_path, file_path)
        self.logger.warning(f"Rolled back {file_path} to backup {backup_path}")

    def _record_in_zettelkasten(self, file_path: Path, analysis: Dict[str, Any], improved_code: str):
        card = {
            "original_analysis": analysis,
            "improvements_made": improved_code,
            "timestamp": datetime.now().isoformat()
        }
        self.zettelkasten.create_card(
            content=json.dumps(card, indent=2),
            title=f"Self-Improvement: {os.path.basename(file_path)}",
            category="self_improvement",
            tags=["ai-generated", "code-improvement", "self-modification"]
        )

    def start_continuous_improvement(self):
        interval = self.config["improvement_settings"]["cycle_interval_hours"] * 3600
        while True:
            self.run_improvement_cycle()
            time.sleep(interval) 