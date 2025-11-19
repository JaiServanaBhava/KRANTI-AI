# backend/app/wifi_status.py

import subprocess
import platform
import time
import threading
from backend.app.voice_recognition.voice_feedback import speak


def get_wifi_name():
    """Get current Wi-Fi SSID (network name)."""
    system = platform.system()

    if system == "Windows":
            output = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"], encoding="utf-8"
            )
            for line in output.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()

    return "Unknown"
   


def get_wifi_status():
    """Return Wi-Fi connection status (connected/disconnected, SSID, signal)."""
    
    wifi_name = get_wifi_name()

    if wifi_name == "Not connected":
            return "You are not connected to any Wi-Fi network."

    system = platform.system()
    signal_strength = "unknown"

    if system == "Windows":
            output = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"], encoding="utf-8"
            )
            for line in output.split("\n"):
                if "Signal" in line:
                    signal_strength = line.split(":")[1].strip()
                    break

    return f"You are connected to Wi-Fi '{wifi_name}' with signal strength {signal_strength}."

   


def speak_wifi_status():
    """Speak Wi-Fi status aloud."""
    msg = get_wifi_status()
    speak(msg)
    return msg


# ----------------- Background Monitor ----------------- #

def wifi_monitor(interval=60):
    """Background Wi-Fi monitor (checks every `interval` seconds)."""
    last_status = None
    while True:
        status = get_wifi_status()
        if status != last_status:  # only notify on change
            speak(status)
            last_status = status
        time.sleep(interval)


def start_wifi_monitor(interval=60):
    """Start Wi-Fi monitor in a background thread."""
    thread = threading.Thread(target=wifi_monitor, args=(interval,), daemon=True)
    thread.start()
