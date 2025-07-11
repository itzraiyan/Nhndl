import json
import os

def is_downloaded(gallery_id, config):
    hist = _load_history(config)
    return str(gallery_id) in hist

def mark_downloaded(gallery_id, config):
    hist = _load_history(config)
    hist[str(gallery_id)] = True
    _save_history(hist, config)

def _load_history(config):
    f = config.get("history_file")
    if not os.path.exists(f):
        return {}
    try:
        with open(f, "r", encoding="utf-8") as fp:
            return json.load(fp)
    except Exception:
        return {}

def _save_history(hist, config):
    f = config.get("history_file")
    try:
        with open(f, "w", encoding="utf-8") as fp:
            json.dump(hist, fp)
    except Exception:
        pass