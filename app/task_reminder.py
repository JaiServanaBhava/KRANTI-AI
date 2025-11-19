import re
import threading
import time
from datetime import datetime, timedelta
import pyttsx3

# 🗣 Fallback speak function (you already have your own)
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# 🕒 Extract time and task from user command
def parse_reminder_command(command):
    """
    Extracts reminder task and time from user command like:
    'remind me to call mom in 10 minutes'
    'remind me at 8 pm to study'
    """
    command = command.lower()

    # Pattern for "in X minutes/hours"
    in_time = re.search(r"in (\d+)\s*(minute|minutes|hour|hours)", command)
    at_time = re.search(r"at (\d+)(?::(\d+))?\s*(am|pm)?", command)

    task = ""
    if "remind me to" in command:
        task = command.split("remind me to")[-1].strip()
    elif "remind me" in command:
        task = command.split("remind me")[-1].strip()

    remind_time = None
    if in_time:
        number = int(in_time.group(1))
        unit = in_time.group(2)
        remind_time = datetime.now() + timedelta(
            minutes=number if "minute" in unit else number * 60
        )
    elif at_time:
        hour = int(at_time.group(1))
        minute = int(at_time.group(2) or 0)
        ampm = at_time.group(3)

        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0

        now = datetime.now()
        remind_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if remind_time < now:
            remind_time += timedelta(days=1)

    return task, remind_time


# ⏰ Function to set reminder
def set_reminder(task, remind_time):
    def reminder_thread():
        time_diff = (remind_time - datetime.now()).total_seconds()
        if time_diff > 0:
            time.sleep(time_diff)
        speak(f"🔔 Reminder: {task}")
        print(f"🔔 Reminder: {task}")

    threading.Thread(target=reminder_thread, daemon=True).start()
    return f"Reminder set for '{task}' at {remind_time.strftime('%I:%M %p')}."


# 🎯 Main function to handle command
def reminder_handler(command):
    task, remind_time = parse_reminder_command(command)
    if not task:
        return "⚠️ Please tell what to remind you about."
    if not remind_time:
        return "⚠️ Please tell when to remind you."

    return set_reminder(task, remind_time)