from ui.banner import show_banner
from ui.colors import c
from core.search import search_nhentai
from core.downloader import download_gallery
import re
import os

def parse_multiple_inputs(input_string):
    # Accepts multiple URLs/IDs (with or without #), comma, space, or newline separated
    items = re.split(r'[\s,]+', input_string)
    cleaned = []
    for item in items:
        item = item.strip()
        if item.startswith("#"):
            item = item[1:]
        if item:
            cleaned.append(item)
    return cleaned

def settings_menu(config):
    while True:
        print(c("yellow", "\n--- Settings ---"))
        print(c("cyan", f"1. Download Directory: {config['download_dir']}"))
        print(c("cyan", f"2. Threads: {config['threads']}"))
        print(c("cyan", f"3. Filename Template: {config['filename_template']}"))
        print(c("cyan", f"4. Max Filename Length: {config['max_filename_len']}"))
        print(c("cyan", f"5. Save as PDF (experimental): {config.get('save_pdf', False)}"))
        print(c("cyan", f"6. Return to main menu"))
        choice = input(c("magenta", "Choose option (1-6): ")).strip()
        if choice == "1":
            new_dir = input("Enter new download directory: ").strip()
            if new_dir:
                config['download_dir'] = os.path.expanduser(new_dir)
        elif choice == "2":
            val = input("Enter max thread count: ").strip()
            if val.isdigit():
                config['threads'] = int(val)
        elif choice == "3":
            new_tpl = input("Enter new filename template (e.g. {id} - {title}): ").strip()
            if new_tpl:
                config['filename_template'] = new_tpl
        elif choice == "4":
            val = input("Enter max filename length: ").strip()
            if val.isdigit():
                config['max_filename_len'] = int(val)
        elif choice == "5":
            val = input("Save downloads as PDF too? (y/n): ").strip().lower()
            config['save_pdf'] = (val == "y")
        elif choice == "6":
            break

def main_menu():
    print(c("cyan", "What do you want to do?"))
    print(c("yellow", "1. Download by URLs/IDs"))
    print(c("yellow", "2. Search and download"))
    print(c("yellow", "3. Settings"))
    print(c("yellow", "4. Exit"))
    return input(c("magenta", "Choice: ")).strip()

class NhndlTUI:
    def __init__(self, config):
        self.config = config

    def run(self):
        show_banner()
        print(c("cyan", "Welcome to NHNDL! (Termux friendly)\n"))
        while True:
            choice = main_menu()
            if choice == "1":
                user_input = input(c("red", "Enter URLs/IDs (comma/space/newline separated): "))
                entries = parse_multiple_inputs(user_input)
                for entry in entries:
                    download_gallery(entry, dest_dir=self.config.get("download_dir"))
            elif choice == "2":
                while True:
                    selected_ids = search_nhentai()
                    if selected_ids:
                        for gid in selected_ids:
                            download_gallery(gid, dest_dir=self.config.get("download_dir"))
                        again = input("Search again? (y/n): ").strip().lower()
                        if again != "y":
                            break
                    else:
                        break
            elif choice == "3":
                settings_menu(self.config)
            elif choice == "4":
                print(c("green", "Goodbye!"))
                break
            else:
                print(c("red", "Invalid choice. Try again."))