import json
import os
from typing import List, Optional

HISTORY_FILE = "history.json"


def load_history() -> List[dict]:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_poll(poll_data: dict) -> None:
    history = load_history()
    # Replace if same poll_id exists, else append
    for i, p in enumerate(history):
        if p.get("poll_id") == poll_data.get("poll_id"):
            history[i] = poll_data
            break
    else:
        history.append(poll_data)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_poll(poll_id: str) -> Optional[dict]:
    for p in load_history():
        if p.get("poll_id") == poll_id:
            return p
    return None
