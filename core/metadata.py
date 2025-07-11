import os
import json

def save_metadata(meta, folder):
    ensure_dir(folder)
    fpath = os.path.join(folder, "info.json")
    try:
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    except Exception:
        pass