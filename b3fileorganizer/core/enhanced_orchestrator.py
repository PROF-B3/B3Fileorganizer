"""
Erweiterter Agenten-Orchestrator für B3FileOrganizer v2.0
Features: Unterbrechungsfähigkeit, Echtzeit-Überwachung und direkte Dateisystem-Operationen.
"""

import json
import logging
import threading
import time
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from datetime import datetime

try:
    import autogen
    from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    logging.warning("autogen nicht verfügbar - verwende Fallback-Orchestrierung")

from .ai_manager import AIManager
from .database_manager import DatabaseManager
from .zettelkasten import ZettelkastenManager
from b3fileorganizer.utils.file_operations import FileOperations
from b3fileorganizer.utils.conversation_logger import ConversationLogger

class ErweiterterOrchestrator:
    """Erweiterter Orchestrator mit Unterbrechungsfähigkeit und Echtzeit-Überwachung."""
    
    def __init__(self, config_path: str = "config/agent_orchestrator.json"):
        self.config_path = config_path
        self.config = {}
        self.agents = {}
        self.logger = logging.getLogger(__name__)
        
        # Unterbrechungssteuerung
        self.running = False
        self.interrupt_requested = False
        self.current_operation = None
        self.operation_progress = 0.0
        
        # Systemkomponenten
        self.ai_manager = AIManager()
        self.db_manager = DatabaseManager()
        self.zettel_manager = ZettelkastenManager()
        self.file_ops = FileOperations()
        self.conversation_logger = ConversationLogger()
        
        # Überwachungs-Callbacks
        self.progress_callbacks: List[Callable[[float, str], None]] = []
        self.conversation_callbacks: List[Callable[[str, str], None]] = []
        self.status_callbacks: List[Callable[[str, str], None]] = []
        
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
            self.logger.info("Erweiterte Orchestrator-Konfiguration geladen")
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
                    "system_message": "Du bist ein Experte für Dateiorganisation mit der Zettelkasten-Methode. Du kannst Ordner erstellen und Dateien direkt organisieren.",
                    "description": "Spezialisiert auf Dateikategorisierung und -organisation"
                },
                "beta": {
                    "name": "Beta", 
                    "greek_symbol": "Β",
                    "role": "Inhaltsanalyse-Spezialist",
                    "model": "llama3.2:3b",
                    "system_message": "Du bist ein Experte für Inhaltsanalyse. Analysiere Dateiinhalte für Themen und Kategorien.",
                    "description": "Analysiert Dateiinhalte für Themen und Kategorien"
                },
                "gamma": {
                    "name": "Gamma",
                    "greek_symbol": "Γ",
                    "role": "Zettelkasten-System-Manager",
                    "model": "codellama:latest",
                    "system_message": "Du bist ein Zettelkasten-Systemexperte. Verwalte Nummerierung und Querverweise.",
                    "description": "Verwaltet Zettelkasten-Nummerierung und Querverweise"
                },
                "delta": {
                    "name": "Delta",
                    "greek_symbol": "Δ",
                    "role": "System-Koordinator",
                    "model": "mixtral:latest",
                    "system_message": "Du koordinierst Systemoperationen und behandelst Unterbrechungen elegant.",
                    "description": "Koordiniert Systemoperationen und Unterbrechungsbehandlung"
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
                    "api_key": "dummy"
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
                code_execution_config=False,
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
            
            self.logger.info(f"{len(self.agents)} erweiterte Agenten erfolgreich initialisiert")
            
        except Exception as e:
            self.logger.error(f"Fehler beim Initialisieren erweiterter Agenten: {e}")
            self.agents = {}
    
    def add_progress_callback(self, callback: Callable[[float, str], None]):
        """Füge Fortschritts-Überwachungs-Callback hinzu."""
        self.progress_callbacks.append(callback)
    
    def add_conversation_callback(self, callback: Callable[[str, str], None]):
        """Füge Konversations-Überwachungs-Callback hinzu."""
        self.conversation_callbacks.append(callback)
    
    def add_status_callback(self, callback: Callable[[str, str], None]):
        """Füge Status-Überwachungs-Callback hinzu."""
        self.status_callbacks.append(callback)
    
    def _update_progress(self, progress: float, message: str):
        """Aktualisiere Fortschritt und benachrichtige Callbacks."""
        self.operation_progress = progress
        for callback in self.progress_callbacks:
            try:
                callback(progress, message)
            except Exception as e:
                self.logger.error(f"Fortschritts-Callback-Fehler: {e}")
    
    def _display_conversation(self, agent_name: str, message: str):
        """Zeige Agenten-Konversation an und benachrichtige Callbacks."""
        for callback in self.conversation_callbacks:
            try:
                callback(agent_name, message)
            except Exception as e:
                self.logger.error(f"Konversations-Callback-Fehler: {e}")
    
    def _update_status(self, status: str, details: str):
        """Aktualisiere Status und benachrichtige Callbacks."""
        for callback in self.status_callbacks:
            try:
                callback(status, details)
            except Exception as e:
                self.logger.error(f"Status-Callback-Fehler: {e}")
    
    def start_operation(self, operation_type: str, parameters: Dict[str, Any]):
        """Starte eine neue Operation mit Unterbrechungsfähigkeit."""
        self.running = True
        self.interrupt_requested = False
        self.current_operation = operation_type
        self.operation_progress = 0.0
        
        self._update_status("gestartet", f"Operation {operation_type} gestartet")
        self._update_progress(0.0, f"Starte {operation_type}")
        
        # Starte Operation in separatem Thread
        operation_thread = threading.Thread(
            target=self._run_operation,
            args=(operation_type, parameters),
            daemon=True
        )
        operation_thread.start()
        
        return {"status": "gestartet", "operation": operation_type}
    
    def request_interruption(self):
        """Fordere Unterbrechung der aktuellen Operation an."""
        if not self.running:
            return {"status": "nicht_laufend", "message": "Keine Operation läuft"}
        
        self.interrupt_requested = True
        self._update_status("unterbrechend", "Unterbrechung angefordert")
        self._update_progress(self.operation_progress, "Unterbrechung läuft...")
        
        return {"status": "unterbrechend", "message": "Unterbrechung angefordert"}
    
    def check_interruption(self) -> bool:
        """Prüfe ob Unterbrechung angefordert wurde."""
        return self.interrupt_requested
    
    def _run_operation(self, operation_type: str, parameters: Dict[str, Any]):
        """Führe Operation mit Unterbrechungsprüfung aus."""
        try:
            if operation_type == "dateiorganisation":
                self._run_dateiorganisation(parameters)
            elif operation_type == "zettelkasten_erstellung":
                self._run_zettelkasten_erstellung(parameters)
            elif operation_type == "inhaltsanalyse":
                self._run_inhaltsanalyse(parameters)
            else:
                self._update_status("fehler", f"Unbekannter Operationstyp: {operation_type}")
                
        except Exception as e:
            self.logger.error(f"Operationsfehler: {e}")
            self._update_status("fehler", str(e))
        finally:
            self.running = False
            self.current_operation = None
            self._update_status("abgeschlossen", "Operation abgeschlossen")
    
    def _run_dateiorganisation(self, parameters: Dict[str, Any]):
        """Führe Dateiorganisations-Operation aus."""
        directory = parameters.get("directory", "")
        files = parameters.get("files", [])
        
        self._update_progress(0.1, "Analysiere Verzeichnisstruktur")
        if self.check_interruption():
            return
        
        # Verzeichnis scannen
        scan_result = self.file_ops.scan_directory(directory)
        if "error" in scan_result:
            self._update_status("fehler", f"Verzeichnis-Scan-Fehler: {scan_result['error']}")
            return
        
        self._update_progress(0.2, "Analysiere Dateiinhalte")
        if self.check_interruption():
            return
        
        # Dateien analysieren
        analysis_results = []
        for i, file_name in enumerate(files):
            if self.check_interruption():
                return
            
            file_path = Path(directory) / file_name
            analysis = self.file_ops.analyze_file_content(str(file_path))
            if "error" not in analysis:
                analysis_results.append(analysis)
            
            progress = 0.2 + (i / len(files)) * 0.3
            self._update_progress(progress, f"Analysiere {file_name}")
        
        self._update_progress(0.5, "Bestimme Organisationsstrategie")
        if self.check_interruption():
            return
        
        # Verwende KI um Organisationsstrategie zu bestimmen
        if self.agents:
            strategy = self._get_organisationsstrategie(analysis_results)
        else:
            strategy = self._get_fallback_strategie(analysis_results)
        
        self._update_progress(0.7, "Erstelle Ordner und organisiere Dateien")
        if self.check_interruption():
            return
        
        # Organisationsausführung
        organized_count = 0
        for i, (file_name, target_category) in enumerate(strategy.items()):
            if self.check_interruption():
                return
            
            # Erstelle Zielordner
            target_folder = Path(directory) / target_category
            folder_created = self.file_ops.create_folder(str(target_folder))
            if folder_created:
                # Meta-Zettel für den Ordner erzeugen
                folder_summary = f"Dieser Ordner ('{target_category}') wurde automatisch erstellt, um Dateien des Typs '{target_category}' zu organisieren.\n\nAlle zugehörigen Dateien werden hier gesammelt."
                zettel_title = f"Ordner-Kommentar: {target_category}"
                # Schreibe Zettel sowohl in X als auch in den Zielordner
                self.zettel_manager.create_zettel_card(
                    content=folder_summary,
                    title=zettel_title,
                    category=target_category,
                    extra_folder_path=str(target_folder)
                )
                # Verschiebe Datei
                source_path = Path(directory) / file_name
                target_path = target_folder / file_name
                if self.file_ops.move_file(str(source_path), str(target_path)):
                    organized_count += 1
                    # Aufzeichnung in Datenbank
                    self.db_manager.record_organization(
                        file_name, str(target_path), target_category, "verschieben"
                    )
            progress = 0.7 + (i / len(strategy)) * 0.3
            self._update_progress(progress, f"Organisiere {file_name}")
        
        self._update_progress(1.0, f"Organisation abgeschlossen: {organized_count} Dateien organisiert")
    
    def _run_zettelkasten_erstellung(self, parameters: Dict[str, Any]):
        """Führe Zettelkasten-Erstellungs-Operation aus."""
        content = parameters.get("content", "")
        title = parameters.get("title", "")
        category = parameters.get("category", "main")
        
        self._update_progress(0.2, "Analysiere Inhalte für thematische Verbindungen")
        if self.check_interruption():
            return
        
        # Finde thematische Verbindungen
        connections = self.zettel_manager.find_thematic_connections(content)
        
        self._update_progress(0.5, "Erstelle Zettelkasten-Karte")
        if self.check_interruption():
            return
        
        # Erstelle Karte
        card_data = self.zettel_manager.create_zettel_card(
            content=content,
            title=title,
            category=category,
            cross_references=connections
        )
        
        if "error" not in card_data:
            self._update_progress(1.0, f"Zettelkasten-Karte erstellt: {card_data['number']}")
        else:
            self._update_status("fehler", f"Karten-Erstellungsfehler: {card_data['error']}")
    
    def _run_inhaltsanalyse(self, parameters: Dict[str, Any]):
        """Führe Inhaltsanalyse-Operation aus."""
        file_path = parameters.get("file_path", "")
        
        self._update_progress(0.3, "Lese Dateiinhalt")
        if self.check_interruption():
            return
        
        # Analysiere Datei
        analysis = self.file_ops.analyze_file_content(file_path)
        if "error" in analysis:
            self._update_status("fehler", f"Analysenfehler: {analysis['error']}")
            return
        
        self._update_progress(0.6, "Generiere KI-Einblicke")
        if self.check_interruption():
            return
        
        # Hole KI-Einblicke
        if self.ai_manager:
            insight_prompt = f"Analysiere diese Dateianalyse und liefere Einblicke: {analysis}"
            insights = self.ai_manager.generate_response(insight_prompt, model_name="mixtral")
            analysis["ki_einblicke"] = insights
        
        self._update_progress(1.0, "Inhaltsanalyse abgeschlossen")
        return analysis
    
    def _get_organisationsstrategie(self, analysis_results: List[Dict]) -> Dict[str, str]:
        """Hole Organisationsstrategie mit KI-Agenten."""
        if not self.agents:
            return self._get_fallback_strategie(analysis_results)
        
        # Erstelle Strategie-Prompt
        strategy_prompt = f"""
        Analysiere diese Dateien und schlage Organisationskategorien vor:
        {analysis_results}
        
        Biete eine JSON-Antwort mit Dateiname -> Kategorie-Zuordnung.
        Verwende Zettelkasten-Prinzipien für Kategorisierung.
        """
        
        try:
            # Verwende Alpha-Agent
            response = self.ai_manager.generate_response(strategy_prompt, model_name="mixtral")
            
            # Parse Antwort (vereinfacht)
            strategy = {}
            for result in analysis_results:
                file_name = result.get("name", "")
                file_type = result.get("type", "unknown")
                strategy[file_name] = file_type
            
            return strategy
            
        except Exception as e:
            self.logger.error(f"Strategie-Generierungsfehler: {e}")
            return self._get_fallback_strategie(analysis_results)
    
    def _get_fallback_strategie(self, analysis_results: List[Dict]) -> Dict[str, str]:
        """Hole Fallback-Organisationsstrategie."""
        strategy = {}
        for result in analysis_results:
            file_name = result.get("name", "")
            file_type = result.get("type", "unknown")
            strategy[file_name] = file_type
        return strategy
    
    def get_operation_status(self) -> Dict[str, Any]:
        """Erhalte aktuellen Operationsstatus."""
        return {
            "running": self.running,
            "interrupt_requested": self.interrupt_requested,
            "current_operation": self.current_operation,
            "progress": self.operation_progress,
            "agents_available": len(self.agents),
            "autogen_available": AUTOGEN_AVAILABLE
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Erhalte Status aller Agenten."""
        return {
            "autogen_available": AUTOGEN_AVAILABLE,
            "agents_initialized": len(self.agents),
            "agent_names": list(self.agents.keys()) if self.agents else [],
            "config_loaded": bool(self.config),
            "interruption_enabled": self.config.get("orchestration", {}).get("interruption_enabled", False),
            "greek_agents": {
                "alpha": "Α - Dateiorganisation",
                "beta": "Β - Inhaltsanalyse", 
                "gamma": "Γ - Zettelkasten-Verwaltung",
                "delta": "Δ - System-Koordination"
            }
        }

# Alias für Rückwärtskompatibilität
InterruptibleOrchestrator = ErweiterterOrchestrator 