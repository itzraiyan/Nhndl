import re

def safe_filename(name, max_len=150):
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    if len(name) > max_len:
        name = name[:max_len].rstrip()
    return name

def make_gallery_filename(meta, config):
    tpl = config.get("filename_template", "{id} - {title}")
    title = meta.get("title", meta.get("id", "unknown"))
    title = safe_filename(title, config.get("max_filename_len", 150))
    return tpl.format(id=meta.get("id"), title=title)