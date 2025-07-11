import os
import sys
import platform

def is_termux():
    # Crude check for Termux
    return "com.termux" in os.environ.get("PREFIX", "")

def ensure_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass

def print_err(msg):
    print(msg, file=sys.stderr)