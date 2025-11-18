import queue
import sounddevice as sd
import json
import requests
import os
from dotenv import load_dotenv  

from backend.app.voice_recognition.vosk_model_loader import get_recognizer
from backend.app.voice_recognition.voice_feedback import speak, get_input

# ----------------- Load Environment ----------------- #
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"
API_URL = os.getenv("GEMINI_API_URL") or f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

# ----------------- VOSK ASR ----------------- #
rec = get_recognizer()
q = queue.Queue()

def callback(indata, frames, time_info, status):
    q.put(bytes(indata))

# ----------------- Gemini API Integration ----------------- #
def send_to_gemini(text):
    if not API_KEY:
        return "❌ Gemini API key missing. Add GEMINI_API_KEY in .env."

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": text}]}
        ]
    }

    try:
        response = requests.post(f"{API_URL}?key={API_KEY}",
                                 json=payload, headers=headers)
        data = response.json()
        print("[Gemini Raw Response]", json.dumps(data, indent=2))

        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "⚠️ Empty response from Gemini.")

        return "⚠️ No valid response from Gemini."

    except requests.exceptions.RequestException as e:
        print(f"[Gemini API Error] {e}")
        try:
            print("[Gemini Error Response]", response.text)
        except:
            pass
        return "❌ Error communicating with Gemini."

# ----------------- Main Loop ----------------- #
if __name__ == "__main__":
    user_text = get_input("Hello! Please say something...")

    if user_text:
        print(f"[User Input] {user_text}")
        response_text = send_to_gemini(user_text)

        print(f"[Gemini Response] {response_text}")

        speak("Gemini replied:")
        speak(response_text)
        speak(f"Processing your input: {user_text}")

    else:
        speak("Sorry, I couldn't understand your speech.")
        print("[ASR] No valid input detected.")
