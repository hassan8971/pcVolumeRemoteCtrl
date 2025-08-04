import time
import requests
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL, CoInitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ====== Settings ======
VOLUME_URL      = 'https://akordha.ir/volume.php?mode=get'
POLL_INTERVAL   = 3      # seconds
REQUEST_TIMEOUT = 5      # seconds
# ======================

def init_volume_interface():
    """Initialize COM once and return the Master Volume interface"""
    CoInitialize()
    devices   = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume    = cast(interface, POINTER(IAudioEndpointVolume))
    return volume


def set_volume(volume_iface, percent):
    """Set the system volume using the provided volume interface"""
    try:
        level = max(0.0, min(1.0, percent / 100.0))
        volume_iface.SetMasterVolumeLevelScalar(level, None)
        print(f"[+] Volume set to {percent}%")
    except Exception as e:
        print(f"[!] Error in set_volume: {e}")


def get_remote_volume(session):
    """Fetch the volume level from the remote server"""
    try:
        resp = session.get(VOLUME_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        v = data.get('level', None)
        if isinstance(v, int) and 0 <= v <= 100:
            return v
        else:
            print(f"[!] Invalid level in JSON: {data}")
            return None
    except Exception as e:
        print(f"[!] Error fetching volume: {e}")
        return None


def main():
    print("=== Agent starting ===")
    volume_iface = init_volume_interface()
    session = requests.Session()
    last_level = None

    while True:
        try:
            v = get_remote_volume(session)
            if v is not None and v != last_level:
                set_volume(volume_iface, v)
                last_level = v
        except Exception as e:
            # Catch any unexpected exception and continue
            print(f"[!] Unhandled exception in main loop: {e}")
        time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    main()