import hashlib
import json
import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.tokyo-cusharaboushi.jp/"
STATE_FILE = "state.json"

def fetch():
    r = requests.get(URL, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text()

def load():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def notify(msg):
    print(msg)  # ←まずはログだけ

def main():
    text = fetch()
    h = hashlib.sha256(text.encode()).hexdigest()

    state = load()

    if state.get("hash") != h:
        if "hash" in state:
            notify("更新あり！")
        else:
            notify("初回保存")

        save({"hash": h})
    else:
        notify("更新なし")

if __name__ == "__main__":
    main()
