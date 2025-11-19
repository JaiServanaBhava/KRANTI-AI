import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.voice_recognition.voice_feedback import speak

def set_airplane_mode(command):
    """Toggles airplane mode."""
    if "on" in command:
        speak("Turning on airplane mode.")
        # Placeholder for actual airplane mode logic
        return "Airplane mode is now on."
    elif "off" in command:
        speak("Turning off airplane mode.")
        # Placeholder for actual airplane mode logic
        return "Airplane mode is now off."
    else:
        speak("You can turn airplane mode on or off.")
        return "You can turn airplane mode on or off."
