# B3FileOrganizer GUI - Requires 'b3_icon.ico' or 'b3_icon.png' in the project directory for window icon.
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon

# --- Backend imports ---
from core.ai_manager import AIManager
from utils.conversation_logger import ConversationLogger
from core.resource_monitor import ResourceMonitor
from core.onboarding import ONBOARDING_QUESTIONS
import json
from utils.i18n import tr

HINT_TEXT = (
    """
B3FileOrganizer GUI - Quick Hints

- Each panel is an independent terminal:
  1. Main User Terminal: Chat with the AI (Alpha, Beta, Gamma, Delta), ask questions, or run commands. On first run, onboarding/setup will start here.
  2. Agent Collaboration Terminal: See and interact with agent-to-agent conversations and workflows. Type /refresh to reload logs.
  3. System Control/Status Terminal: View system specs, logs, diagnostics, and run control commands. Type /status or /refresh for live stats.

- Type in any panel's input box and press Enter to send a command or message.
- Panel commands (type in input box):
    /export   - Export panel content to a .txt file
    /clear    - Clear panel content
    /status   - (System panel) Show system status
    /refresh  - (Agent/System panel) Refresh logs/status
- Most commands can be written in natural language; the AI will interpret and act.
- Example commands:
    organize X/         # Organize files in folder X/
    status              # Show system status
    extract wikipedia   # Start Wikipedia knowledge extraction
    help                # Show available commands
    agent Beta          # Switch to Beta agent
- Tab cycles only between the three input boxes (not buttons).
- For more help, see the README or documentation.
"""
)

RETRO_FONT = QFont("VT323, Perfect DOS VGA 437, Courier New, Consolas, monospace", 13)

USER_PROFILE_PATH = "config/user_profile.json"

class TerminalPanel(QWidget):
    def __init__(self, title, parent=None, input_handler=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.input_handler = input_handler
        layout = QVBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #00FF00; background: #000; font-weight: bold;")
        self.title_label.setFont(RETRO_FONT)
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("background: #000; color: #00FF00;")
        self.text_area.setFont(RETRO_FONT)
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type here and press Enter...")
        self.input_box.setStyleSheet("background: #000; color: #00FF00;")
        self.input_box.setFont(RETRO_FONT)
        layout.addWidget(self.title_label)
        layout.addWidget(self.text_area)
        layout.addWidget(self.input_box)
        self.setLayout(layout)
        self.setStyleSheet("background: #000; border: 2px solid #111;")
        self.input_box.returnPressed.connect(self.handle_input)

    def handle_input(self):
        text = self.input_box.text().strip()
        if not text:
            return
        if self.input_handler:
            self.input_handler(text, self)
        self.input_box.clear()

    def append(self, msg):
        self.text_area.append(msg)

    def clear_panel(self):
        self.text_area.clear()

    def export_panel(self):
        content = self.text_area.toPlainText()
        if not content:
            return
        fname, _ = QFileDialog.getSaveFileName(self, "Export Panel Content", "panel.txt", "Text Files (*.txt)")
        if fname:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(content)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("B3 Archivar")
        self.resize(1200, 600)
        # Set window icon (always prefer .ico if present)
        icon_path = None
        if os.path.exists("b3_icon.ico"):
            icon_path = "b3_icon.ico"
        elif os.path.exists("b3_icon.png"):
            icon_path = "b3_icon.png"
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))
        # --- Backend instances ---
        self.ai_manager = AIManager()
        self.conversation_logger = ConversationLogger()
        self.resource_monitor = ResourceMonitor()
        self.resource_monitor.start_monitoring()
        # --- GUI Layout ---
        central = QWidget()
        main_layout = QVBoxLayout()
        # Black header bar for hint button
        header = QWidget()
        header.setStyleSheet("background: #000; border: none;")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        self.hint_btn = QPushButton("Hint")
        self.hint_btn.setStyleSheet("background: #222; color: #00FF00; font-weight: bold;")
        self.hint_btn.setFont(RETRO_FONT)
        self.hint_btn.clicked.connect(self.show_hint)
        header_layout.addWidget(self.hint_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        # Add a minimalist title label for branding
        self.brand_label = QLabel("B3 Archivar")
        self.brand_label.setStyleSheet("color: #00FF00; background: #000; font-weight: bold; font-size: 18px;")
        self.brand_label.setFont(RETRO_FONT)
        header_layout.addWidget(self.brand_label, alignment=Qt.AlignmentFlag.AlignLeft)
        header.setLayout(header_layout)
        main_layout.addWidget(header)
        # Panels: Agent Collab (left), Main User (center), System Control (right)
        panel_layout = QHBoxLayout()
        self.panel_agent = TerminalPanel("Agent Collaboration Terminal", input_handler=self.handle_agent_input)
        self.panel_user = TerminalPanel("Main User Terminal (AI Conversation)", input_handler=self.handle_user_input)
        self.panel_system = TerminalPanel("System Control/Status Terminal", input_handler=self.handle_system_input)
        panel_layout.addWidget(self.panel_agent)
        panel_layout.addWidget(self.panel_user)
        panel_layout.addWidget(self.panel_system)
        main_layout.addLayout(panel_layout)
        central.setLayout(main_layout)
        self.setCentralWidget(central)
        self.setStyleSheet("background: #000; border: 2px solid #111;")
        self.setFont(RETRO_FONT)
        # Set tab order: only cycle between input boxes
        self.setTabOrder(self.panel_agent.input_box, self.panel_user.input_box)
        self.setTabOrder(self.panel_user.input_box, self.panel_system.input_box)
        self.setTabOrder(self.panel_system.input_box, self.panel_agent.input_box)
        # Onboarding state
        self.onboarding_active = False
        self.onboarding_index = 0
        self.onboarding_answers = {}
        self.check_onboarding()

    def show_hint(self):
        QMessageBox.information(self, "B3FileOrganizer - Hint", HINT_TEXT)

    def check_onboarding(self):
        if not os.path.exists(USER_PROFILE_PATH):
            self.onboarding_active = True
            self.panel_user.clear_panel()
            self.panel_user.append("Welcome to B3FileOrganizer! Let's set up your profile.")
            self.onboarding_index = 0
            self.onboarding_answers = {}
            self.ask_next_onboarding_question()

    def ask_next_onboarding_question(self):
        if self.onboarding_index < len(ONBOARDING_QUESTIONS):
            q = ONBOARDING_QUESTIONS[self.onboarding_index]
            # Use translation if available, fallback to prompt
            prompt = tr(q['key']) if tr(q['key']) != q['key'] else q['prompt']
            self.panel_user.append(f"Q{self.onboarding_index+1}: {prompt}")
        else:
            # Save profile with correct structure
            answers = {q['key']: self.onboarding_answers.get(q['key'], '') for q in ONBOARDING_QUESTIONS}
            profile = {
                "user_info": {"alias": "", "language": "en"},
                "onboarding_answers": answers,
                "system_name": "B3 Archivar",
                "metadata": {"profile_complete": True}
            }
            os.makedirs(os.path.dirname(USER_PROFILE_PATH), exist_ok=True)
            with open(USER_PROFILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
            self.panel_user.append("\nOnboarding complete! Your profile is saved.")
            self.onboarding_active = False
            self.panel_user.append("You can now chat with the AI or use any command.")

    # --- Panel Handlers ---
    def handle_user_input(self, text, panel):
        if self.onboarding_active:
            # Save answer and ask next question
            q = ONBOARDING_QUESTIONS[self.onboarding_index]
            self.onboarding_answers[q['key']] = text
            self.onboarding_index += 1
            self.ask_next_onboarding_question()
            return
        if text.lower() == '/clear':
            panel.clear_panel()
            return
        if text.lower() == '/export':
            panel.export_panel()
            return
        # AI conversation
        panel.append(f"> {text}")
        try:
            response = self.ai_manager.generate_response(text)
        except Exception as e:
            response = f"[AI Error] {e}"
        panel.append(f"<AI>: {response}")
        # Log conversation
        try:
            conv_id = self.conversation_logger.start_conversation("gui_user", ["User", "AI"])
            self.conversation_logger.log_message(conv_id, "User", text)
            self.conversation_logger.log_message(conv_id, "AI", response)
        except Exception as e:
            panel.append(f"[Log Error] {e}")

    def handle_agent_input(self, text, panel):
        if text.lower() == '/clear':
            panel.clear_panel()
            return
        if text.lower() == '/export':
            panel.export_panel()
            return
        if text.lower() == '/refresh':
            # Show latest agent conversations
            try:
                recent = self.conversation_logger.get_recent_conversations(limit=5)
                panel.clear_panel()
                for conv in recent:
                    conv_data = conv.get('conversation', {})
                    panel.append(f"[{conv_data.get('timestamp', '')}] {', '.join(conv_data.get('participants', []))}")
                    for msg in conv.get('messages', []):
                        panel.append(f"  {msg.get('sender', '')}: {msg.get('content', '')}")
                    panel.append("-")
            except Exception as e:
                panel.append(f"[Agent Log Error] {e}")
            return
        panel.append(f"> {text}")

    def handle_system_input(self, text, panel):
        if text.lower() == '/clear':
            panel.clear_panel()
            return
        if text.lower() == '/export':
            panel.export_panel()
            return
        if text.lower() in ['/status', '/refresh']:
            try:
                summary = self.resource_monitor.get_resource_summary()
                current = summary.get('current', {})
                panel.clear_panel()
                panel.append(f"CPU: {current.get('cpu_percent', 0):.1f}%")
                panel.append(f"RAM: {current.get('memory_percent', 0):.1f}%")
                panel.append(f"Available: {current.get('memory_available_gb', 0):.2f} GB")
                for drive, usage in current.get('disk_usage', {}).items():
                    panel.append(f"Disk {drive}: {usage:.1f}%")
            except Exception as e:
                panel.append(f"[Status Error] {e}")
            return
        panel.append(f"> {text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(RETRO_FONT)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())