"""
File Operations for B3FileOrganizer
Handles actual file system operations for organization.
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
import hashlib
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class FileOperations:
    """Handles file system operations for organization."""
    
    def __init__(self, backup_enabled: bool = True, rules_path: str = "b3fileorganizer/config/file_and_zettel_rules.json"):
        self.backup_enabled = backup_enabled
        self.logger = logging.getLogger(__name__)
        self.rules_path = rules_path
        self.file_categorization_rules = self._load_categorization_rules()
    
    def _load_categorization_rules(self):
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                rules = json.load(f)
            return rules.get("file_categorization_rules", {})
        except Exception as e:
            self.logger.error(f"Error loading categorization rules: {e}")
            return {}
    
    def reload_rules(self):
        self.file_categorization_rules = self._load_categorization_rules()
    
    def scan_directory(self, path: str) -> Dict[str, Any]:
        """Scan directory and return files and folders."""
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                return {"files": [], "folders": [], "error": "Directory not found"}
            
            files = []
            folders = []
            
            for item in path_obj.iterdir():
                if item.is_file():
                    files.append(item.name)
                elif item.is_dir():
                    folders.append(item.name)
            
            return {
                "files": sorted(files),
                "folders": sorted(folders),
                "path": str(path_obj.absolute())
            }
            
        except Exception as e:
            self.logger.error(f"Error scanning directory {path}: {e}")
            return {"files": [], "folders": [], "error": str(e)}
    
    def analyze_file_content(self, file_path: str) -> Dict:
        """Analyze file content for categorization."""
        try:
            path_obj = Path(file_path)
            if not path_obj.exists():
                return {"error": "File not found"}
            
            # Basic file analysis
            analysis = {
                "name": path_obj.name,
                "extension": path_obj.suffix.lower(),
                "size": path_obj.stat().st_size,
                "modified": datetime.fromtimestamp(path_obj.stat().st_mtime),
                "type": self._get_file_type(path_obj.suffix),
                "content_preview": ""
            }
            
            # Try to extract content preview for text files
            if analysis["type"] == "text":
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1000)  # First 1000 characters
                        analysis["content_preview"] = content
                except Exception:
                    analysis["content_preview"] = "[Binary or encoded content]"
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {e}")
            return {"error": str(e)}
    
    def _get_file_type(self, extension: str) -> str:
        """Determine file type from extension using config rules."""
        ext_lower = extension.lower()
        for category, ext_list in self.file_categorization_rules.items():
            if ext_lower in ext_list:
                return category
        return "unknown"
    
    def create_folder(self, folder_path: str) -> bool:
        """Create folder if it doesn't exist."""
        try:
            path_obj = Path(folder_path)
            path_obj.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created folder: {folder_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating folder {folder_path}: {e}")
            return False
    
    def move_file(self, source: str, destination: str, overwrite: bool = False) -> bool:
        """Move file from source to destination."""
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                self.logger.error(f"Source file not found: {source}")
                return False
            
            # Create destination directory if it doesn't exist
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Handle file conflicts
            if dest_path.exists() and not overwrite:
                # Generate unique filename
                counter = 1
                while dest_path.exists():
                    stem = dest_path.stem
                    suffix = dest_path.suffix
                    dest_path = dest_path.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
            
            # Move the file
            shutil.move(str(source_path), str(dest_path))
            self.logger.info(f"Moved file: {source} -> {dest_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error moving file {source} to {destination}: {e}")
            return False
    
    def rename_file(self, old_path: str, new_name: str) -> bool:
        """Rename a file."""
        try:
            old_path_obj = Path(old_path)
            new_path_obj = old_path_obj.parent / new_name
            
            if not old_path_obj.exists():
                self.logger.error(f"File not found: {old_path}")
                return False
            
            # Handle conflicts
            if new_path_obj.exists():
                counter = 1
                while new_path_obj.exists():
                    stem = new_path_obj.stem
                    suffix = new_path_obj.suffix
                    new_path_obj = new_path_obj.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
            
            old_path_obj.rename(new_path_obj)
            self.logger.info(f"Renamed file: {old_path} -> {new_path_obj}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error renaming file {old_path}: {e}")
            return False
    
    def get_duplicate_files(self, directory: str) -> List[List[str]]:
        """Find duplicate files by content hash."""
        try:
            hash_dict = {}
            duplicates = []
            
            for file_path in Path(directory).rglob('*'):
                if file_path.is_file():
                    try:
                        file_hash = self._get_file_hash(file_path)
                        if file_hash in hash_dict:
                            hash_dict[file_hash].append(str(file_path))
                        else:
                            hash_dict[file_hash] = [str(file_path)]
                    except Exception:
                        continue
            
            # Return groups of duplicates
            for file_hash, file_list in hash_dict.items():
                if len(file_list) > 1:
                    duplicates.append(file_list)
            
            return duplicates
            
        except Exception as e:
            self.logger.error(f"Error finding duplicates in {directory}: {e}")
            return []
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def cleanup_empty_folders(self, directory: str) -> int:
        """Remove empty folders recursively."""
        try:
            count = 0
            for root, dirs, files in os.walk(directory, topdown=False):
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    try:
                        if not any(dir_path.iterdir()):  # Empty directory
                            dir_path.rmdir()
                            count += 1
                            self.logger.info(f"Removed empty folder: {dir_path}")
                    except Exception:
                        continue
            return count
        except Exception as e:
            self.logger.error(f"Error cleaning up empty folders in {directory}: {e}")
            return 0
    
    def backup_file(self, file_path: str, backup_dir: str) -> Optional[str]:
        """Create backup of file."""
        if not self.backup_enabled:
            return None
            
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                return None
            
            # Create backup directory with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = Path(backup_dir) / f"{source_path.stem}_{timestamp}{source_path.suffix}"
            
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, backup_path)
            
            self.logger.info(f"Backed up file: {file_path} -> {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            self.logger.error(f"Error backing up file {file_path}: {e}")
            return None 