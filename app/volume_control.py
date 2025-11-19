from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
import re

def set_system_volume(level):
    """
    Sets Windows master volume to a specific percentage (0–100)
    """
    try:
        # Limit range
        level = max(0, min(100, int(level)))

        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume.SetMasterVolume(level / 100, None)
        return f"🔊 Volume set to {level}%"

    except Exception as e:
        return f"⚠️ Error setting volume: {e}"

def extract_volume_level(command: str):
    """
    Extracts the number (volume percentage) from voice command
    Example: 'set volume to 70' → 70
    """
    numbers = re.findall(r'\d+', command)
    if numbers:
        return int(numbers[0])
    return None

def volume_control(command):
    """
    Main function to control volume via text/voice command
    """
    level = extract_volume_level(command)
    if level is not None:
        return set_system_volume(level)
    else:
        return "⚠️ Please say like 'set volume to 50'"
