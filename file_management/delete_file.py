import os
import subprocess
from backend.app.voice_recognition.voice_feedback import speak, get_input

def delete_file(command):
    try:
        name = command.replace("delete", "").strip()
        speak("Where is the file or folder located?")
        location = get_input().lower()

        if "don't know" in location:
            subprocess.run(["explorer", "/select,", name])
            return

        search_paths = [
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.join(os.path.expanduser("~"), "Downloads"),
            os.path.join(os.path.expanduser("~"), "Documents"),
            os.path.expanduser("~")
        ]

        for base in search_paths:
            for root, dirs, files in os.walk(base):
                all_items = files + dirs
                matches = [item for item in all_items if os.path.splitext(item)[0] == name]

                if len(matches) > 1:
                    speak(f"I found multiple matches for {name}")
                    for i, match in enumerate(matches):
                        speak(f"{i+1}: {match}")
                    speak("Which one should I delete?")
                    choice = get_input().strip()
                    try:
                        match = matches[int(choice) - 1]
                    except:
                        speak("Invalid choice.")
                        return
                elif matches:
                    match = matches[0]
                else:
                    continue

                full_path = os.path.join(root, match)
                if os.path.isdir(full_path):
                    os.rmdir(full_path)
                else:
                    os.remove(full_path)
                speak(f"{match} deleted from {root}")
                return

        speak("File not found.")
    except Exception as e:
        speak(f"Error while deleting: {e}")

