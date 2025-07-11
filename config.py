import os
import json

# All Nhndl files and directories should be inside ~/Nhndl
NHNDL_HOME = os.path.expanduser("~/Nhndl")
NHNDL_DOWNLOADS = os.path.join(NHNDL_HOME, "Downloads")
NHNDL_CONFIG = os.path.join(NHNDL_HOME, "config.json")
NHNDL_HISTORY = os.path.join(NHNDL_HOME, "history.json")

DEFAULT_CONFIG = {
    "download_dir": NHNDL_DOWNLOADS,
    "threads": 12,
    "filename_template": "{id} - {title}",
    "max_filename_len": 150,
    "history_file": NHNDL_HISTORY,
    "color": True,
    "output_format": "cbz"
}

def ensure_dirs():
    os.makedirs(NHNDL_HOME, exist_ok=True)
    os.makedirs(NHNDL_DOWNLOADS, exist_ok=True)

def load_config(path=None):
    ensure_dirs()
    config_path = path or NHNDL_CONFIG
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            config.update(user_cfg)
        except Exception:
            pass
    # Always expand the path if user changed it in config
    config["download_dir"] = os.path.expanduser(config["download_dir"])
    config["history_file"] = os.path.expanduser(config["history_file"])
    return config

def save_config(config, path=None):
    ensure_dirs()
    config_path = path or NHNDL_CONFIG
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception:
        pass