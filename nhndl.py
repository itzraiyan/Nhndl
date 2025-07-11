#!/usr/bin/env python3
import sys
from ui.tui import NhndlTUI
from config import load_config

def main():
    config = load_config()
    tui = NhndlTUI(config)
    tui.run()

if __name__ == "__main__":
    main()
