import os
import json

DEFAULT_CONFIG = {
    "download_dir": os.path.expanduser("~/Nhndl"),
    "threads": 12,
    "filename_template": "{id} - {title}",
    "max_filename_len": 150,
    "history_file": os.path.expanduser("~/.nhndl_history.json"),
    "color": True
}

def load_config(path=None):
    config = DEFAULT_CONFIG.copy()
    config_path = path or os.path.expanduser("~/.nhndl_config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            config.update(user_cfg)
        except Exception:
            pass
    return config