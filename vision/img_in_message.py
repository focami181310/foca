import base64
import os
import json
from datetime import datetime
from constants import MEMORY_FILES_DIR


def get_current_time():
    current_time = datetime.now()
    return current_time.strftime("%d.%m.%Y %H:%M:%S")


def add_img(role, name, content, path):
    with open(path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    chat_history = json.loads(MEMORY_FILES_DIR.joinpath("chat_history.json").read_text(encoding="utf-8"))

    current_time = get_current_time()

    chat_history.append({
        "role": role,
        "name": name,
        "content": [
                    {"type": "text", "text": f"[{current_time}] - {content}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
    })

    chat_history_json = json.dumps(chat_history, ensure_ascii=False, indent=4)

    (MEMORY_FILES_DIR / "chat_history.json").write_text(chat_history_json, encoding="utf-8")