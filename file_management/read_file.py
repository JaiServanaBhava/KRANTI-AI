import os
from backend.app.voice_recognition.voice_feedback import speak, get_input

def read_file():
    try:
        speak("What file do you want me to read?")
        name = get_input()

        speak("Where is it located?")
        location = get_input()

        path = os.path.join(os.path.expanduser("~"), location.capitalize(), name)

        if not os.path.exists(path):
            speak("File not found.")
            return

        with open(path, 'r') as f:
            content = f.read()
            speak("Reading file content now.")
            speak(content[:1000])  # limit reading to first 1000 chars
    except Exception as e:
        speak(f"Could not read file. Error: {e}")
