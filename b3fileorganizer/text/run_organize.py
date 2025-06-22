#!/usr/bin/env python3
"""
B3FileOrganizer v2.0 - Erweiterter Launcher mit griechischen Agenten
Ein KI-gestütztes Dateiorganisationssystem mit Zettelkasten-Integration.

Copyright (C) 2073-2025 Prof. B3, University of Temporal Transfer
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"O copyright e d'o pateterno" - Copyright belongs to the ancestors
Knowledge flows freely across timelines and dimensions.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from colorama import init as colorama_init, Fore, Style
import threading
import itertools
from b3fileorganizer.utils.i18n import tr, set_language

colorama_init(autoreset=True)

# ASCII Art Banner
# B3_ASCII = f"""
# {Fore.CYAN}{Style.BRIGHT}
#  ____   ____   ____   ____   ____   ____   ____   ____   ____
# |  __| |__  | |__  | |__  | |__  | |__  | |__  | |__  | |__  |
# | |__  |__| | |__| | |__| | |__| | |__| | |__| | |__| | |__| |
# |____| |____| |____| |____| |____| |____| |____| |____| |____|
#
# {Style.RESET_ALL}{Fore.YELLOW}B3FileOrganizer v2.0 - The Future of File Organization
# {Style.RESET_ALL}------------------------------------------------------------
# """

# Agent color mapping
AGENT_COLORS = {
    "Alpha": Fore.GREEN + Style.BRIGHT,
    "Beta": Fore.BLUE + Style.BRIGHT,
    "Gamma": Fore.MAGENTA + Style.BRIGHT,
    "Delta": Fore.YELLOW + Style.BRIGHT,
    "User": Fore.WHITE + Style.BRIGHT,
    "System": Fore.CYAN + Style.BRIGHT
}

# Agent ASCII icons
AGENT_ICONS = {
    "Alpha": f"{Fore.GREEN}{Style.BRIGHT}  Α  (🤖)  {Style.RESET_ALL}",
    "Beta": f"{Fore.BLUE}{Style.BRIGHT}  Β  (📘)  {Style.RESET_ALL}",
    "Gamma": f"{Fore.MAGENTA}{Style.BRIGHT}  Γ  (🧠)  {Style.RESET_ALL}",
    "Delta": f"{Fore.YELLOW}{Style.BRIGHT}  Δ  (⚙️ )  {Style.RESET_ALL}",
    "User": f"{Fore.WHITE}{Style.BRIGHT}  ☺  (You) {Style.RESET_ALL}",
    "System": f"{Fore.CYAN}{Style.BRIGHT}  Σ  (SYS) {Style.RESET_ALL}"
}

# Section divider
SECTION_DIVIDER = f"{Fore.CYAN}{Style.BRIGHT}" + "═"*50 + f"{Style.RESET_ALL}"

# Success banner
# SUCCESS_BANNER = f"""
# {Fore.GREEN}{Style.BRIGHT}
#   _____  _    _  ____   ____  _____  _____ 
#  / ____|| |  | ||  _ \/ __ \|  __ \|  __ \
# | (___  | |  | || |_) | |  | | |__) | |  | |
#  \___ \ | |  | ||  _ <| |  | |  _  /| |  | |
#  ____) || |__| || |_) | |__| | | \ \| |__| |
# |_____/  \____/ |____/ \____/|_|  \_\_____/
# {Style.RESET_ALL}
# """

# Error banner
# ERROR_BANNER = f"""
# {Fore.RED}{Style.BRIGHT}
#   ______ _____  _____  _____  _____ 
#  |  ____|  __ \|  __ \|  __ \|  __ \
#  | |__  | |__) | |__) | |  | | |__) |
#  |  __| |  _  /|  _  /| |  | |  _  /
#  | |____| | \ \| | \ \| |__| | | \ \
#  |______|_|  \_\_|  \_\_____/|_|  \_\
# {Style.RESET_ALL}
# """

# Welcome banner
WELCOME_BANNER = f"{Fore.CYAN}{Style.BRIGHT}B3 Archivar{Style.RESET_ALL}\n{Fore.YELLOW}The Future of File & Knowledge Organization{Style.RESET_ALL}\n{'-'*60}"

# Goodbye banner
GOODBYE_BANNER = f"{Fore.MAGENTA}{Style.BRIGHT}Goodbye! B3 Archivar is shutting down.{Style.RESET_ALL}"

# Core-Module importieren
from b3fileorganizer.core.ai_manager import AIManager
from b3fileorganizer.core.database_manager import DatabaseManager
from b3fileorganizer.core.resource_monitor import ResourceMonitor
from b3fileorganizer.core.config_manager import ConfigManager
from b3fileorganizer.core.progress_tracker import ProgressTracker
from b3fileorganizer.core.zettelkasten import ZettelkastenManager
from b3fileorganizer.core.enhanced_orchestrator import ErweiterterOrchestrator

# Utility-Module importieren
from b3fileorganizer.utils.file_operations import FileOperations
from b3fileorganizer.utils.conversation_logger import ConversationLogger
from b3fileorganizer.utils.report_generator import ReportGenerator
from b3fileorganizer.utils.status_monitor import StatusMonitor
from b3fileorganizer.utils.wikipedia_processor import WikipediaProcessor

# Onboarding module
from b3fileorganizer.core import onboarding

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('b3fileorganizer.log'),
        logging.StreamHandler()
    ]
)

class B3FileOrganizerLauncher:
    """Erweiterter Launcher für B3FileOrganizer v2.0 mit griechischen Agenten."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.version = "2.0.0"
        self.system_name = "B3FileOrganizer"
        self.alias = "User"
        # Load system_name and alias from user_profile.json if available
        try:
            with open("config/user_profile.json", "r", encoding="utf-8") as f:
                profile = json.load(f)
                self.system_name = profile.get("system_name", self.system_name)
                self.alias = profile.get("user_info", {}).get("alias", self.alias)
        except Exception:
            pass
        
        # Systemkomponenten initialisieren
        self.ai_manager = None
        self.db_manager = None
        self.resource_monitor = None
        self.config_manager = None
        self.progress_tracker = None
        self.zettel_manager = None
        self.orchestrator = None
        
        # Utility-Komponenten
        self.file_ops = None
        self.conversation_logger = None
        self.report_generator = None
        self.status_monitor = None
        self.wikipedia_processor = None
        
        # Status-Tracking
        self.current_operation = None
        self.operation_progress = 0.0
        
        self.initialize_system()
    
    def initialize_system(self):
        """Initialisiere alle Systemkomponenten."""
        try:
            self.logger.info("Initialisiere B3FileOrganizer v2.0 System...")
            
            # Core-Komponenten
            self.ai_manager = AIManager()
            self.db_manager = DatabaseManager()
            self.resource_monitor = ResourceMonitor()
            self.config_manager = ConfigManager()
            self.progress_tracker = ProgressTracker()
            self.zettel_manager = ZettelkastenManager()
            self.orchestrator = ErweiterterOrchestrator()
            
            # Utility-Komponenten
            self.file_ops = FileOperations()
            self.conversation_logger = ConversationLogger()
            self.report_generator = ReportGenerator()
            self.status_monitor = StatusMonitor()
            self.wikipedia_processor = WikipediaProcessor()
            
            # Orchestrator-Callbacks einrichten
            self.orchestrator.add_progress_callback(self._progress_callback)
            self.orchestrator.add_conversation_callback(self._conversation_callback)
            self.orchestrator.add_status_callback(self._status_callback)
            
            self.logger.info("System erfolgreich initialisiert")
            
        except Exception as e:
            self.logger.error(f"Systeminitialisierungsfehler: {e}")
            print(f"Fehler beim Initialisieren des Systems: {e}")
    
    def _progress_callback(self, progress: float, message: str):
        """Callback für Fortschrittsaktualisierungen."""
        self.operation_progress = progress
        print(f"\rFortschritt: {progress*100:.1f}% - {message}", end="", flush=True)
    
    def _conversation_callback(self, agent_name: str, message: str):
        """Callback für Agenten-Konversationen."""
        print(f"\n[{agent_name}]: {message}")
        self.conversation_logger.log_conversation(agent_name, message)
    
    def _status_callback(self, status: str, details: str):
        """Callback für Statusaktualisierungen."""
        print(f"\nStatus: {status} - {details}")
    
    def display_header(self):
        """Zeige System-Header an."""
        print(WELCOME_BANNER)
        print(f"{Fore.CYAN}{Style.BRIGHT}Version: {self.version}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(SECTION_DIVIDER)
    
    def display_menu(self):
        """Zeige Hauptmenü an (CLI version: single linear list)."""
        print(f"\nMAIN MENU")
        print("-"*60)
        print(f"1. 💬 Talk to {self.system_name} (your AI assistant)")
        print(f"2. 📊 System Dashboard & Status")
        print(f"3. 🤖 Multi-Agent Organization (Alpha, Beta, Gamma)")
        print(f"4. 📚 Wikipedia Knowledge Extraction")
        print(f"5. 🔍 Advanced File Analysis")
        print(f"6. 🧠 Learning System & Improvements")
        print(f"7. 🔧 Diagnostics & System Check")
        print(f"8. 🔄 Recalibrate Onboarding / Update Preferences")
        print(f"9. 🛠️ Self-Improvement & Module Creation")
        print(f"10. 📚 Research Assistant & Academic Writing")
        print(f"11. 📚 Research Assistant & Academic Writing")
        print(f"0. 🚪 Exit")
        print("-"*60)
    
    def show_status(self):
        """Show live agent/resource status and progress."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== SYSTEM STATUS ==={Style.RESET_ALL}")
        print(SECTION_DIVIDER)
        orch_status = self.orchestrator.get_agent_status() if self.orchestrator else {}
        op_status = self.orchestrator.get_operation_status() if self.orchestrator else {}
        usage = self.resource_monitor.get_current_resources() if self.resource_monitor else None
        if usage:
            print(f"{Fore.YELLOW}CPU: {usage.cpu_percent:.1f}% | RAM: {usage.memory_percent:.1f}%{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}CPU: N/A | RAM: N/A{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Agents initialized: {orch_status.get('agents_initialized', 0)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Agent names: {', '.join([AGENT_ICONS.get(name, name) + name for name in orch_status.get('agent_names', [])])}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Autogen available: {orch_status.get('autogen_available', False)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Current operation: {op_status.get('current_operation', 'None')}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Progress: {op_status.get('progress', 0.0)*100:.1f}%{Style.RESET_ALL}")
        print(SECTION_DIVIDER)
        print(f"{Fore.CYAN}{Style.BRIGHT}===================={Style.RESET_ALL}\n")
    
    def typewriter_print(self, text, color=Fore.WHITE, delay=0.01, agent=None):
        if agent and agent in AGENT_ICONS:
            print(AGENT_ICONS[agent], end=' ')
        for char in text:
            print(f"{color}{char}{Style.RESET_ALL}", end='', flush=True)
            time.sleep(delay)
        print()
    
    def option_1_simple_conversation(self):
        """Option 1: Einfache Konversation mit Alpha-Agent."""
        print(f"\n{Fore.GREEN}{Style.BRIGHT}💬 EINFACHE KONVERSATION MIT ALPHA (Α){Style.RESET_ALL}")
        print(SECTION_DIVIDER)
        print(f"{Fore.GREEN}Alpha ist der Dateiorganisation-Spezialist.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Du kannst Fragen zu Dateiorganisation, Zettelkasten oder allgemeine Fragen stellen.{Style.RESET_ALL}")
        print(SECTION_DIVIDER)
        
        # Start a new conversation session for logging
        conversation_id = self.conversation_logger.start_conversation(
            "simple_conversation_alpha", ["User", "Alpha"]
        )
        
        while True:
            try:
                user_input = input(f"\n{AGENT_ICONS['User']}{AGENT_COLORS['User']}Deine Nachricht (oder 'zurück' zum Hauptmenü, 'status' für Status): {Style.RESET_ALL}").strip()
                
                if user_input.lower() in ['zurück', 'back', 'exit', 'quit']:
                    print(GOODBYE_BANNER)
                    break
                if user_input.lower() == 'status':
                    self.show_status()
                    continue
                if not user_input:
                    continue
                print(f"\n{AGENT_ICONS['User']}{AGENT_COLORS['User']}[Du]: {user_input}{Style.RESET_ALL}\n")
                # Show progress dots while waiting for response
                stop_dots = False
                def dots():
                    for c in itertools.cycle(['.', '..', '...']):
                        if stop_dots:
                            break
                        print(f"\r{AGENT_ICONS['Alpha']}{AGENT_COLORS['Alpha']}[Alpha (Α)] arbeitet{c} (geschätzt 5-30s){Style.RESET_ALL}", end='', flush=True)
                        time.sleep(0.7)
                t = threading.Thread(target=dots)
                t.start()
                try:
                    response = self.ai_manager.generate_response(
                        f"Antworte als Alpha (Α), der Dateiorganisation-Spezialist: {user_input}",
                        model_name="mixtral"
                    )
                finally:
                    stop_dots = True
                    t.join()
                print(f"\r", end='')
                self.typewriter_print(f"[Alpha (Α)]: {response}\n", color=AGENT_COLORS['Alpha'], delay=0.012, agent="Alpha")
                # Log conversation using log_message
                self.conversation_logger.log_message(conversation_id, "User", user_input)
                self.conversation_logger.log_message(conversation_id, "Alpha", response)
                print("\n" + SECTION_DIVIDER)
            except KeyboardInterrupt:
                print(f"\n\n{Fore.RED}Konversation beendet.{Style.RESET_ALL}")
                print(GOODBYE_BANNER)
                break
            except Exception as e:
                print(ERROR_BANNER)
                print(f"{Fore.RED}Fehler: {e}{Style.RESET_ALL}")
    
    def option_2_system_dashboard(self):
        """Option 2: System-Dashboard & Status."""
        print("\n📊 SYSTEM-DASHBOARD & STATUS")
        print("="*60)
        
        # Systemstatus sammeln
        status_data = {
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "ai_models": self.ai_manager.get_model_status() if self.ai_manager else {},
            "database_status": {},  # No get_status method, so leave as empty or implement if needed
            "resource_usage": None,
            "orchestrator_status": self.orchestrator.get_agent_status() if self.orchestrator else {},
            "zettelkasten_status": self.zettel_manager.get_statistics() if self.zettel_manager else {}
        }
        
        # Status anzeigen
        print(f"🔄 Version: {status_data['version']}")
        print(f"⏰ Zeitstempel: {status_data['timestamp']}")
        
        print(f"\n🤖 KI-Modelle verfügbar:")
        for model, available in status_data['ai_models'].items():
            print(f"   - {model}: {'✅' if available else '❌'}")
        
        print(f"\n💾 Datenbank-Status: (nicht verfügbar)")
        
        print(f"\n💻 Ressourcen-Nutzung:")
        usage = self.resource_monitor.get_current_resources() if self.resource_monitor else None
        if usage:
            print(f"   - CPU: {usage.cpu_percent:.1f}%")
            print(f"   - RAM: {usage.memory_percent:.1f}%")
        else:
            print(f"   - CPU: N/A")
            print(f"   - RAM: N/A")
        
        print(f"\n🎭 Orchestrator-Status:")
        orch_status = status_data['orchestrator_status']
        print(f"   - Autogen verfügbar: {orch_status.get('autogen_available', False)}")
        print(f"   - Agenten initialisiert: {orch_status.get('agents_initialized', 0)}")
        print(f"   - Unterbrechung aktiviert: {orch_status.get('interruption_enabled', False)}")
        
        print(f"\n📚 Zettelkasten-Status:")
        zettel_status = status_data['zettelkasten_status']
        print(f"   - Karten insgesamt: {zettel_status.get('total_cards', 0)}")
        print(f"   - Hauptthemen: {zettel_status.get('main_topics', 0)}")
        print(f"   - Häufig genutzt: {zettel_status.get('frequently_accessed', 0)}")
        print(f"   - Zitate/Auszüge: {zettel_status.get('quotes_excerpts', 0)}")
        print(f"   - Querverweise: {zettel_status.get('cross_references', 0)}")
        print(f"   - Subthemen: {zettel_status.get('subtopics', 0)}")
        
        input("\nDrücke Enter zum Fortfahren...")
    
    def option_3_multi_agent_organization(self):
        """Option 3: Multi-Agenten-Organisation mit drei schwächeren Modellen."""
        print("\n🤖 MULTI-AGENTEN-ORGANISATION")
        print("Verwendet Alpha (Α), Beta (Β) und Gamma (Γ) für kooperative Dateiorganisation.")
        print("-"*60)
        
        # Verzeichnis auswählen
        directory = input("Verzeichnis zum Organisieren (oder Enter für aktuelles): ").strip()
        if not directory:
            directory = os.getcwd()
        
        if not os.path.exists(directory):
            print(f"Fehler: Verzeichnis '{directory}' existiert nicht.")
            return
        
        print(f"\nVerwende Verzeichnis: {directory}")
        
        # Dateien scannen
        print("Scanne Dateien...")
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        if not files:
            print("Keine Dateien im Verzeichnis gefunden.")
            return
        
        print(f"Gefunden: {len(files)} Dateien")
        
        # Multi-Agenten-Operation starten
        print("\nStarte Multi-Agenten-Organisation...")
        
        operation_params = {
            "directory": directory,
            "files": files,
            "agent_mode": "multi",
            "models": ["llama3.2:3b", "codellama:latest", "mixtral:latest"]
        }
        
        result = self.orchestrator.start_operation("dateiorganisation", operation_params)
        
        if result.get("status") == "gestartet":
            print("Operation gestartet. Überwache Fortschritt...")
            
            # Fortschritt überwachen
            while self.orchestrator.running:
                time.sleep(1)
                status = self.orchestrator.get_operation_status()
                if status.get("interrupt_requested"):
                    print("\nUnterbrechung angefordert...")
                    break
            
            print("\nOrganisation abgeschlossen!")
        else:
            print(f"Fehler beim Starten der Operation: {result}")
        
        input("\nDrücke Enter zum Fortfahren...")
    
    def option_4_wikipedia_extraction(self):
        """Option 4: Wikipedia-Wissen-Extraktion."""
        print("\n📚 WIKIPEDIA-WISSEN-EXTRAKTION")
        print("Extrahiert Wissen aus Wikipedia-Dumps für Zettelkasten-Integration.")
        print("-"*60)
        
        # Wikipedia-Dump-Pfad
        default_paths = ["X/b3wiki", "X/wikipedia_dumps"]
        dump_path = input(f"Pfad zu Wikipedia-Dump (Enter für Standard: {default_paths[0]}): ").strip()
        if not dump_path:
            # Auto-detect
            for path in default_paths:
                if os.path.exists(path):
                    dump_path = path
                    print(f"Verwende gefundenen Dump-Pfad: {dump_path}")
                    break
            else:
                print(f"Kein Standard-Wikipedia-Dump-Ordner gefunden. Bitte gib einen Pfad an.")
                dump_path = input("Pfad zu Wikipedia-Dump: ").strip()
                if not dump_path or not os.path.exists(dump_path):
                    print("Abbruch: Kein gültiger Dump-Pfad angegeben.")
                    return
        elif not os.path.exists(dump_path):
            print(f"Wikipedia-Dump-Pfad '{dump_path}' existiert nicht.")
            create_dump = input("Soll der Pfad erstellt werden? (j/n): ").strip().lower()
            if create_dump == 'j':
                os.makedirs(dump_path, exist_ok=True)
                print(f"Pfad '{dump_path}' erstellt.")
            else:
                return
        
        # Extraktionsparameter
        topic = input("Thema für Extraktion (oder Enter für allgemeine Extraktion): ").strip()
        max_articles = input("Maximale Anzahl Artikel (Standard: 100): ").strip()
        max_articles = int(max_articles) if max_articles.isdigit() else 100
        
        print(f"\nStarte Wikipedia-Extraktion...")
        print(f"Thema: {topic if topic else 'Allgemein'}")
        print(f"Max. Artikel: {max_articles}")
        
        # Extraktion starten
        extraction_params = {
            "dump_path": dump_path,
            "topic": topic,
            "max_articles": max_articles,
            "output_path": "X/wikipedia_extracted"
        }
        
        try:
            # Use process_wikipedia_dump instead of extract_knowledge
            result = self.wikipedia_processor.process_wikipedia_dump(
                dump_path, output_dir=extraction_params["output_path"]
            )
            
            if "error" not in result:
                print(f"\n✅ Extraktion erfolgreich!")
                print(f"Artikel extrahiert: {result.get('total_articles', 0)}")
                print(f"Ausgabepfad: {result.get('output_directory', '')}")
            else:
                print(f"\n❌ Extraktionsfehler: {result['error']}")
                
        except Exception as e:
            print(f"\n❌ Fehler bei der Extraktion: {e}")
        
        input("\nDrücke Enter zum Fortfahren...")
    
    def option_5_advanced_file_analysis(self):
        """Option 5: Erweiterte Dateianalyse."""
        print("\n🔍 ERWEITERTE DATEIANALYSE")
        print("Detaillierte Analyse von Dateien mit KI-Einblicken.")
        print("-"*60)
        
        # Datei auswählen
        file_path = input("Pfad zur zu analysierenden Datei: ").strip()
        
        if not os.path.exists(file_path):
            print(f"Fehler: Datei '{file_path}' existiert nicht.")
            return
        
        print(f"\nAnalysiere: {file_path}")
        
        # Analyse starten
        analysis_params = {
            "file_path": file_path,
            "include_ai_insights": True,
            "generate_summary": True,
            "suggest_organization": True
        }
        
        try:
            result = self.orchestrator.start_operation("inhaltsanalyse", analysis_params)
            
            if result.get("status") == "gestartet":
                print("Analyse gestartet...")
                
                # Warte auf Abschluss
                while self.orchestrator.running:
                    time.sleep(0.5)
                
                print("\n✅ Analyse abgeschlossen!")
                
                # Ergebnisse anzeigen
                analysis_result = self.file_ops.analyze_file_content(file_path)
                if "error" not in analysis_result:
                    print(f"\n📄 Datei: {analysis_result.get('name', 'Unbekannt')}")
                    print(f"📁 Typ: {analysis_result.get('type', 'Unbekannt')}")
                    print(f"📏 Größe: {analysis_result.get('size', 0)} Bytes")
                    print(f"📅 Erstellt: {analysis_result.get('created', 'Unbekannt')}")
                    
                    if 'ki_einblicke' in analysis_result:
                        print(f"\n🤖 KI-Einblicke:")
                        print(analysis_result['ki_einblicke'])
                
            else:
                print(f"Fehler beim Starten der Analyse: {result}")
                
        except Exception as e:
            print(f"\n❌ Analysenfehler: {e}")
        
        input("\nDrücke Enter zum Fortfahren...")
    
    def option_6_learning_system(self):
        """Option 6: Lernsystem & Verbesserungen."""
        print("\n🧠 LERNSYSTEM & VERBESSERUNGEN")
        print("System lernt aus Interaktionen und verbessert sich kontinuierlich.")
        print("-"*60)
        
        print("Lernsystem-Features:")
        print("1. 📊 Interaktionsanalyse")
        print("2. 🔄 Modell-Optimierung")
        print("3. 📈 Performance-Tracking")
        print("4. 🎯 Verbesserungsvorschläge")
        print("5. 📚 Wissensdatenbank-Update")
        
        choice = input("\nWähle eine Option (1-5) oder Enter für alle: ").strip()
        
        if not choice:
            # Alle Lernoperationen ausführen
            print("\nFühre alle Lernoperationen aus...")
            
            # 1. Interaktionsanalyse
            print("1. Analysiere Interaktionen...")
            interactions = self.conversation_logger.get_recent_interactions(limit=100)
            print(f"   {len(interactions)} Interaktionen analysiert")
            
            # 2. Modell-Optimierung
            print("2. Optimiere Modelle...")
            optimization_result = self.ai_manager.optimize_models() if self.ai_manager else {}
            print(f"   Optimierung abgeschlossen")
            
            # 3. Performance-Tracking
            print("3. Tracke Performance...")
            performance_data = self.progress_tracker.get_performance_metrics() if self.progress_tracker else {}
            print(f"   Performance-Daten gesammelt")
            
            # 4. Verbesserungsvorschläge
            print("4. Generiere Verbesserungsvorschläge...")
            suggestions = self._generate_improvement_suggestions()
            for i, suggestion in enumerate(suggestions, 1):
                print(f"   {i}. {suggestion}")
            
            # 5. Wissensdatenbank-Update
            print("5. Update Wissensdatenbank...")
            update_result = self.zettel_manager.update_knowledge_base() if self.zettel_manager else {}
            print(f"   Wissensdatenbank aktualisiert")
            
        else:
            # Spezifische Option ausführen
            if choice == "1":
                print("Analysiere Interaktionen...")
                interactions = self.conversation_logger.get_recent_interactions(limit=50)
                print(f"{len(interactions)} Interaktionen analysiert")
            
            elif choice == "2":
                print("Optimiere Modelle...")
                if self.ai_manager:
                    self.ai_manager.optimize_models()
                print("Modell-Optimierung abgeschlossen")
            
            elif choice == "3":
                print("Tracke Performance...")
                if self.progress_tracker:
                    metrics = self.progress_tracker.get_performance_metrics()
                    print("Performance-Daten gesammelt")
            
            elif choice == "4":
                print("Generiere Verbesserungsvorschläge...")
                suggestions = self._generate_improvement_suggestions()
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"{i}. {suggestion}")
            
            elif choice == "5":
                print("Update Wissensdatenbank...")
                if self.zettel_manager:
                    self.zettel_manager.update_knowledge_base()
                print("Wissensdatenbank aktualisiert")
        
        input("\nDrücke Enter zum Fortfahren...")
    
    def option_7_diagnostics(self):
        """Option 7: Diagnostik & Systemprüfung."""
        print("\n🔧 DIAGNOSTIK & SYSTEMPRÜFUNG")
        print("Umfassende Systemprüfung und Fehlerdiagnose.")
        print("-"*60)
        
        print("Führe Systemdiagnostik aus...")
        
        # 1. Komponenten-Test
        print("\n1. Teste Systemkomponenten...")
        components_status = {
            "AI Manager": self.ai_manager is not None,
            "Database Manager": self.db_manager is not None,
            "Resource Monitor": self.resource_monitor is not None,
            "Config Manager": self.config_manager is not None,
            "Progress Tracker": self.progress_tracker is not None,
            "Zettelkasten Manager": self.zettel_manager is not None,
            "Orchestrator": self.orchestrator is not None
        }
        
        for component, status in components_status.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {component}")
        
        # 2. KI-Modelle testen
        print("\n2. Teste KI-Modelle...")
        if self.ai_manager:
            try:
                model_status = self.ai_manager.get_model_status()
                for model, available in model_status.items():
                    status_icon = "✅" if available else "❌"
                    print(f"   {status_icon} {model}")
            except Exception as e:
                print(f"   ❌ Fehler beim Testen der KI-Modelle: {e}")
        
        # 3. Datenbank-Test (placeholder)
        print("\n3. Teste Datenbank...")
        if self.db_manager:
            print(f"   ℹ️  Datenbank-Status: (Statusabfrage nicht implementiert)")
        else:
            print(f"   ❌ Datenbank nicht initialisiert")
        
        # 4. Ressourcen-Test (real-time CPU/RAM)
        print("\n4. Teste Ressourcen-Monitor...")
        if self.resource_monitor:
            try:
                usage = self.resource_monitor.get_current_resources() if hasattr(self.resource_monitor, 'get_current_resources') else None
                if usage:
                    print(f"   ✅ CPU: {usage.cpu_percent:.1f}%")
                    print(f"   ✅ RAM: {usage.memory_percent:.1f}%")
                else:
                    print(f"   ℹ️  Ressourcen-Status: (Statusabfrage nicht implementiert)")
            except Exception as e:
                print(f"   ❌ Ressourcen-Monitor: Fehler - {e}")
        else:
            print(f"   ❌ Ressourcen-Monitor nicht initialisiert")
        
        # 5. Orchestrator-Test (include agent list)
        print("\n5. Teste Orchestrator...")
        if self.orchestrator:
            try:
                orch_status = self.orchestrator.get_agent_status()
                print(f"   ✅ Autogen verfügbar: {orch_status.get('autogen_available', False)}")
                print(f"   ✅ Agenten initialisiert: {orch_status.get('agents_initialized', 0)}")
                agent_names = orch_status.get('agent_names', [])
                if agent_names:
                    print(f"   🧑‍💻 Agenten-Liste: {', '.join(agent_names)}")
            except Exception as e:
                print(f"   ❌ Orchestrator: Fehler - {e}")
        else:
            print(f"   ❌ Orchestrator nicht initialisiert")
        
        # 6. Zettelkasten-Test (placeholder)
        print("\n6. Teste Zettelkasten...")
        if self.zettel_manager:
            print(f"   ℹ️  Zettelkasten-Status: (Statusabfrage nicht implementiert)")
        else:
            print(f"   ❌ Zettelkasten nicht initialisiert")
        
        print("\n✅ Diagnostik abgeschlossen!")
        
        input("\nDrücke Enter zum Fortfahren...")
    
    def _generate_improvement_suggestions(self):
        """Generiere Verbesserungsvorschläge basierend auf Systemdaten."""
        suggestions = [
            "Erhöhe die Anzahl der verfügbaren KI-Modelle für bessere Diversität",
            "Implementiere erweiterte Zettelkasten-Querverweise",
            "Füge automatische Backup-Funktionen hinzu",
            "Optimiere die Agenten-Kommunikation für schnellere Ergebnisse",
            "Implementiere benutzerdefinierte Organisationsregeln"
        ]
        return suggestions
    
    def option_9_self_improvement(self):
        """Option 9: Self-Improvement & Module Creation."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🛠️ SELF-IMPROVEMENT & MODULE CREATION{Style.RESET_ALL}")
        print("="*60)
        print(f"{Fore.GREEN}The AI can create new modules to extend system capabilities.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}This allows the system to adapt to your specific needs.{Style.RESET_ALL}")
        print("="*60)
        
        try:
            from text.self_improver import QuickSelfImprover
            improver = QuickSelfImprover()
            
            print(f"\n{Fore.YELLOW}Available actions:{Style.RESET_ALL}")
            print("1. Create Research Assistant module")
            print("2. Create custom module")
            print("3. List existing dynamic modules")
            print("4. Run improvement cycle")
            print("0. Back to main menu")
            
            choice = input(f"\n{AGENT_ICONS['User']}{AGENT_COLORS['User']}Choose action: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                print(f"\n{Fore.CYAN}Creating Research Assistant module...{Style.RESET_ALL}")
                result = improver.create_research_assistant_module()
                if result["success"]:
                    print(f"{Fore.GREEN}✅ Research Assistant module created successfully!{Style.RESET_ALL}")
                    if result.get("cli_integrated"):
                        print(f"{Fore.GREEN}✅ Module integrated into CLI menu{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Failed to create module: {result.get('error', 'Unknown error')}{Style.RESET_ALL}")
                    
            elif choice == "2":
                module_name = input("Module name (e.g., 'data_analyzer'): ").strip()
                purpose = input("Module purpose: ").strip()
                requirements = input("Requirements (comma-separated): ").strip().split(",")
                requirements = [req.strip() for req in requirements if req.strip()]
                
                if module_name and purpose and requirements:
                    print(f"\n{Fore.CYAN}Creating custom module...{Style.RESET_ALL}")
                    result = improver.create_new_module(module_name, purpose, requirements)
                    if result["success"]:
                        print(f"{Fore.GREEN}✅ Custom module created successfully!{Style.RESET_ALL}")
                        
                        # Ask if user wants to integrate into CLI
                        integrate = input("Integrate into CLI menu? (y/n): ").strip().lower()
                        if integrate == 'y':
                            menu_option = input("Menu option text: ").strip()
                            cli_result = improver.integrate_module_into_cli(module_name, menu_option)
                            if cli_result["success"]:
                                print(f"{Fore.GREEN}✅ Module integrated into CLI{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Failed to create module: {result.get('error', 'Unknown error')}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Please provide all required information{Style.RESET_ALL}")
                    
            elif choice == "3":
                modules = improver.list_dynamic_modules()
                if modules:
                    print(f"\n{Fore.CYAN}Dynamic modules:{Style.RESET_ALL}")
                    for name, info in modules.items():
                        print(f"  📦 {name}: {info.get('purpose', 'No description')}")
                        print(f"     Created: {info.get('created', 'Unknown')}")
                        print(f"     CLI integrated: {info.get('cli_integrated', False)}")
                        print()
                else:
                    print(f"{Fore.YELLOW}No dynamic modules found.{Style.RESET_ALL}")
                    
            elif choice == "4":
                print(f"\n{Fore.CYAN}Running improvement cycle...{Style.RESET_ALL}")
                results = improver.run_improvement_cycle()
                print(f"{Fore.GREEN}Improvement cycle completed:{Style.RESET_ALL}")
                for result in results:
                    status_icon = "✅" if result["status"] == "improved" else "⚠️"
                    print(f"  {status_icon} {result['file']}: {result['status']}")
                    
            elif choice == "0":
                return
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}Error in self-improvement system: {e}{Style.RESET_ALL}")
        
        input("\nDrücke Enter zum Fortfahren...")
    
    
    def option_10_research_assistant(self):
        """Option 10: 📚 Research Assistant & Academic Writing"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📚 Research Assistant & Academic Writing{Style.RESET_ALL}")
        print("="*60)
        
        try:
            from b3fileorganizer.core.research_assistant import Research_AssistantManager
            research_assistant_manager = Research_AssistantManager()
            
            # Add your module-specific logic here
            print(f"Module research_assistant loaded successfully")
            
        except Exception as e:
            print(f"{Fore.RED}Error loading research_assistant module: {e}{Style.RESET_ALL}")
        
        input("\nDrücke Enter zum Fortfahren...")


    def option_11_research_assistant(self):
        """Option 11: 📚 Research Assistant & Academic Writing"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📚 Research Assistant & Academic Writing{Style.RESET_ALL}")
        print("="*60)
        
        try:
            from b3fileorganizer.core.research_assistant import Research_AssistantManager
            research_assistant_manager = Research_AssistantManager()
            
            # Add your module-specific logic here
            print(f"Module research_assistant loaded successfully")
            
        except Exception as e:
            print(f"{Fore.RED}Error loading research_assistant module: {e}{Style.RESET_ALL}")
        
        input("\nDrücke Enter zum Fortfahren...")

def run(self):
        """Hauptschleife des Launchers."""
        while True:
            try:
                self.display_header()
                self.display_menu()
                choice = input("\n" + tr("menu_prompt")).strip()
                if choice == "0":
                    print("\n👋 " + tr("goodbye"))
                    break
                elif choice == "1":
                    self.option_1_simple_conversation()
                elif choice == "2":
                    self.option_2_system_dashboard()
                elif choice == "3":
                    self.option_3_multi_agent_organization()
                elif choice == "4":
                    self.option_4_wikipedia_extraction()
                elif choice == "5":
                    self.option_5_advanced_file_analysis()
                elif choice == "6":
                    self.option_6_learning_system()
                elif choice == "7":
                    self.option_7_diagnostics()
                elif choice == "8" or choice.lower() == 'recalibrate':
                    print(tr("recalibrate_warning"))
                    confirm = input(tr("recalibrate_confirm")).strip().lower()
                    if confirm in ['y', 'yes', 'j', 'ja', 's', 'si', 'oui', 'да', 'نعم']:
                        alias, sys_name, answers = onboarding.run_onboarding()
                        self.system_name = sys_name
                        self.alias = alias
                        print(tr("recalibrate_done").replace("{system_name}", sys_name))
                        input(tr("press_enter"))
                    else:
                        print(tr("recalibrate_cancelled"))
                        input(tr("press_enter"))
                elif choice.lower().startswith('language'):
                    parts = choice.split()
                    if len(parts) == 2:
                        set_language(parts[1])
                        print(tr("language_switched").replace("{lang}", parts[1]))
                    else:
                        print(tr("language_usage"))
                    input(tr("press_enter"))
                elif choice.lower() == 'status':
                    self.show_status()
                    input(tr("press_enter"))
                elif choice == "9":
                    self.option_9_self_improvement()
                else:
                    print(tr("invalid_choice"))
            except KeyboardInterrupt:
                print("\n\n" + tr("terminated_by_user"))
                break
            except Exception as e:
                print(f"\n❌ {tr('unexpected_error')}: {e}")
                self.logger.error(f"Launcher-Fehler: {e}")
                input(tr("press_enter"))

def main():
    """Hauptfunktion."""
    try:
        # Onboarding check
        if onboarding.needs_onboarding():
            alias, sys_name, answers = onboarding.run_onboarding()
            first_msg = onboarding.generate_first_message(alias, sys_name, answers)
            print("\n" + first_msg)
        launcher = B3FileOrganizerLauncher()
        launcher.run()
    except Exception as e:
        print(f"\n{Fore.RED}{Style.BRIGHT}FATAL ERROR during startup: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 