# NHNDL: nhentai Batch Downloader 🚀

![NHNDL Banner](https://files.catbox.moe/2yff0e.png)

> **Note:** This project contains AI-generated content. The code, documentation, and features have been shaped with the help of AI tools, but the vision and polish come from the project owner.

---

NHNDL is a beginner-friendly, interactive Python tool for **batch downloading and organizing nhentai galleries**. Whether you want to archive your favorite works, download in bulk, or just enjoy a smooth terminal experience (with extra love for Termux/Android users), NHNDL is here for you!

---

## ✨ Features

* ⚡ **Batch download** nhentai galleries using IDs, URLs, or a flexible `.txt` list
* 📁 **Folder grouping:** Organize downloads into custom-named subfolders
* 🔎 **Interactive search:** Browse and select galleries via keyword search
* 🗃️ **Download as CBZ or PDF** (or both)
* 🧠 **Smart duplicate detection:** Skips already-downloaded galleries
* 📝 **Flexible .txt batch format:** Mix singles and groups, comment lines, blank lines as separators
* 🎨 **Colorful, friendly CLI** with banners and detailed help
* ♻️ **Resumable and robust:** Handles errors, skips, and overwrites gracefully
* 🐍 **Pure Python:** Works on Android (Termux), Linux, and Windows
* 🌱 **No coding required:** Designed for all skill levels

---

## 📦 Installation

### 🟩 Android (Termux) – **Recommended**

1. **Install Termux:**  
   Get [Termux from F-Droid](https://f-droid.org/packages/com.termux/) (recommended) or Google Play.

2. **Set up Termux:**
   ```sh
   pkg update
   pkg upgrade
   pkg install python git
   ```

3. **Get NHNDL:**
   ```sh
   git clone https://github.com/itzraiyan/Nhndl.git
   cd Nhndl
   ```
   _Or download ZIP and extract with a file manager._

4. **Install Python requirements:**
   ```sh
   pip install -r requirements.txt
   ```

5. **You're ready! Just run:**
   ```sh
   python nhndl.py
   ```

---

### 🟦 Linux (Ubuntu/Debian/Fedora/Arch...)

```sh
sudo apt update
sudo apt install python3 python3-pip git
git clone https://github.com/itzraiyan/Nhndl.git
cd Nhndl
pip3 install -r requirements.txt
python3 nhndl.py
```

---

### 🟨 Windows

1. **Install [Python 3.x](https://www.python.org/downloads/) and [Git](https://git-scm.com/download/win)**  
   _(During Python install, check "Add Python to PATH")_

2. **Open Command Prompt or PowerShell**

3. **Get NHNDL:**
   ```bat
   git clone https://github.com/itzraiyan/Nhndl.git
   cd Nhndl
   ```

4. **Install dependencies:**
   ```bat
   pip install -r requirements.txt
   ```

5. **Run NHNDL:**
   ```bat
   python nhndl.py
   ```

---

## ▶️ Usage Guide

When you run `python nhndl.py`, you'll get a menu:

1. **Download by URLs/IDs:** Paste in one or more IDs or nhentai URLs (comma, space, or newline separated).
2. **Search and download:** Search nhentai by keyword, browse pages, select galleries to download.
3. **Batch download from TXT:** Download many galleries and organize them—see below!
4. **Settings:** Change download folder, threads, output format, etc.
5. **Exit**

---

### 🗃️ Batch Download from TXT (with Grouping!)

NHNDL can batch download galleries by reading a `.txt` file. It's super flexible:

- **Singles:** Each gallery ID, #ID, or URL on its own line.
- **Groups (folders):**  
  Leave a blank line, then write `>> Folder Name` on a line, then put IDs/URLs for that group underneath (one per line).
- **Switch between singles and groups with blank lines.**
- **Lines starting with `#` are comments and ignored.**
- **You can mix singles and groups however you like!**

#### Example `list.txt`:

```
123456
# This is a comment
https://nhentai.net/g/789012

>> My Series
111111
222222
333333

555555
666666

>> Other Stuff
777777
888888
```

**Tip:** Edit your main batch list at `~/Nhndl/list.txt` (created for you!), or use any `.txt` file and enter its full path.

**How to get the path of your file:**
- **Linux/Termux:** `realpath yourfile.txt`
- **Windows:** Shift+Right-click the file, then "Copy as path"

---

### 📁 Download Output

- All downloads go to `~/Nhndl/Downloads` by default.
- Grouped galleries are placed in subfolders.
- Each gallery is saved as a `.cbz` (comic book archive), `.pdf`, or both—your choice.
- Metadata (`info.json`) is saved with each gallery.

---

## 📂 Project Structure

```
Nhndl/
├── core/
│   ├── downloader.py    # Downloading, conversion, naming
│   ├── search.py        # Interactive search
│   ├── naming.py        # Safe filenames
│   ├── history.py       # Download history (skip duplicates)
│   ├── metadata.py      # Save info.json for each download
├── ui/
│   ├── tui.py           # Main menu & batch TXT logic
│   ├── banner.py        # Banner art
│   ├── colors.py        # Colored terminal output
│   ├── grid.py          # CLI grid view
├── utils.py             # Misc helpers
├── config.py            # Config & setup
├── nhndl.py             # Entry point
├── requirements.txt     # Python dependencies
├── README.md
```

---

## 💡 Frequently Asked Questions

**Q: Does this work on Android (Termux)?**  
A: Yes! NHNDL is designed to be Termux-friendly.

**Q: Where do my downloads go?**  
A: By default, to `~/Nhndl/Downloads`.

**Q: Can I use my own .txt batch file?**  
A: Yes! Place it anywhere and provide the full path, or use the default `~/Nhndl/list.txt`.

**Q: What formats are supported?**  
A: CBZ (default), PDF, or both. Change in settings.

**Q: Will it skip galleries I've already downloaded?**  
A: Yes—NHNDL tracks downloaded galleries and skips them unless you choose to overwrite.

**Q: Is this safe?**  
A: Downloads are local only. No login required. No data is sent anywhere except to nhentai's public API.

**Q: I got an error!**  
A: Check the error message and try again. For help, open an [issue](https://github.com/itzraiyan/Nhndl/issues) and include details.

**Q: Is this project AI-generated?**  
A: Yes, this README and parts of the code are AI-assisted.

---

## 🛡️ Privacy & Security

- No account or login needed.
- All files saved locally, in your home directory.
- No tracking, no external data storage.

---

## 🤝 Contributing

- Issues and pull requests are welcome!
- Please be respectful and constructive—everyone starts somewhere.

---

## 📜 License

NHNDL is licensed under the [MIT License](LICENSE).

---

## 🌸 Credits & Acknowledgments

- Created by [Zilhazz Arefin](https://github.com/itzraiyan)
- ASCII art and helpful colors to brighten your terminal!

---

## 🛑 Disclaimer

> **This project contains AI-generated content. Use at your own risk, and always review code before running.**

---

**Enjoy NHNDL—your batch nhentai adventures await!**  
*“Even the longest journey begins with a single download.”*