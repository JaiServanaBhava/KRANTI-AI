import time
import threading
import psutil
from plyer import notification
import winsound

class USBWatcher:
    def __init__(self, speak_callback=None):
        """
        speak_callback: optional function (e.g. your assistant's speak)
        """
        self.previous_devices = set(self.get_connected_devices())
        self.speak = speak_callback
        self.running = False

    def get_connected_devices(self):
        """Return list of connected removable drives (USBs)."""
        devices = []
        partitions = psutil.disk_partitions(all=False)
        for p in partitions:
            if 'removable' in p.opts or 'cdrom' in p.opts:
                devices.append(p.device)
        return devices

    def alert(self, title, message):
        """Show alert and optionally speak."""
        # Popup
        notification.notify(
            title=title,
            message=message,
            app_name="Kranti Assistant",
            timeout=4
        )
        # Sound
        winsound.Beep(1000, 500)
        # Voice
        if self.speak:
            self.speak(message)

    def start(self):
        """Start monitoring USB insert/removal."""
        if self.running:
            return
        self.running = True
        threading.Thread(target=self.monitor, daemon=True).start()

    def stop(self):
        """Stop monitoring."""
        self.running = False

    def monitor(self):
        """Monitor loop."""
        while self.running:
            current_devices = set(self.get_connected_devices())

            inserted = current_devices - self.previous_devices
            removed = self.previous_devices - current_devices

            for dev in inserted:
                self.alert("🔌 USB Inserted", f"Drive {dev} connected.")

            for dev in removed:
                self.alert("❌ USB Removed", f"Drive {dev} disconnected.")

            self.previous_devices = current_devices
            time.sleep(2)  # check every 2 seconds


# Example usage
if __name__ == "__main__":
    watcher = USBWatcher()
    watcher.start()
    print("🔍 USB Watcher running... Press Ctrl+C to stop.")
    while True:
        time.sleep(1)
