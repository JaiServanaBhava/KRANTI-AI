import time
import threading
import subprocess
from plyer import notification
from backend.app.voice_recognition.voice_feedback import speak


# Keep last known state of connected devices
connected_devices = set()

def notify(title, message):
    """Windows notification"""
    notification.notify(
        title=title,
        message=message,
        timeout=8
    )

def get_bluetooth_devices():
    """
    Get list of connected Bluetooth devices using PowerShell.
    Works on Windows 10/11.
    """
    try:
        result = subprocess.check_output(
            ["powershell", "-Command",
             "Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -eq 'OK' } | Select-Object -ExpandProperty FriendlyName"],
            text=True
        )
        devices = [line.strip() for line in result.splitlines() if line.strip()]
        return set(devices)
    except Exception:
        return set()

def monitor_bluetooth():
    """Background monitor for new/disconnected devices"""
    global connected_devices
    while True:
        current_devices = get_bluetooth_devices()

        # Newly connected devices
        new = current_devices - connected_devices
        for device in new:
            msg = f"Bluetooth device connected: {device}"
            speak(msg)
            notify("Bluetooth Connected ✅", msg)

        # Disconnected devices
        gone = connected_devices - current_devices
        for device in gone:
            msg = f"Bluetooth device disconnected: {device}"
            speak(msg)
            notify("Bluetooth Disconnected ❌", msg)

        connected_devices = current_devices
        time.sleep(10)  # check every 10 sec

# Start monitor in background
bt_thread = threading.Thread(target=monitor_bluetooth, daemon=True)
bt_thread.start()

def get_status():
    """Return current connected devices as string"""
    devices = get_bluetooth_devices()
    if not devices:
        return "No Bluetooth devices are connected right now."
    return "Currently connected devices are: " + ", ".join(devices)
