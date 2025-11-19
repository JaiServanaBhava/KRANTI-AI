import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.voice_recognition.voice_feedback import speak

def log_action(command):
    """Logs an action."""
    action = command.replace("log", "").strip()
    speak(f"Logging action: {action}")
    # Placeholder for actual logging logic
    return f"Logged: {action}"
