from ui.banner import show_banner
from ui.colors import c
from core.search import search_nhentai
from core.downloader import download_gallery
from core.downloader import parse_multiple_inputs  # Import for reuse in batch txt
import re
import os
from config import NHNDL_HOME, NHNDL_DOWNLOADS, NHNDL_CONFIG, save_config, load_config, ensure_dirs

def show_batch_txt_guide():
    print(c("cyan", "\n--- Batch Download from TXT Guide ---"))
    print(c("yellow", "How to organize your download list:"))
    print(c("yellow", "• Each single entry (gallery ID, #ID, or URL) goes on its own line."))
    print(c("yellow", "• To start a group (folder), leave a blank line, then write '>> Folder Name' on a new line."))
    print(c("yellow", "  Add any entries you want in that group below it, one per line."))
    print(c("yellow", "• To start more single entries or another group, leave another blank line."))
    print(c("yellow", "• Lines starting with # are ignored (comments)."))
    print(c("yellow", "• Always use a blank line to switch between singles and groups, or between groups."))
    print(c("yellow", "• Place your .txt file in your Nhndl folder or give its full path."))
    print(c("yellow", "• You can use or edit the default list at ~/Nhndl/list.txt.\n"))

    print(c("yellow", "Example:"))
    print(c("white", "  123456"))
    print(c("white", "  #123456"))
    print(c("white", "  https://nhentai.net/g/789012"))
    print(c("white", ""))  # Blank line to start a group
    print(c("white", "  >> My Series"))
    print(c("white", "  111111"))
    print(c("white", "  222222"))
    print(c("white", "  333333"))
    print(c("white", ""))  # Blank line to start more singles
    print(c("white", "  555555"))
    print(c("white", "  666666"))
    print(c("white", ""))  # Another blank line to start another group
    print(c("white", "  >> Other Stuff"))
    print(c("white", "  777777"))
    print(c("white", "  888888"))

    print(c("cyan", "\nTip: Always use a blank line to switch between single entries and groups, or to start a new group."))
    print(c("cyan", "Need help finding your file path? See 'Advanced Tips' below."))

    print(c("magenta", "\n--- Advanced Tips (optional) ---"))
    print(c("yellow", "• To get the full path of your file:"))
    print(c("white", "  Linux/Termux: realpath yourfile.txt"))
    print(c("white", "  Windows: Shift+Right-click the file, then 'Copy as path'"))

def ensure_default_list_txt():
    """Create ~/Nhndl/list.txt if it doesn't exist."""
    path = os.path.join(NHNDL_HOME, "list.txt")
    if not os.path.exists(path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("# Your NHNDL batch download list\n")
                f.write("# Add one gallery ID or URL per line. Lines starting with # are ignored.\n")
                f.write("# Leave a blank line to separate singles and groups.\n")
                f.write("123456\n#123456\nhttps://nhentai.net/g/789012\n\n")
                f.write(">> My Series\n111111\n222222\n333333\n\n")
                f.write("555555\n666666\n\n")
                f.write(">> Other Stuff\n777777\n888888\n")
            print(c("green", f"\nCreated default list.txt at {path}. Edit this file to add or remove galleries anytime!\n"))
        except Exception as e:
            print(c("red", f"[ERROR] Could not create default list.txt: {e}"))

def main_menu():
    print(c("cyan", "What do you want to do?"))
    print(c("yellow", "1. Download by URLs/IDs"))
    print(c("yellow", "2. Search and download"))
    print(c("yellow", "3. Batch download from TXT"))
    print(c("yellow", "4. Settings"))
    print(c("yellow", "5. Exit"))
    return input(c("magenta", "Choice: ")).strip()

class NhndlTUI:
    def __init__(self, config):
        self.config = config
        ensure_dirs()
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
                show_batch_txt_guide()
                ensure_default_list_txt()
                print(c("magenta", f"\nYou can edit {os.path.join(NHNDL_HOME, 'list.txt')} to manage your downloads."))
                print(c("magenta", "Or, enter the path to another .txt file if you want to use a different list."))
                print(c("yellow", "(Leave blank to use the default list.txt in your NHNDL home directory.)"))
                path = input(c("magenta", "Enter path to your .txt file: ")).strip()
                if not path:
                    path = os.path.join(NHNDL_HOME, "list.txt")
                if not os.path.exists(path):
                    print(c("red", f"[ERROR] File does not exist: {path}"))
                    continue
                singles, series = parse_batch_txt(path)
                # Download singles
                for entry in singles:
                    download_gallery(
                        entry,
                        dest_dir=self.config.get("download_dir"),
                        threads=self.config.get("threads", 12),
                        output_format=self.config.get("output_format", "cbz"),
                        filename_template=self.config.get("filename_template", "{id} - {title}"),
                        max_filename_len=self.config.get("max_filename_len", 150)
                    )
                # Download series (in subfolders)
                for series_name, entries in series.items():
                    folder = os.path.join(self.config.get("download_dir"), safe_folder(series_name))
                    os.makedirs(folder, exist_ok=True)
                    for entry in entries:
                        download_gallery(
                            entry,
                            dest_dir=folder,
                            threads=self.config.get("threads", 12),
                            output_format=self.config.get("output_format", "cbz"),
                            filename_template=self.config.get("filename_template", "{id} - {title}"),
                            max_filename_len=self.config.get("max_filename_len", 150)
                        )
                print(c("green", "Batch download complete."))
            elif choice == "4":
                settings_menu(self.config)
            elif choice == "5":
                print(c("green", "Goodbye!"))
                break
            else:
                print(c("red", "Invalid choice. Try again."))

def safe_folder(name, max_len=80):
    import re
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    if len(name) > max_len:
        name = name[:max_len].rstrip()
    return name

def parse_batch_txt(txt_path):
    singles = []
    series = {}
    mode = "singles"
    group_name = None
    current_entries = []

    def flush_block():
        nonlocal current_entries, mode, group_name
        if mode == "singles" and current_entries:
            singles.extend(current_entries)
        elif mode == "group" and group_name and current_entries:
            if group_name not in series:
                series[group_name] = []
            series[group_name].extend(current_entries)
        current_entries = []
        group_name = None
        mode = "singles"

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    flush_block()
                    continue
                if line.startswith(">>"):
                    flush_block()
                    group_name = line[2:].strip()
                    mode = "group"
                else:
                    current_entries.append(line)
            # Flush any remaining block at EOF
            flush_block()
    except Exception as e:
        print(c("red", f"[ERROR] Could not read TXT: {e}"))
    return singles, series