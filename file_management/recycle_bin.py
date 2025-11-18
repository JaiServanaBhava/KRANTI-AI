import send2trash 
from backend.app.voice_recognition.voice_feedback import speak

def bin(path):
      send2trash.send2trash(path) 
      speak("Moved to recycle bin successfully")
