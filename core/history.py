import json
import os
from config import NHNDL_HISTORY, ensure_dirs

def is_downloaded(gallery_id, config):
    hist = _load_history(config)
    return str(gallery_id) in hist

def mark_downloaded(gallery_id, config):
    hist = _load_history(config)
    hist[str(gallery_id)] = True
    _save_history(hist, config)

def _load_history(config):
    ensure_dirs()
    f = config.get("history_file", NHNDL_HISTORY)
    if not os.path.exists(f):
        return {}
    try:
        with open(f, "r", encoding="utf-8") as fp:
            return json.load(fp)
    except Exception:
        return {}

def _save_history(hist, config):
    ensure_dirs()
    f = config.get("history_file", NHNDL_HISTORY)
    try:
        with open(f, "w", encoding="utf-8") as fp:
            json.dump(hist, fp)
    except Exception:
        pass