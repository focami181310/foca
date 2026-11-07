import os

MARKER_FILE = "last_run_failed.marker"

def previous_run_crushed():
    if os.path.exists(MARKER_FILE):
        return True
    else:
        return False

def create_crash_marker(module_name, function):
    with open(MARKER_FILE, "w") as f:
        f.write(f"failed in {module_name}. In {function}")

def remove_crash_marker():
    if os.path.exists(MARKER_FILE):
        os.remove(MARKER_FILE)
        