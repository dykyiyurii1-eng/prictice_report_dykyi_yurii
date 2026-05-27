from .save_data import *
import json
from datetime import datetime
from pathlib import Path


def load_history() -> list:
    Path(history_file).parent.mkdir(parents=True, exist_ok=True)
    if not Path(history_file).exists():
        return []
    with open(history_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_to_history(action: str, name: str):
    history = load_history()
    history.append({
        "action": action,
        "name": name,
        "time": datetime.now().strftime("%d.%m.%Y %H:%M"),
    })
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def clear_history():
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump([], f)