import os
from backend.app.voice_recognition.voice_feedback import speak, get_input

def rename_file(command):
    try:
        speak("What is the current name of the file or folder?")
        current = get_input().strip()

        speak("What should be the new name?")
        new = get_input().strip()

        speak("Where is the file or folder located?")
        location = get_input().lower()

        path = os.path.join(os.path.expanduser("~"), location.capitalize(), current)
        new_path = os.path.join(os.path.expanduser("~"), location.capitalize(), new)

        if os.path.exists(path):
            os.rename(path, new_path)
            speak(f"Renamed {current} to {new}")
        else:
            speak("File not found.")
    except Exception as e:
        speak(f"Rename failed: {e}")
