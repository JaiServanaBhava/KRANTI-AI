import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QComboBox, QLabel
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QObject
# NOTE: The deep_translator library must be installed: pip install deep-translator
from deep_translator import GoogleTranslator 

# --- Signal Class to Safely Update GUI from Worker Thread ---
class TranslatorSignals(QObject):
    """Signals available from a worker thread to update the main GUI thread."""
    translation_finished = pyqtSignal(str)
    translation_error = pyqtSignal(str)

# --- Worker Thread to Handle Translation (Non-Blocking) ---
class TranslationWorker(threading.Thread):
    def __init__(self, signals, text, src, dest):
        super().__init__()
        self.signals = signals
        self.text = text
        self.src = src
        self.dest = dest
        self.daemon = True # Allows the application to exit even if the thread is running

    def run(self):
        try:
            # The actual translation work
            translated = GoogleTranslator(source=self.src, target=self.dest).translate(self.text)
            self.signals.translation_finished.emit(translated)
        except Exception as e:
            self.signals.translation_error.emit(str(e))


class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌐 Kranti Translator")
        self.setGeometry(300, 200, 700, 500)
        self.setStyleSheet("""
            QWidget { background-color: #1e1e1e; color: #ffffff; }
            QLabel { color: #aaaaaa; }
            QTextEdit { background-color: #2d2d30; border: 1px solid #555555; padding: 10px; }
            QComboBox { background-color: #3e3e42; color: #ffffff; padding: 5px; border-radius: 3px; }
            QPushButton { 
                background-color: #007ACC; 
                color: white; 
                padding: 10px; 
                border-radius: 5px; 
                border: none;
            }
            QPushButton:hover { background-color: #008cd7; }
        """)

        # Fonts
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        text_font = QFont("Segoe UI", 12)

        # Layouts
        main_layout = QVBoxLayout()
        lang_layout = QHBoxLayout()
        text_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()

        # Title
        title = QLabel("🌐 KRANTI TRANSLATOR")
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #7AA2F7; margin-bottom: 10px;")
        main_layout.addWidget(title)

        # Language dropdowns
        self.source_lang = QComboBox()
        self.target_lang = QComboBox()
        self.source_lang.setFont(text_font)
        self.target_lang.setFont(text_font)

        # Updated Language List
        LANGS = {
            "Auto Detect": "auto", "English": "en", "Hindi": "hi", "Marathi": "mr",
            "French": "fr", "Spanish": "es", "German": "de", "Chinese (Simplified)": "zh-cn",
            "Japanese": "ja", "Russian": "ru", "Portuguese": "pt", "Korean": "ko"
        }

        for name, code in LANGS.items():
            self.source_lang.addItem(name, code)
            self.target_lang.addItem(name, code)

        self.source_lang.setCurrentText("Auto Detect")
        self.target_lang.setCurrentText("Hindi")

        lang_layout.addWidget(QLabel("FROM:"))
        lang_layout.addWidget(self.source_lang, 3) # Weight 3
        lang_layout.addWidget(QLabel("TO:"))
        lang_layout.addWidget(self.target_lang, 3) # Weight 3

        # Text boxes
        self.input_box = QTextEdit()
        self.input_box.setFont(text_font)
        self.input_box.setPlaceholderText("✍️ Enter text here...")
        self.input_box.setFixedHeight(250)
        self.input_box.setFocusPolicy(Qt.StrongFocus) # Ensure it captures focus

        self.output_box = QTextEdit()
        self.output_box.setFont(text_font)
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("🔄 Translation will appear here...")
        self.output_box.setFixedHeight(250)
        self.output_box.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)

        text_layout.addWidget(self.input_box)
        text_layout.addWidget(self.output_box)

        # Buttons
        self.translate_btn = QPushButton("🚀 Translate")
        self.translate_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.translate_btn.clicked.connect(self.do_translate)
        
        self.clear_btn = QPushButton("🧹 Clear All")
        self.clear_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.clear_btn.clicked.connect(self.clear_text)
        self.clear_btn.setStyleSheet("background-color: #DA3633; color: white; padding: 10px; border-radius: 5px;")
        self.clear_btn.setObjectName("clear_button") # Use object name for unique styling if needed

        btn_layout.addWidget(self.translate_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.setSpacing(20)

        # Add layouts to main
        main_layout.addLayout(lang_layout)
        main_layout.addLayout(text_layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)
        
        # Initialize signals
        self.signals = TranslatorSignals()
        self.signals.translation_finished.connect(self.handle_translation_result)
        self.signals.translation_error.connect(self.handle_translation_error)

    def handle_translation_result(self, translated_text):
        """Called by the worker thread signal upon success."""
        self.output_box.setPlainText(translated_text)
        self.translate_btn.setEnabled(True)
        self.translate_btn.setText("🚀 Translate")

    def handle_translation_error(self, error_message):
        """Called by the worker thread signal upon error."""
        self.output_box.setPlainText(f"❌ Translation failed:\n{error_message}")
        self.translate_btn.setEnabled(True)
        self.translate_btn.setText("🚀 Translate")

    def do_translate(self):
        text = self.input_box.toPlainText().strip()
        if not text:
            self.output_box.setPlainText("⚠️ Please enter text to translate.")
            return

        src = self.source_lang.currentData()
        dest = self.target_lang.currentData()

        self.translate_btn.setEnabled(False)
        self.translate_btn.setText("Translating...")
        self.output_box.setPlainText("Processing translation...")

        # Start the network operation in a separate thread
        worker = TranslationWorker(self.signals, text, src, dest)
        worker.start()

    def clear_text(self):
        self.input_box.clear()
        self.output_box.clear()


if __name__ == '__main__':
    # This block executes when the file is run directly.
    # We remove the old 'translator()' function wrapper and the faulty 'elif' block.
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())