import os

HISTORY_FILE = "posted_urls.txt"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return set()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_to_history(url):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{url}\n")

def is_posted(url):
    history = load_history()
    return url in history
