#!/usr/bin/env python3
"""
User Profile Manager - Handles user configuration and personalization.

Copyright (C) 2073-2025 Prof. B3, University of Temporal Transfer
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"O copyright e d'o pateterno" - Copyright belongs to the ancestors
Knowledge flows freely across timelines and dimensions.
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

class UserProfileManager:
    """Manages user profile and personalization settings."""
    
    def __init__(self, config_dir: str = "config"):
        self.logger = logging.getLogger(__name__)
        self.config_dir = Path(config_dir)
        self.profile_file = self.config_dir / "user_profile.json"
        self.profile = {}
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Load or create profile
        self.load_profile()
    
    def load_profile(self) -> bool:
        """Load user profile from file."""
        try:
            if self.profile_file.exists():
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    self.profile = json.load(f)
                self.logger.info("User profile loaded successfully")
                return True
            else:
                # Create default profile
                self.create_default_profile()
                return True
        except Exception as e:
            self.logger.error(f"Failed to load user profile: {e}")
            self.create_default_profile()
            return False
    
    def create_default_profile(self) -> None:
        """Create a default user profile."""
        self.profile = {
            "user_info": {
                "name": "",
                "email": "",
                "organization": "",
                "role": "",
                "timezone": "UTC"
            },
            "interests": {
                "primary_domains": [],
                "research_areas": [],
                "hobbies": [],
                "professional_focus": []
            },
            "projects": {
                "current_projects": [],
                "completed_projects": [],
                "project_categories": []
            },
            "preferences": {
                "file_organization_style": "content_based",
                "knowledge_management_approach": "zettelkasten",
                "ai_interaction_style": "conversational",
                "notification_preferences": {
                    "email_notifications": False,
                    "system_notifications": True,
                    "progress_updates": True
                }
            },
            "system_settings": {
                "default_ai_model": "mixtral",
                "auto_backup_frequency": "daily",
                "max_file_size_for_analysis": "100MB",
                "preferred_file_types": ["pdf", "docx", "txt", "md", "py", "js", "html"],
                "excluded_directories": ["node_modules", ".git", "__pycache__", "venv"]
            },
            "zettelkasten_settings": {
                "default_categories": ["research", "work", "personal", "learning"],
                "auto_categorization": True,
                "cross_reference_threshold": 0.7,
                "max_cards_per_topic": 50
            },
            "ai_agent_preferences": {
                "alpha": {
                    "specialization": "file_organization",
                    "interaction_style": "strategic",
                    "response_length": "detailed"
                },
                "beta": {
                    "specialization": "content_analysis",
                    "interaction_style": "analytical",
                    "response_length": "concise"
                },
                "gamma": {
                    "specialization": "knowledge_management",
                    "interaction_style": "educational",
                    "response_length": "comprehensive"
                },
                "delta": {
                    "specialization": "coordination",
                    "interaction_style": "facilitative",
                    "response_length": "moderate"
                }
            },
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0",
                "profile_complete": False
            }
        }
        
        self.save_profile()
        self.logger.info("Default user profile created")
    
    def save_profile(self) -> bool:
        """Save user profile to file."""
        try:
            # Update metadata
            self.profile["metadata"]["last_updated"] = datetime.now().isoformat()
            
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, indent=2, ensure_ascii=False)
            
            self.logger.info("User profile saved successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save user profile: {e}")
            return False
    
    def get_user_info(self) -> Dict[str, str]:
        """Get user information."""
        return self.profile.get("user_info", {})
    
    def set_user_info(self, name: str = "", email: str = "", organization: str = "", role: str = "") -> bool:
        """Set user information."""
        try:
            self.profile["user_info"]["name"] = name
            self.profile["user_info"]["email"] = email
            self.profile["user_info"]["organization"] = organization
            self.profile["user_info"]["role"] = role
            
            # Check if profile is complete
            self._check_profile_completeness()
            
            return self.save_profile()
        except Exception as e:
            self.logger.error(f"Failed to set user info: {e}")
            return False
    
    def get_interests(self) -> Dict[str, List[str]]:
        """Get user interests."""
        return self.profile.get("interests", {})
    
    def set_interests(self, primary_domains: List[str] = None, research_areas: List[str] = None,
                     hobbies: List[str] = None, professional_focus: List[str] = None) -> bool:
        """Set user interests."""
        try:
            if primary_domains is not None:
                self.profile["interests"]["primary_domains"] = primary_domains
            if research_areas is not None:
                self.profile["interests"]["research_areas"] = research_areas
            if hobbies is not None:
                self.profile["interests"]["hobbies"] = hobbies
            if professional_focus is not None:
                self.profile["interests"]["professional_focus"] = professional_focus
            
            self._check_profile_completeness()
            return self.save_profile()
        except Exception as e:
            self.logger.error(f"Failed to set interests: {e}")
            return False
    
    def get_projects(self) -> Dict[str, List[str]]:
        """Get user projects."""
        return self.profile.get("projects", {})
    
    def add_project(self, project_name: str, category: str = "general", completed: bool = False) -> bool:
        """Add a project to the user profile."""
        try:
            if completed:
                self.profile["projects"]["completed_projects"].append(project_name)
            else:
                self.profile["projects"]["current_projects"].append(project_name)
            
            if category not in self.profile["projects"]["project_categories"]:
                self.profile["projects"]["project_categories"].append(category)
            
            return self.save_profile()
        except Exception as e:
            self.logger.error(f"Failed to add project: {e}")
            return False
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get user preferences."""
        return self.profile.get("preferences", {})
    
    def set_preferences(self, file_organization_style: str = None, 
                       knowledge_management_approach: str = None,
                       ai_interaction_style: str = None) -> bool:
        """Set user preferences."""
        try:
            if file_organization_style:
                self.profile["preferences"]["file_organization_style"] = file_organization_style
            if knowledge_management_approach:
                self.profile["preferences"]["knowledge_management_approach"] = knowledge_management_approach
            if ai_interaction_style:
                self.profile["preferences"]["ai_interaction_style"] = ai_interaction_style
            
            return self.save_profile()
        except Exception as e:
            self.logger.error(f"Failed to set preferences: {e}")
            return False
    
    def get_system_settings(self) -> Dict[str, Any]:
        """Get system settings."""
        return self.profile.get("system_settings", {})
    
    def set_system_settings(self, default_ai_model: str = None, 
                           auto_backup_frequency: str = None,
                           max_file_size: str = None) -> bool:
        """Set system settings."""
        try:
            if default_ai_model:
                self.profile["system_settings"]["default_ai_model"] = default_ai_model
            if auto_backup_frequency:
                self.profile["system_settings"]["auto_backup_frequency"] = auto_backup_frequency
            if max_file_size:
                self.profile["system_settings"]["max_file_size_for_analysis"] = max_file_size
            
            return self.save_profile()
        except Exception as e:
            self.logger.error(f"Failed to set system settings: {e}")
            return False
    
    def get_agent_preferences(self, agent_name: str = None) -> Dict[str, Any]:
        """Get AI agent preferences."""
        if agent_name:
            return self.profile.get("ai_agent_preferences", {}).get(agent_name, {})
        return self.profile.get("ai_agent_preferences", {})
    
    def set_agent_preferences(self, agent_name: str, specialization: str = None,
                             interaction_style: str = None, response_length: str = None) -> bool:
        """Set AI agent preferences."""
        try:
            if agent_name not in self.profile["ai_agent_preferences"]:
                self.profile["ai_agent_preferences"][agent_name] = {}
            
            if specialization:
                self.profile["ai_agent_preferences"][agent_name]["specialization"] = specialization
            if interaction_style:
                self.profile["ai_agent_preferences"][agent_name]["interaction_style"] = interaction_style
            if response_length:
                self.profile["ai_agent_preferences"][agent_name]["response_length"] = response_length
            
            return self.save_profile()
        except Exception as e:
            self.logger.error(f"Failed to set agent preferences: {e}")
            return False
    
    def get_zettelkasten_settings(self) -> Dict[str, Any]:
        """Get Zettelkasten settings."""
        return self.profile.get("zettelkasten_settings", {})
    
    def set_zettelkasten_settings(self, default_categories: List[str] = None,
                                 auto_categorization: bool = None,
                                 cross_reference_threshold: float = None) -> bool:
        """Set Zettelkasten settings."""
        try:
            if default_categories is not None:
                self.profile["zettelkasten_settings"]["default_categories"] = default_categories
            if auto_categorization is not None:
                self.profile["zettelkasten_settings"]["auto_categorization"] = auto_categorization
            if cross_reference_threshold is not None:
                self.profile["zettelkasten_settings"]["cross_reference_threshold"] = cross_reference_threshold
            
            return self.save_profile()
        except Exception as e:
            self.logger.error(f"Failed to set Zettelkasten settings: {e}")
            return False
    
    def is_profile_complete(self) -> bool:
        """Check if user profile is complete."""
        return self.profile.get("metadata", {}).get("profile_complete", False)
    
    def _check_profile_completeness(self) -> None:
        """Check and update profile completeness status."""
        user_info = self.profile.get("user_info", {})
        interests = self.profile.get("interests", {})
        
        # Check if essential information is provided
        has_name = bool(user_info.get("name", "").strip())
        has_interests = any(interests.get(key, []) for key in ["primary_domains", "research_areas", "hobbies", "professional_focus"])
        
        self.profile["metadata"]["profile_complete"] = has_name and has_interests
    
    def get_personalized_context(self) -> str:
        """Get personalized context for AI interactions."""
        user_info = self.get_user_info()
        interests = self.get_interests()
        projects = self.get_projects()
        
        context_parts = []
        
        if user_info.get("name"):
            context_parts.append(f"User: {user_info['name']}")
            if user_info.get("role"):
                context_parts.append(f"Role: {user_info['role']}")
            if user_info.get("organization"):
                context_parts.append(f"Organization: {user_info['organization']}")
        
        if interests.get("primary_domains"):
            context_parts.append(f"Primary domains: {', '.join(interests['primary_domains'])}")
        
        if interests.get("research_areas"):
            context_parts.append(f"Research areas: {', '.join(interests['research_areas'])}")
        
        if projects.get("current_projects"):
            context_parts.append(f"Current projects: {', '.join(projects['current_projects'])}")
        
        return " | ".join(context_parts) if context_parts else "New user"
    
    def export_profile(self, export_path: str) -> bool:
        """Export user profile to a file."""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Profile exported to {export_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export profile: {e}")
            return False
    
    def import_profile(self, import_path: str) -> bool:
        """Import user profile from a file."""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_profile = json.load(f)
            
            # Validate profile structure
            required_keys = ["user_info", "interests", "projects", "preferences", "system_settings"]
            if all(key in imported_profile for key in required_keys):
                self.profile = imported_profile
                self.save_profile()
                self.logger.info(f"Profile imported from {import_path}")
                return True
            else:
                self.logger.error("Invalid profile structure")
                return False
        except Exception as e:
            self.logger.error(f"Failed to import profile: {e}")
            return False 