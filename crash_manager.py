import os
from message_worker import add_message

user_name = os.getenv("USER_NAME")

MARKER_FILE = "last_run_failed.marker"

NORMAL_MESSAGE = f"{user_name} инициализировал попытку запустить мост..."
CRASH_MESSAGE = f"{user_name} инициализировал попытку запустить мост... Прошлая попытка не удалась..."

def previous_run_crashed():
    if os.path.exists(MARKER_FILE):
        return True
    else:
        return False

def create_crash_marker():
    with open(MARKER_FILE, "w") as f:
        f.write(f"Last time program ended without user's command")

def crash_check_set():
    did_crash = previous_run_crashed()
    create_crash_marker()

    if did_crash:
        print("Мост: Попытка запустить мост... Прошлая попытка не удалась...")
        add_message("user", "Мост", CRASH_MESSAGE)
    else:
        print("Мост: Попытка запустить мост...")
        add_message("user", "Мост", NORMAL_MESSAGE)

def crash_check_remove():
    if os.path.exists(MARKER_FILE):
        os.remove(MARKER_FILE)