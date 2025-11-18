import os
import shutil
from backend.app.voice_recognition.voice_feedback import speak, get_input

def move_file():
    try:
        speak("What is the name of the file or folder?")
        name = get_input()

        speak("Where is it currently located?")
        source_loc = get_input()

        speak("Where do you want to move it?")
        dest_loc = get_input()

        base_path = os.path.expanduser("~")
        source_path = os.path.join(base_path, source_loc.capitalize(), name)
        dest_path = os.path.join(base_path, dest_loc.capitalize(), name)

        shutil.move(source_path, dest_path)
        speak(f"{name} moved from {source_loc} to {dest_loc}")
    except Exception as e:
        speak(f"Move failed: {e}")