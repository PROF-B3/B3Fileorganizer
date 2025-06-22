#!/usr/bin/env python3
"""
B3Computer Drive Manager
Handles access to X: and B: drives with safety protocols
"""
import os
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import time

class DriveManager:
    """Manages X: and B: drive operations for B3Computer"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Use actual drive letters
        self.x_drive = Path("X:/")
        self.b_drive = Path("B:/")
        
        # Check if drives exist (don't create them - they're real drives!)
        if not self.x_drive.exists():
            self.logger.warning("X: drive not accessible or doesn't exist")
        if not self.b_drive.exists():
            self.logger.warning("B: drive not accessible or doesn't exist")
        # Safety settings
        self.max_file_size_mb = 500
        self.allowed_extensions = {'.py', '.txt', '.md', '.json', '.csv', '.log'}
        self.forbidden_patterns = ['system32', 'windows', 'program files']

    def scan_x_drive(self) -> Dict[str, Any]:
        """Scan X: drive for files to organize"""
        if not self.x_drive.exists():
            return {'files_found': 0, 'error': 'X: drive not found'}
        files = []
        for file_path in self.x_drive.rglob("*"):
            if file_path.is_file() and self._is_safe_file(file_path):
                files.append({
                    'path': str(file_path),
                    'name': file_path.name,
                    'size': file_path.stat().st_size,
                    'extension': file_path.suffix,
                    'modified': file_path.stat().st_mtime
                })
        return {
            'success': True,
            'files_found': len(files),
            'files': files,
            'drive': 'X:'
        }

    def scan_b_drive(self) -> Dict[str, Any]:
        """Scan B: drive for databases and backups"""
        if not self.b_drive.exists():
            return {'databases': [], 'error': 'B: drive not found'}
        databases = []
        backups = []
        for file_path in self.b_drive.rglob("*"):
            if file_path.is_file() and self._is_safe_file(file_path):
                file_info = {
                    'path': str(file_path),
                    'name': file_path.name,
                    'size': file_path.stat().st_size,
                    'modified': file_path.stat().st_mtime
                }
                if file_path.suffix in ['.db', '.sqlite', '.sql']:
                    databases.append(file_info)
                elif 'backup' in file_path.name.lower():
                    backups.append(file_info)
        return {
            'success': True,
            'databases': databases,
            'backups': backups,
            'drive': 'B:'
        }

    def organize_x_drive_files(self, organization_plan: Dict[str, str]) -> Dict[str, Any]:
        """Organize files on X: drive based on AI analysis"""
        results = {
            'success': True,
            'organized_files': 0,
            'created_folders': 0,
            'errors': []
        }
        try:
            for file_path, target_category in organization_plan.items():
                source_path = Path(file_path)
                if not source_path.exists():
                    continue
                # Create target directory
                target_dir = self.x_drive / target_category
                target_dir.mkdir(exist_ok=True)
                results['created_folders'] += 1
                # Move file safely
                target_path = target_dir / source_path.name
                if self._safe_move_file(source_path, target_path):
                    results['organized_files'] += 1
                else:
                    results['errors'].append(f"Failed to move {source_path}")
        except Exception as e:
            results['success'] = False
            results['errors'].append(str(e))
        return results

    def backup_to_b_drive(self, file_path: str, backup_name: str = None) -> bool:
        """Backup file to B: drive"""
        try:
            source = Path(file_path)
            if not source.exists():
                return False
            backup_name = backup_name or f"{source.stem}_backup_{int(time.time())}{source.suffix}"
            backup_path = self.b_drive / "backups" / backup_name
            backup_path.parent.mkdir(exist_ok=True)
            shutil.copy2(source, backup_path)
            return True
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            return False

    def _is_safe_file(self, file_path: Path) -> bool:
        """Check if file is safe to process"""
        # Size check
        try:
            if file_path.stat().st_size > self.max_file_size_mb * 1024 * 1024:
                return False
        except:
            return False
        # Extension check
        if file_path.suffix not in self.allowed_extensions and file_path.suffix:
            return False
        # Path safety check
        path_str = str(file_path).lower()
        if any(pattern in path_str for pattern in self.forbidden_patterns):
            return False
        return True

    def _safe_move_file(self, source: Path, target: Path) -> bool:
        """Safely move file with error handling"""
        try:
            if target.exists():
                # Create unique name
                counter = 1
                while target.exists():
                    name_parts = target.stem, counter, target.suffix
                    target = target.parent / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                    counter += 1
            shutil.move(str(source), str(target))
            return True
        except Exception as e:
            self.logger.error(f"File move failed: {e}")
            return False

    def get_drive_status(self) -> Dict[str, Any]:
        """Check real drive access"""
        return {
            'x_drive': {
                'path': "X:/",
                'exists': self.x_drive.exists(),
                'accessible': self.x_drive.exists() and os.access(self.x_drive, os.R_OK | os.W_OK)
            },
            'b_drive': {
                'path': "B:/", 
                'exists': self.b_drive.exists(),
                'accessible': self.b_drive.exists() and os.access(self.b_drive, os.R_OK | os.W_OK)
            }
        } 