import os
from backend.app.voice_recognition.voice_feedback import speak, get_input
import subprocess

def create_file_or_folder(command):
    try:
        type_ = None
        if "folder" in command:
            type_ = "folder"
        elif "file" in command:
            type_ = "file"
        
        if type_ is None:
            speak("Do you want to create a file or a folder?")
            type_ = get_input().lower()
            if "folder" in type_:
                type_ = "folder"
            elif "file" in type_:
                type_ = "file"
            else:
                speak("I didn't understand. Please try again.")
                return

        name_search = command.replace("create", "").replace("file", "").replace("folder", "").strip()
        
        if not name_search:
            speak(f"What should be the name of the new {type_}?")
            name = get_input()
        else:
            name = name_search.strip() 

        if not name:
            speak("I need a name to proceed. Command cancelled.")
            return

        location_keywords = ["desktop", "download", "document"]
        location_found = next((loc for loc in location_keywords if loc in command), None)
        
        if not location_found:
            speak("Where should I create it?")
            location = get_input().lower()
            if "don't know" in location:
                speak("Opening File Explorer for you to decide.")
                subprocess.run(["explorer"])
                return
        else:
            location = location_found

        user_home = os.path.expanduser("~")
        PATH_MAP = {
            "desktop": os.path.join(user_home, "Desktop"),
            "download": os.path.join(user_home, "Downloads"),
            "document": os.path.join(user_home, "Documents"),
        }

        if "desktop" in location:
            path = PATH_MAP["desktop"]
            location_name = "Desktop"
        elif "download" in location:
            path = PATH_MAP["download"]
            location_name = "Downloads"
        elif "document" in location:
            path = PATH_MAP["document"]
            location_name = "Documents"
        else:
            path = os.path.join(user_home, location)
            location_name = location

        os.makedirs(path, exist_ok=True) 

        full_path = os.path.join(path, name)
        
        if type_ == "file":
            open(full_path, 'a').close()
        else:
            os.makedirs(full_path, exist_ok=True)

        speak(f"{type_.capitalize()} {name} created in {location_name}")
        return f"✅ {type_.capitalize()} {name} created successfully in {location_name}."
        
    except Exception as e:
        error_message = f"Failed to create the item. Error: {e}"
        speak(error_message)
        return f"❌ {error_message}"