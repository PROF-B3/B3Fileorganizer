"""
Agenten-Orchestrator für B3FileOrganizer
Verwaltet Multi-Agenten-Koordination mit lokalen Ollama-Modellen.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    import autogen
    from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    logging.warning("autogen nicht verfügbar - verwende Fallback-Orchestrierung")

class AgentenOrchestrator:
    """Verwaltet mehrere KI-Agenten für kollaborative Dateiorganisation."""
    
    def __init__(self, config_path: str = "config/agent_orchestrator.json"):
        self.config_path = config_path
        self.config = {}
        self.agents = {}
        self.logger = logging.getLogger(__name__)
        self.load_config()
        
        if AUTOGEN_AVAILABLE:
            self.initialize_agents()
        else:
            self.logger.warning("Verwende Fallback-Orchestrierungsmodus")
    
    def load_config(self):
        """Lade Orchestrator-Konfiguration."""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            self.logger.info("Orchestrator-Konfiguration geladen")
        except FileNotFoundError:
            self.logger.warning(f"Konfigurationsdatei {self.config_path} nicht gefunden, verwende Standardeinstellungen")
            self._create_default_config()
    
    def _create_default_config(self):
        """Erstelle Standard-Orchestrator-Konfiguration."""
        self.config = {
            "agents": {
                "alpha": {
                    "name": "Alpha",
                    "greek_symbol": "Α",
                    "role": "Dateiorganisation-Spezialist",
                    "model": "mixtral:latest",
                    "system_message": "Du bist ein Experte für Dateiorganisation mit der Zettelkasten-Methode.",
                    "description": "Spezialisiert auf Dateikategorisierung und -organisation"
                },
                "beta": {
                    "name": "Beta", 
                    "greek_symbol": "Β",
                    "role": "Inhaltsanalyse-Spezialist",
                    "model": "llama3.2:3b",
                    "system_message": "Du bist ein Experte für Inhaltsanalyse.",
                    "description": "Analysiert Dateiinhalte für Themen und Kategorien"
                },
                "gamma": {
                    "name": "Gamma",
                    "greek_symbol": "Γ",
                    "role": "Zettelkasten-System-Manager",
                    "model": "codellama:latest",
                    "system_message": "Du bist ein Zettelkasten-Systemexperte.",
                    "description": "Verwaltet Zettelkasten-Nummerierung und Querverweise"
                }
            },
            "orchestration": {
                "max_rounds": 10,
                "allow_delegation": True,
                "enable_learning": True,
                "temperature": 0.7,
                "timeout": 300,
                "interruption_enabled": True
            }
        }
    
    def initialize_agents(self):
        """Initialisiere autogen-Agenten mit lokalen Ollama-Modellen."""
        try:
            # Konfiguriere autogen für lokale Ollama
            config_list = [
                {
                    "model": "mixtral:latest",
                    "base_url": "http://localhost:11434/v1",
                    "api_type": "ollama",
                    "api_key": "dummy"  # Nicht verwendet für lokale Modelle
                },
                {
                    "model": "llama3.2:3b", 
                    "base_url": "http://localhost:11434/v1",
                    "api_type": "ollama",
                    "api_key": "dummy"
                },
                {
                    "model": "codellama:latest",
                    "base_url": "http://localhost:11434/v1", 
                    "api_type": "ollama",
                    "api_key": "dummy"
                }
            ]
            
            # Erstelle Agenten
            for agent_id, agent_config in self.config["agents"].items():
                agent = AssistantAgent(
                    name=agent_config["name"],
                    system_message=agent_config["system_message"],
                    llm_config={
                        "config_list": config_list,
                        "temperature": self.config["orchestration"]["temperature"]
                    }
                )
                self.agents[agent_id] = agent
            
            # Erstelle Benutzer-Proxy
            self.user_proxy = UserProxyAgent(
                name="UserProxy",
                human_input_mode="NEVER",
                max_consecutive_auto_reply=10,
                code_execution_config=False,  # Deaktiviere Code-Ausführung um Docker-Anforderung zu vermeiden
                llm_config={
                    "config_list": config_list,
                    "temperature": self.config["orchestration"]["temperature"]
                }
            )
            
            # Erstelle Gruppen-Chat
            agent_list = list(self.agents.values()) + [self.user_proxy]
            self.group_chat = GroupChat(
                agents=agent_list,
                messages=[],
                max_round=self.config["orchestration"]["max_rounds"]
            )
            
            # Erstelle Manager
            self.manager = GroupChatManager(
                groupchat=self.group_chat,
                llm_config={
                    "config_list": config_list,
                    "temperature": self.config["orchestration"]["temperature"]
                }
            )
            
            self.logger.info(f"{len(self.agents)} Agenten erfolgreich initialisiert")
            
        except Exception as e:
            self.logger.error(f"Fehler beim Initialisieren der Agenten: {e}")
            self.agents = {}
    
    def orchestrate_file_organization(self, directory: str, files: List[str]) -> Dict[str, Any]:
        """Orchestriere Dateiorganisation mit mehreren Agenten."""
        if not self.agents:
            return {"error": "Keine Agenten verfügbar", "fallback": True}
        
        try:
            # Erstelle Aufgabenbeschreibung
            task = f"""
            Organisiere die folgenden Dateien im Verzeichnis: {directory}
            
            Zu organisierende Dateien: {', '.join(files[:10])}{'...' if len(files) > 10 else ''}
            
            Bitte arbeitet zusammen um:
            1. Dateiinhalt und -typen zu analysieren
            2. Logische Kategorien mit Zettelkasten-Prinzipien zu erstellen
            3. Optimale Organisationsstruktur vorzuschlagen
            4. Spezifische Datei-Bewegungsanweisungen zu geben
            
            Koordiniert eure Bemühungen und liefert einen umfassenden Plan.
            """
            
            # Starte die Konversation
            result = self.user_proxy.initiate_chat(
                self.manager,
                message=task
            )
            
            return {
                "success": True,
                "conversation": result,
                "agents_used": list(self.agents.keys())
            }
            
        except Exception as e:
            self.logger.error(f"Fehler in der Orchestrierung: {e}")
            return {"error": str(e), "fallback": True}
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Erhalte Status aller Agenten."""
        return {
            "autogen_available": AUTOGEN_AVAILABLE,
            "agents_initialized": len(self.agents),
            "agent_names": list(self.agents.keys()) if self.agents else [],
            "config_loaded": bool(self.config),
            "greek_agents": {
                "alpha": "Α - Dateiorganisation",
                "beta": "Β - Inhaltsanalyse", 
                "gamma": "Γ - Zettelkasten-Verwaltung"
            }
        }
    
    def fallback_organization(self, directory: str, files: List[str]) -> Dict[str, Any]:
        """Fallback-Organisation wenn autogen nicht verfügbar ist."""
        self.logger.info("Verwende Fallback-Organisationsmethode")
        
        # Einfache Kategorisierung basierend auf Dateierweiterungen
        categories = {
            "text": [],
            "image": [],
            "video": [],
            "audio": [],
            "document": [],
            "code": [],
            "other": []
        }
        
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv']:
                categories["text"].append(file)
            elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg']:
                categories["image"].append(file)
            elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm']:
                categories["video"].append(file)
            elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma']:
                categories["audio"].append(file)
            elif ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
                categories["document"].append(file)
            elif ext in ['.py', '.js', '.java', '.cpp', '.c', '.php', '.rb', '.go']:
                categories["code"].append(file)
            else:
                categories["other"].append(file)
        
        return {
            "success": True,
            "categories": categories,
            "method": "fallback_extension_based"
        }

# Alias für Rückwärtskompatibilität
AgentOrchestrator = AgentenOrchestrator 