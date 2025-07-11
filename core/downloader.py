import os
from .naming import make_gallery_filename, safe_filename
from .metadata import save_metadata
from .history import is_downloaded, mark_downloaded
from utils import ensure_dir, print_err

def download_gallery(gallery_id, config, meta, image_urls):
    dest_dir = config["download_dir"]
    filename = make_gallery_filename(meta, config)
    out_path = os.path.join(dest_dir, filename + ".cbz")
    ensure_dir(dest_dir)
    if is_downloaded(gallery_id, config):
        print(f"[SKIP] Already downloaded: {gallery_id}")
        return
    # TODO: Download images, create CBZ, save metadata
    # (Stub; see core/downloader.py full implementation later)
    mark_downloaded(gallery_id, config)
    print(f"[DONE] Saved: {out_path}")