from ui.banner import show_banner
from ui.colors import c
from core.search import search_nhentai
from core.downloader import download_gallery
import re
import os
from config import NHNDL_HOME, NHNDL_DOWNLOADS, NHNDL_CONFIG, save_config, load_config, ensure_dirs

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

def show_template_help():
    print(c("cyan", "\n--- Filename Template Help ---"))
    print(c("yellow", "You can use the following placeholders:"))
    print(c("white", "{id}       - Gallery ID"))
    print(c("white", "{title}    - English title (fallback Japanese/title if not available)"))
    print(c("white", "{media_id} - NHentai media ID (for images)"))
    print(c("white", "{pages}    - Number of pages"))
    print(c("white", "{language} - Language tag (e.g. english, japanese)"))
    print(c("white", "{ext}      - File extension (cbz/pdf)"))
    print(c("yellow", "Example: {id} - {title} [{language}]"))
    print("")

def settings_menu(config):
    while True:
        print(c("yellow", f"\n--- Settings --- (All settings/config/history are stored in {NHNDL_HOME})"))
        print(c("cyan", f"1. Download Directory: {config['download_dir']}"))
        print(c("cyan", f"2. Threads: {config['threads']}"))
        print(c("cyan", f"3. Filename Template: {config['filename_template']}"))
        print(c("cyan", f"4. Max Filename Length: {config['max_filename_len']}"))
        print(c("cyan", f"5. Output Format: {config.get('output_format', 'cbz')}"))
        print(c("cyan", f"6. Show filename template help"))
        print(c("cyan", f"7. Save and return to main menu"))
        choice = input(c("magenta", "Choose option (1-7): ")).strip()
        if choice == "1":
            new_dir = input("Enter new download directory: ").strip()
            if new_dir:
                config['download_dir'] = os.path.expanduser(new_dir)
        elif choice == "2":
            val = input("Enter max thread count: ").strip()
            if val.isdigit():
                config['threads'] = int(val)
        elif choice == "3":
            new_tpl = input("Enter new filename template (type 'help' for options): ").strip()
            if new_tpl.lower() == "help":
                show_template_help()
            elif new_tpl:
                config['filename_template'] = new_tpl
        elif choice == "4":
            val = input("Enter max filename length: ").strip()
            if val.isdigit():
                config['max_filename_len'] = int(val)
        elif choice == "5":
            print(c("yellow", "Choose output format:"))
            print(c("white", "1. CBZ only"))
            print(c("white", "2. PDF only"))
            print(c("white", "3. Both CBZ and PDF"))
            fmt = input("Format (1/2/3): ").strip()
            if fmt == "1":
                config['output_format'] = "cbz"
            elif fmt == "2":
                config['output_format'] = "pdf"
            elif fmt == "3":
                config['output_format'] = "both"
        elif choice == "6":
            show_template_help()
        elif choice == "7":
            save_config(config)
            print(c("green", f"Settings saved to {NHNDL_CONFIG}. Returning to main menu."))
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
        ensure_dirs()
        # Always use the default if missing or blank
        if not self.config.get('download_dir'):
            self.config['download_dir'] = NHNDL_DOWNLOADS
        else:
            self.config['download_dir'] = os.path.expanduser(self.config['download_dir'])

    def run(self):
        show_banner()
        print(c("cyan", "Welcome to NHNDL! (Termux friendly)\n"))
        while True:
            choice = main_menu()
            if choice == "1":
                user_input = input(c("red", "Enter URLs/IDs (comma/space/newline separated): "))
                entries = parse_multiple_inputs(user_input)
                for entry in entries:
                    download_gallery(
                        entry,
                        dest_dir=self.config.get("download_dir"),
                        threads=self.config.get("threads", 12),
                        output_format=self.config.get("output_format", "cbz"),
                        filename_template=self.config.get("filename_template", "{id} - {title}"),
                        max_filename_len=self.config.get("max_filename_len", 150)
                    )
            elif choice == "2":
                while True:
                    selected_ids = search_nhentai()
                    if selected_ids:
                        for gid in selected_ids:
                            download_gallery(
                                gid,
                                dest_dir=self.config.get("download_dir"),
                                threads=self.config.get("threads", 12),
                                output_format=self.config.get("output_format", "cbz"),
                                filename_template=self.config.get("filename_template", "{id} - {title}"),
                                max_filename_len=self.config.get("max_filename_len", 150)
                            )
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