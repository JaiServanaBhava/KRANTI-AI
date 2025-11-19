import psutil
import threading
import time
from plyer import notification  # pip install plyer
from backend.app.voice_recognition.voice_feedback import speak


def notify(title, message):
    """Show Windows notification"""
    notification.notify(
        title=title,
        message=message,
        timeout=10  # seconds
    )

def check_battery():
    """Background thread that checks battery every 5 minutes"""
    while True:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged

            if percent < 15 and not plugged:
                msg = f"Battery low, {percent}% left. Please plug in the charger."
                speak(msg)
                notify("Battery Alert ⚡", msg)
            if percent < 30 and not plugged:
                msg = f"Battery low, {percent}% left. Please plug in the charger."
                speak(msg)
                notify("Battery Alert ⚡", msg)
        
        time.sleep(300)  # 5 minutes

# Start background thread
battery_thread = threading.Thread(target=check_battery, daemon=True)
battery_thread.start()

def get_battery_status():
    """Return current battery percentage"""
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plugged = "charging" if battery.power_plugged else "not charging"
        return f"Battery is at {percent}% and currently {plugged}."
    else:
        return "Sorry, I cannot access the battery information."
