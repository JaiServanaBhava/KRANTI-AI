import os
import sys
import threading
import queue
import json
import sounddevice as sd
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWebChannel import QWebChannel

# ----------------- Your Existing Imports ----------------- #
from backend.app.voice_recognition.vosk_model_loader import get_recognizer
from backend.app.voice_recognition.voice_feedback import speak
from backend.app.voice_recognition.wake_word_listener import detect_wake_word
from router import route_command
from backend.ai_assistant.fetchSystemInfo import fetchSystemInfo as get_system_info

# ----------------- Global Setup ----------------- #
recognizer = get_recognizer()
q = queue.Queue()


def audio_callback(indata, frames, time, status):
    """Collect mic input into queue"""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def listen_loop():
    """
    Continuous listening loop:
      - Always listens for 'kranti'
      - If active, executes commands
      - 'stop listening' disables commands until 'kranti' is heard again
    """
    listening = False

    with sd.RawInputStream(samplerate=16000, blocksize=8000,
                           dtype="int16", channels=1,
                           callback=audio_callback):

        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower().strip()

                if not text:
                    continue

                print(f"🎙️ Heard: {text}")

                # Wake word
                if "kranti"  in text or "start" in text or "hello" in text  and not listening:
                    listening = True
                    speak("Hello boss, I am listening.What can I do for you?")
                    continue

                # Stop listening
                if "stop listening" in text and listening:
                    listening = False
                    speak("Okay boss, I’ll wait until you call me again.")
                    continue

                # Actively listening → run router
                if listening:
                    if "exit" in text:
                        speak("Okay boss, shutting down. Goodbye!")
                        os._exit(0)

                    response = route_command(text,recognizer)
                    speak("sir I am listening for your next command.")
                    continue
                

class Bridge(QObject):
    newMessage = pyqtSignal(str, str)
   
    @pyqtSlot(result=str)
    def fetchSystemInfo(self):
        info = get_system_info()
        return json.dumps(info)

    def __init__(self, main_window):
        super().__init__()
        self.listening = False
        self.main_window = main_window


    @pyqtSlot(str)
    def sendMessage(self, text):
        print(f"💬 User: {text}")
        response = route_command(text,recognizer)
        if not response:
            response = "Sorry, I didn't understand that."
        self.newMessage.emit("AI", response)

    @pyqtSlot()
    def wakeKranti(self):
        if not self.listening:
            self.listening = True
            threading.Thread(target=lambda: speak("Hello boss, I am listening. What can I do for you?")).start()
            self.main_window.browser.page().runJavaScript(
                'document.getElementById("status").textContent = "Status: Listening";'
            )

# ----------------- GUI Window ----------------- #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kranti AI - Personal Assistant")
        self.setGeometry(100, 100, 1200, 800)
        self.browser = QWebEngineView()  # first, create the browser

        self.channel = QWebChannel()
        self.bridge = Bridge(self)  # pass main window reference
        self.channel.registerObject("bridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)

        # load your HTML frontend
        self.browser.setUrl(QUrl.fromLocalFile(
            os.path.abspath("frontend/index.html")
        ))
        self.setCentralWidget(self.browser)



# ----------------- Entry Point ----------------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- Start remote.py in background ---
    try:
        import subprocess
        subprocess.Popen(
            [sys.executable, "remote.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("Remote control server started.")
    except Exception as e:
        print("Error starting remote.py:", e)

    # --- Start GUI ---
    main_win = MainWindow()
    main_win.show()

    # --- Start listener thread ---
    threading.Thread(target=listen_loop, daemon=True).start()

    print("🧠 Kranti AI started. Say 'kranti' to wake me up.")

    sys.exit(app.exec_())
