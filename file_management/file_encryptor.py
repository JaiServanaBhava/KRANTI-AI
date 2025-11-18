from cryptography.fernet import Fernet
from backend.app.voice_recognition.voice_feedback import speak

def generate_key(): 
    return Fernet.generate_key()

def encrypt_file(path, key):
    try: 
        fernet = Fernet(key) 
        with open(path, 'rb') as file: 
            original = file.read()
            encrypted = fernet.encrypt(original)
            with open(path, 'wb') as encrypted_file: 
                encrypted_file.write(encrypted) 
                speak("File encrypted successfully")
    except Exception as e:
          speak(f"Encryption failed. Error: {str(e)}")
