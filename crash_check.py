import os

MARKER_FILE = "last_run_failed.marker"

def previous_run_crashed():
    if os.path.exists(MARKER_FILE):
        return True
    else:
        return False

def create_crash_marker():
    with open(MARKER_FILE, "w") as f:
        f.write(f"Last time program ended without user's command")

def remove_crash_marker():
    if os.path.exists(MARKER_FILE):
        os.remove(MARKER_FILE)
        