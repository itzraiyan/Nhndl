import os
import sys
import requests
import shutil
from zipfile import ZipFile
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from .naming import safe_filename

MAX_IMAGE_THREADS = 12

def get_gallery_id(arg):
    arg = arg.strip()
    if arg.startswith('#'):
        arg = arg[1:]
    if arg.isdigit():
        return arg
    import re
    match = re.search(r'nhentai\.net/g/(\d+)', arg)
    if match:
        return match.group(1)
    raise ValueError(f"Invalid nhentai URL or gallery ID: {arg}")

def fetch_gallery_data(gallery_id):
    api_url = f"https://nhentai.net/api/gallery/{gallery_id}"
    try:
        resp = requests.get(api_url, timeout=15)
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}")
        return resp.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch gallery {gallery_id}: {e}")

def get_image_url(media_id, page, page_type):
    ext_map = {"j": "jpg", "p": "png", "g": "gif", "w": "webp"}
    ext = ext_map.get(page_type)
    if not ext:
        raise ValueError(f"Unknown image type: {page_type}")
    return f"https://i.nhentai.net/galleries/{media_id}/{page}.{ext}", ext

def download_image(args):
    idx, media_id, page_type, folder = args
    url, ext = get_image_url(media_id, idx, page_type)
    filename = os.path.join(folder, f"{idx:03d}.{ext}")
    try:
        r = requests.get(url, stream=True, timeout=20)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
            return filename
        else:
            return None
    except Exception:
        return None

def download_images(media_id, pages, folder, threads=MAX_IMAGE_THREADS):
    os.makedirs(folder, exist_ok=True)
    task_args = [(idx, media_id, page['t'], folder) for idx, page in enumerate(pages, 1)]
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(tqdm(executor.map(download_image, task_args), total=len(task_args), desc=f"{Fore.YELLOW}Pages", leave=False, colour="yellow"))
    img_files = [f for f in results if f]
    return img_files

def create_cbz(img_files, outpath):
    try:
        with ZipFile(outpath, 'w') as zipf:
            for img in img_files:
                arcname = os.path.basename(img)
                zipf.write(img, arcname=arcname)
    except Exception as e:
        raise RuntimeError(f"Failed to create cbz: {e}")

def images_to_pdf(img_files, pdf_path):
    try:
        from PIL import Image
        imgs = [Image.open(img).convert("RGB") for img in img_files]
        if imgs:
            imgs[0].save(pdf_path, save_all=True, append_images=imgs[1:])
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to create PDF: {e}")

def clean_folder(folder):
    try:
        shutil.rmtree(folder, ignore_errors=True)
    except Exception:
        pass

def get_cbz_page_count(cbz_path):
    """Returns the number of image files in an existing CBZ archive."""
    try:
        with ZipFile(cbz_path, 'r') as zipf:
            count = len([f for f in zipf.namelist() if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))])
        return count
    except Exception:
        return 0

def download_gallery(arg, dest_dir=None, custom_cbz=None, threads=MAX_IMAGE_THREADS, save_pdf=False):
    try:
        gallery_id = get_gallery_id(arg)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {arg}: {e}")
        return

    try:
        data = fetch_gallery_data(gallery_id)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to fetch {arg}: {e}")
        return

    title = data['title']['english'] or data['title']['japanese'] or gallery_id
    safe_title = safe_filename(title)
    cbz_name = custom_cbz if custom_cbz else f"{safe_title}.cbz"
    cbz_path = os.path.join(dest_dir, cbz_name) if dest_dir else cbz_name

    if len(cbz_path) > 240:
        safe_title = safe_title[:230]
        cbz_name = custom_cbz if custom_cbz else f"{safe_title}.cbz"
        cbz_path = os.path.join(dest_dir, cbz_name) if dest_dir else cbz_name

    media_id = data['media_id']
    pages = data['images']['pages']
    page_count = len(pages)

    # --- Error Handling: Existing File Check ---
    if os.path.exists(cbz_path):
        existing_count = get_cbz_page_count(cbz_path)
        if existing_count == page_count:
            print(f"{Fore.CYAN}[SKIP]{Style.RESET_ALL} {cbz_path} already exists with {existing_count} pages.")
            return
        else:
            print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} File '{cbz_path}' exists with {existing_count} pages, but gallery has {page_count} pages.")
            resp = input(f"Do you want to overwrite the existing file? (y/n): ").strip().lower()
            if resp != 'y':
                print(f"{Fore.LIGHTYELLOW_EX}Skipping download for: {cbz_path}{Style.RESET_ALL}")
                return
            else:
                print(f"{Fore.YELLOW}Overwriting: {cbz_path}{Style.RESET_ALL}")

    tmp_folder = f"tmp_{gallery_id}"

    print(f"{Fore.GREEN}==> Downloading:{Style.RESET_ALL} {Fore.WHITE}{cbz_name}{Style.RESET_ALL} {Fore.MAGENTA}(ID: {gallery_id}){Style.RESET_ALL} - {page_count} pages")
    img_files = download_images(media_id, pages, tmp_folder, threads=threads)
    if not img_files:
        print(f"{Fore.RED}[{gallery_id}] No images downloaded. Possibly network error or gallery removed.{Style.RESET_ALL}")
        clean_folder(tmp_folder)
        return

    try:
        os.makedirs(dest_dir, exist_ok=True)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to create folder: {e}")
        clean_folder(tmp_folder)
        return

    try:
        create_cbz(img_files, cbz_path)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {safe_title}: {e}")
        clean_folder(tmp_folder)
        return

    # PDF export if enabled
    if save_pdf:
        try:
            pdf_path = os.path.join(dest_dir, f"{safe_title}.pdf") if dest_dir else f"{safe_title}.pdf"
            images_to_pdf(img_files, pdf_path)
            print(f"{Fore.LIGHTGREEN_EX}Saved as PDF: {pdf_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} PDF export failed: {e}")

    clean_folder(tmp_folder)
    print(f"{Fore.LIGHTGREEN_EX}Saved as: {cbz_path}{Style.RESET_ALL}\n")