import subprocess
import os
from backend.app import battery_status
from backend.app import bluetooth_status
from backend.app.voice_recognition.voice_feedback import speak
import pyautogui
import pyperclip
import time
import webbrowser
import pygetwindow as gw
import sounddevice as sd
import queue
import json
import threading
from backend.ai_assistant.dictate import start_dictation
import backend.file_management as fm
from backend.ai_assistant.Weather import Weather
from backend.app.wifi_status import *
from backend.app.battery_status import *
import requests
from api import send_to_gemini

APP_PATHS = {
    "notepad": r"C:\Windows\System32\notepad.exe",
    "paint": r"C:\Windows\System32\mspaint.exe",
    "wordpad": r"C:\Program Files\Windows NT\Accessories\wordpad.exe",
    "calculator": r"C:\Windows\System32\calc.exe",
    "cmd": r"C:\Windows\System32\cmd.exe",
    "powershell": r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "onenote": r"C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "python": r"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe",
    "program_files": r"C:\Program Files",
    "program_files_x86": r"C:\Program Files (x86)",
}

NOTEPAD_PATH = r"C:\Windows\System32\notepad.exe"

def open_app(command: str):
    APP_PATHS = {
        "notepad": "notepad.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
    }
    for app in APP_PATHS:
        if app in command:
            try:
                focused = False
                try:
                    win = [w for w in gw.getWindowsWithTitle(app.capitalize()) if w.isVisible][0]
                    win.activate()
                    focused = True
                    print(f"🔍 Focused existing {app.capitalize()} window.")
                except Exception:
                    pass
                if not focused:
                    subprocess.Popen(APP_PATHS[app])
                    print(f"🚀 Launched {app.capitalize()}.")
                    time.sleep(1)
                    try:
                        win = [w for w in gw.getWindowsWithTitle(app.capitalize()) if w.isVisible][0]
                        win.activate()
                        print(f"🎯 Re-focused {app.capitalize()} after launch.")
                    except Exception:
                        pass
                if "chrome" in app:
                    try:
                        win = [w for w in gw.getWindowsWithTitle("Chrome") if w.isVisible][0]
                        win.activate()
                        time.sleep(0.3)
                        print("🌐 Chrome focused.")
                    except Exception:
                        pass
                    return f"✅ {app.capitalize()} opened or focused."
                return f"✅ {app.capitalize()} opened or focused."
            except Exception as e:
                return f"❌ Failed to open {app}: {e}"
    return "⚠️ I couldn’t find that app in my list."

def open_notepad_for_dictation(command: str, recognizer):
    app = "notepad"
    try:
        focused = False
        try:
            win = [w for w in gw.getWindowsWithTitle(app.capitalize()) if w.isVisible][0]
            win.activate()
            focused = True
            print(f"🔍 Focused existing {app.capitalize()} window.")
        except Exception:
            pass
        if not focused:
            subprocess.Popen(NOTEPAD_PATH)
            print(f"🚀 Launched {app.capitalize()}.")
            time.sleep(1)
            try:
                win = [w for w in gw.getWindowsWithTitle(app.capitalize()) if w.isVisible][0]
                win.activate()
                print(f"🎯 Re-focused {app.capitalize()} after launch.")
            except Exception:
                pass
        print("🤖 Say 'dictate' to start speaking into Notepad, or 'cancel' to skip.")
        q = queue.Queue()
        def callback(indata, frames, time_, status):
            q.put(bytes(indata))
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    text = json.loads(recognizer.Result()).get("text", "").lower()
                    if not text:
                        continue
                    print("🎙️ You said:", text)
                    if any(word in text for word in ["dictate", "yes", "start", "begin"]):
                        print("🎤 Starting dictation mode...")
                        threading.Thread(
                            target=start_dictation, args=(recognizer,), daemon=True
                        ).start()
                        return "Dictation started."
                    elif any(word in text for word in ["no", "cancel", "stop"]):
                        print("❌ Dictation cancelled.")
                        return "Dictation cancelled."
                    print("🤖 Say 'dictate' or 'cancel'.")
    except Exception as e:
        return f"❌ Failed to handle Notepad dictation: {e}"
    return f"✅ {app.capitalize()} opened."

def route_command(command: str,recognizer):
    command = command.lower()
    if "joke" in command:
        from backend.fun.joke import get_joke
        result = get_joke()
    elif "open notepad" in command or "launch notepad" in command or \
             "start notepad" in command or "open note" in command:
        result = open_notepad_for_dictation(command, recognizer)
    elif "shutdown" in command or "shut down" in command:
        speak("Shutting down your computer.")
        os.system("shutdown /s /t 0")
    elif "restart" in command or "reboot" in command:
        speak("Restarting your system.")
        os.system("shutdown /r /t 0")
    elif "lock" in command:
        speak("Locking the computer.")
        subprocess.call("rundll32.exe user32.dll,LockWorkStation")
    elif "logout" in command or "sign out" in command:
        speak("Logging out.")
        os.system("shutdown /l")
    elif "sleep" in command or "hibernate" in command:
        speak("Putting system to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
    elif "youtube video download" in command or "youtube download" in command or \
             "download youtube video" in command or "video download" in command or \
             "download video" in command:
        from backend.ai_assistant.youtube import download_youtube_video
        result = download_youtube_video()
    elif "weather" in command or "temperature" in command or "forecast" in command:
        from backend.ai_assistant.Weather import Weather
        words = command.split()
        city = "Your City"
        if "in" in words:
            idx = words.index("in")
            if idx + 1 < len(words):
                city = " ".join(words[idx + 1:])
        import threading
        threading.Thread(target=lambda: Weather(city), daemon=True).start()
        result = f"🌦 Showing weather for {city}"
    elif any(word in command for word in [
        "tab", "scroll", "reload", "back", "forward", "bookmark",
        "fullscreen", "history", "downloads"]):
        from backend.ai_assistant.browser_control import browser_control
        result = browser_control(command)
    elif "whatsapp schedule" in command or "schedule message" in command or \
             "whatsapp message" in command or "send whatsapp" in command:
        from backend.ai_assistant.whatapp import open_whatsapp_scheduler
        result = open_whatsapp_scheduler()
    elif "remind me" in command:
        from backend.ai_assistant.reminder import set_reminder
        return set_reminder(command)
    elif "quote" in command or "inspire me" in command or "motivate me" in command:
        from backend.fun.quotes import get_random_quote
        result = get_random_quote()
    elif "send email" in command:
        from backend.ai_assistant.send_email_gui import send_email_gui
        speak("Opening email window, sir. Please fill the details.")
        send_email_gui()
        return "Email window opened."
    elif "battery" in command or "charge" in command:
        result = battery_status.get_battery_status()
    elif "bluetooth" in command or "devices" in command:
        result = bluetooth_status.get_status()
    elif "wifi" in command or "wlan" in command:
        result = speak_wifi_status()
    elif "organize" in command or "clean" in command:
        from backend.ai_assistant.organize import (
            organize_folder,
            organize_shortcut,
        )
        for key in ["downloads", "documents", "desktop", "pictures", "videos", "music"]:
            if key in command:
                result = organize_shortcut(key)
                break
        else:
            if "organize folder" in command:
                path = command.replace("organize folder", "").strip()
                result = organize_folder(path)
            else:
                words = command.split()
                for w in words:
                    if ":" in w or "\\" in w or "/" in w:
                        result = organize_folder(w)
                        break
                else:
                    result = "❌ Please provide a valid folder path."
    elif "clear clipboard" in command or "open my clipboard" in command or "show clipboard" in command or "clipboard history" in command or "show history" in command:
        from backend.app.clipboard_viewer import show_clipboard_window
        speak("Opening your clipboard sir.")
        show_clipboard_window()
        return "Showing clipboard."
    elif "create file" in command or "create folder" in command or "make folder" in command:
        result = fm.create_file_or_folder(command)
    elif "delete" in command:
        result = fm.delete_file(command)
    elif "rename" in command:
        result = fm.rename_file(command)
    elif "read" in command:
        result = fm.read_file(command)
    elif "move" in command:
        result = fm.move_file(command)
    elif "search" in command:
        result = fm.search_file(command)
    elif "translate" in command:
        from backend.app.Translator_App import do_translate
        result = do_translate(command)
    elif "compress" in command:
        result = fm.compress_file(command)
    elif "encrypt" in command:
        result = fm.encrypt_file(command)
    elif "restore" in command or "recycle bin" in command:
        result = fm.bin(command)
    elif "screenshot" in command:
        result = fm.take_screenshot()
    elif "clean temp" in command or "temporary files" in command:
        result = fm.clean_temp()
    elif "large files" in command:
        result = fm.find_large_files("C:\\")
    elif "duplicates" in command or "duplicate files" in command:
        result = fm.find_duplicates("C:\\")
    elif "recent files" in command:
        result = fm.recent_files()
    elif "metadata" in command:
        result = fm.inspect_metadata(command)
    elif "open" in command or "launch" in command or "start" in command:
        result = open_app(command)
    else:
        from backend.ai_assistant.mycommand import handle_personal_reply
        personal_reply = handle_personal_reply(command)
        if personal_reply:
            result = personal_reply
        else:
            try:
                requests.get("https://www.google.com", timeout=3)
                internet = True
            except:
                internet = False
            if internet:
                try:
                    from api import send_to_gemini
                    
                    # CHANGED: Request a single, concise line instead of a single word or short sentence.
                    command += " Respond in one single, concise line, summarizing the answer."
                    
                    full_response = send_to_gemini(command)
                    
                    if isinstance(full_response, str):
                        # Clean up the response, replacing newlines with spaces to enforce one line
                        short_answer = full_response.strip().replace('\n', ' ') 
                        max_length = 100
                        # Truncate and add ellipses if the answer exceeds the max length
                        result = short_answer[:max_length] + '...' if len(short_answer) > max_length else short_answer
                    else:
                        # Fallback for non-string responses
                        result = str(full_response)[:100]
                        
                except Exception as e:
                    result = f"⚠️ Error while fetching answer: {e}"
                    
            else:
                result = "🌐 Internet is disconnected,I cannot fetch online information."
            
    if isinstance(result, str) and result.strip():
        speak(result)
    return result