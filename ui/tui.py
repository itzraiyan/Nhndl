from .banner import show_banner
from .colors import c
from .grid import print_grid
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
                keyword = input("Keyword: ").strip()
                res = search_nhentai(keyword)
                print_grid([f"[{i+1}] {r['title']} (ID: {r['id']})" for i, r in enumerate(res)], cols=1)
                sel = input("Select number to download, or Enter to skip: ").strip()
                if sel.isdigit() and 1 <= int(sel) <= len(res):
                    r = res[int(sel)-1]
                    # TODO: Fetch meta+image_urls from API
                    meta = {"id": r['id'], "title": r['title']}
                    image_urls = [] # fake; fill in later
                    download_gallery(r['id'], self.config, meta, image_urls)
            else:
                # Assume it's a direct download
                gid = user
                # TODO: Fetch meta+image_urls from API
                meta = {"id": gid, "title": gid}
                image_urls = []
                download_gallery(gid, self.config, meta, image_urls)