import shutil, os
from backend.app.voice_recognition.voice_feedback import speak

def compress_file(path): 
     zip_name = path + ".zip"
     shutil.make_archive(path, 'zip', os.path.dirname(path), os.path.basename(path))
     speak(f"File compressed successfully to {zip_name}")
    

