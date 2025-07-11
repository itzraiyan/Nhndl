from ui.banner import show_banner
from ui.colors import c
from core.search import search_nhentai
from core.downloader import download_gallery

class NhndlTUI:
    def __init__(self, config):
        self.config = config

    def run(self):
        show_banner()
        print(c("cyan", "Welcome to NHNDL! (Termux friendly)\n"))
        while True:
            print(c("yellow", "Enter nhentai URL/ID, 'search', or 'exit':"))
            user = input(c("red", "Nhndl> ")).strip()
            if not user or user.lower() in {"exit", "quit", "q"}:
                print(c("green", "Goodbye!"))
                break
            elif user.lower().startswith("search"):
                selected_ids = search_nhentai()
                if selected_ids:
                    for gid in selected_ids:
                        download_gallery(gid, dest_dir=self.config.get("download_dir"))
                continue
            else:
                # Assume it's a direct download
                gid = user
                download_gallery(gid, dest_dir=self.config.get("download_dir"))