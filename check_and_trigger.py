import os
import re
import requests
import hashlib
from pathlib import Path

# ============= تنظیمات =============
LOG_URL = "https://raw.githubusercontent.com/alipoorkaramali/youtube-news-watcher/main/logs/new_videos.txt"
STATE_FILE = "processed.txt"
TITLE_STATE_FILE = "processed_titles.txt"

REPO_OWNER = "alipoorkaramali"
REPO_NAME = "youtube-SoundCloud-downloader"
WORKFLOW_FILE = "Multi-Platform-Downloader-auto-Mega.yml"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

AUTO_FOLDER = "news_downloads"
MEGA_FOLDER = "YoutubeNews"
QUALITY = "best"
SPLIT_CHOICE = "single"
# ==================================

def load_processed_hashes():
    if not Path(STATE_FILE).exists():
        return set()
    with open(STATE_FILE) as f:
        return set(line.strip() for line in f if line.strip())

def save_processed_hashes(hashes):
    with open(STATE_FILE, "w") as f:
        for h in hashes:
            f.write(h + "\n")

def load_processed_items():
    if not Path(TITLE_STATE_FILE).exists():
        return set()
    with open(TITLE_STATE_FILE, encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def add_processed_item(platform: str, title: str):
    key = f"{platform}:{normalize_title(title)}"
    with open(TITLE_STATE_FILE, "a", encoding='utf-8') as f:
        f.write(key + "\n")

def normalize_title(title: str) -> str:
    if not title:
        return ""
    title = re.sub(r'\s*[\(\[].*?[\)\]]\s*', ' ', title)
    title = re.sub(r'(?i)\b(official|video|music|clip|lyrics|hd|4k|full|audio|version|remix)\b', '', title)
    title = re.sub(r'\s+', ' ', title).strip().lower()
    return title

def extract_info(line: str):
    parts = line.split(" | ")
    if len(parts) < 4:
        return None
    platform = parts[1].strip()
    url = parts[-1].strip()
    
    if platform not in ("youtube", "soundcloud"):
        if "youtube.com" in url or "youtu.be" in url:
            platform = "youtube"
        elif "soundcloud.com" in url:
            platform = "soundcloud"
    
    title_parts = parts[2:-1]
    title = " | ".join(title_parts).strip() if title_parts else ""
    return (platform, title, url)

def trigger_download(video_url: str, platform: str, title: str):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "ref": "main",
        "inputs": {
            "platform": platform,
            "url": video_url,
            "type": "audio",
            "quality": QUALITY,
            "folder": AUTO_FOLDER,
            "mega_folder": MEGA_FOLDER,
            "split_choice": SPLIT_CHOICE
        }
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 204:
        print(f"✅ Triggered: {platform} | {title}")
        return True
    else:
        print(f"❌ Failed {platform} | {title} → {resp.status_code}")
        return False

def main():
    resp = requests.get(LOG_URL)
    if resp.status_code != 200:
        print(f"⚠️ Failed to fetch log: {resp.status_code}")
        return

    lines = [line.strip() for line in resp.text.splitlines() if line.strip()]
    processed_hashes = load_processed_hashes()
    processed_items = load_processed_items()
    new_count = 0

    for line in lines:
        info = extract_info(line)
        if not info:
            continue
            
        platform, title, video_url = info
        
        link_hash = hashlib.md5(video_url.encode()).hexdigest()
        if link_hash in processed_hashes:
            continue

        # تشخیص محتوای مشابه بین یوتیوب و ساندکلاد
        norm_title = normalize_title(title)
        if any(existing.split(":", 1)[1] == norm_title for existing in processed_items):
            print(f"⏭️ Similar content already processed: {title}")
            processed_hashes.add(link_hash)
            continue

        print(f"🎯 New: {platform} | {title}")
        
        success = trigger_download(video_url, platform, title)
        
        if success:
            processed_hashes.add(link_hash)
            add_processed_item(platform, title)
            new_count += 1

    save_processed_hashes(processed_hashes)
    print(f"✅ Processed {new_count} new item(s).")

if __name__ == "__main__":
    main()
