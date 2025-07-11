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
    print(c("yellow", "• Put one gallery ID (123456), #ID (#123456), or full URL (https://nhentai.net/g/123456) per line."))
    print(c("yellow", "• Blank lines or lines beginning with # are ignored."))
    print(c("yellow", "• To group multiple galleries into a series, use lines starting with '>>', like:"))
    print(c("white", "  >> My Series Name"))
    print(c("white", "  123456"))
    print(c("white", "  https://nhentai.net/g/789012"))
    print(c("white", "  #445566"))
    print(c("yellow", "• All galleries under the last '>>' go into a folder named after the series."))
    print(c("yellow", "• Single galleries (not under any '>>') are downloaded normally.\n"))
    print(c("yellow", f"Place your txt file anywhere and enter the full path, or put it in {NHNDL_HOME} for convenience."))
    print(c("cyan", "\n[Tip] How to get the full path of your .txt file:"))
    print(c("yellow", "• On Linux/Termux: Open a new session in your terminal, and use the command:"))
    print(c("white", "  realpath yourfile.txt"))
    print(c("yellow", "  This will print the absolute path, which you can copy and paste when prompted."))
    print(c("yellow", "• On Windows: Right-click the file while holding Shift, then select 'Copy as path'."))
    print(c("green", f"\n[Info] You can keep your main batch list at {os.path.join(NHNDL_HOME, 'list.txt')} and add new downloads by editing it anytime!"))
    print(c("yellow", f"If you create a new file, always make sure it's in your home directory for best compatibility."))

def ensure_default_list_txt():
    """Create ~/Nhndl/list.txt if it doesn't exist."""
    path = os.path.join(NHNDL_HOME, "list.txt")
    if not os.path.exists(path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("# Your NHNDL batch download list\n")
                f.write("# Add one gallery ID or URL per line. Lines starting with # are ignored.\n")
                f.write("# Example:\n")
                f.write("123456\n")
                f.write("https://nhentai.net/g/789012\n")
                f.write(">> My Series\n")
                f.write("112233\n")
                f.write("#445566\n")
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
    current_series = None
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith(">>"):
                    current_series = line[2:].strip()
                    if current_series not in series:
                        series[current_series] = []
                else:
                    if current_series:
                        series[current_series].append(line)
                    else:
                        singles.append(line)
    except Exception as e:
        print(c("red", f"[ERROR] Could not read TXT: {e}"))
    return singles, series