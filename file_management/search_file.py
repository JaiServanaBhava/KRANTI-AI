import os
import subprocess
from backend.app.voice_recognition.voice_feedback import speak, get_input

def search_file():
    try:
        speak("What file or folder are you looking for?")
        query = get_input().strip().lower()

        user_home = os.path.expanduser("~")

        for root, dirs, files in os.walk(user_home):
            for item in files + dirs:
                if query in item.lower():
                    full_path = os.path.join(root, item)
                    speak(f"Found {item}. Opening location.")
                    subprocess.run(["explorer", "/select,", full_path])
                    return

        speak("No matching file or folder found.")
    except Exception as e:
        speak(f"Search failed: {e}")

