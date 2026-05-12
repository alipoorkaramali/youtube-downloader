```markdown
# 🎬 YouTube & SoundCloud Auto Downloader (GitHub Actions)

[![GitHub release](https://img.shields.io/github/v/release/alipoorkaramali/youtube-SoundCloud-downloader)](https://github.com/alipoorkaramali/youtube-SoundCloud-downloader/releases/latest)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/alipoorkaramali/youtube-SoundCloud-downloader/.github/workflows/Multi-Platform%20Downloader-auto%F0%9F%94%90.yml?label=Auto%20Downloads)](https://github.com/alipoorkaramali/youtube-SoundCloud-downloader/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A fully automated, secure, and self‑hosted downloader for **YouTube** and **SoundCloud** that runs on **GitHub Actions**. It fetches new audio from an RSS‑like log, decrypts your cookies on‑the‑fly, downloads the media, stores it in the repository, and automatically cleans up files older than 24 hours.

> **🔐 Security first** – Your cookies are never stored in plain text. They are encrypted with GPG, and only the decryption key is kept as a GitHub secret.

---

## ✨ Features

- **Automatic & manual modes** – Trigger downloads via a scheduled workflow or on demand.
- **Multi‑platform** – Supports YouTube (audio) and SoundCloud (audio).
- **Encrypted cookies** – `cookies.txt` is encrypted as `cookies.txt.gpg`; decryption happens inside the runner using a secret key.
- **No storage conflicts** – Each download folder maintains its own time‑record file (`upload_times_<folder>.txt`).
- **Automatic clean‑up** – Files older than 24 hours are deleted automatically (auto mode only).
- **Smart duplicate prevention** – Uses both URL hashes and titles to avoid re‑downloading the same content.
- **Release integration** – Small files (< 90 MB) are attached to the “latest” release for easy download.
- **Retry mechanism** – Git pushes retry up to 5 times to solve concurrency conflicts.

---

## 🚀 Quick Start

### 1. Prerequisites

- A **GitHub account** – the workflow runs on GitHub Actions (free tier).
- A **GitHub repository** (private or public) – this project.
- Your **cookies** from YouTube (and optionally SoundCloud) in Netscape format (the same format that `yt-dlp` expects).

> How to export cookies:
> - Use a browser extension like [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) (Chrome) or [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) (Firefox).
> - Export the cookies for `youtube.com` and save as `cookies.txt`.

### 2. Repository setup

Clone the repository (or use it as a template):

```bash
git clone https://github.com/alipoorkaramali/youtube-SoundCloud-downloader.git
cd youtube-SoundCloud-downloader
```

### 3. Encrypt your cookies

Install **GPG** and **OpenSSL** on your local machine (or inside Termux / WSL / Linux):

```bash
# Install tools (Ubuntu/Debian)
sudo apt update && sudo apt install gnupg openssl -y
```

Generate a strong random key and **save it securely** (you will need it as a GitHub secret):

```bash
openssl rand -base64 24
# Example output: dGhpcyBpcyBhbiBleGFtcGxlIGtleSBmb3IgMjQgYnl0ZXM=
```

Encrypt your `cookies.txt` using that key:

```bash
gpg --symmetric --batch --yes \
    --passphrase "your_generated_key_here" \
    --cipher-algo AES256 cookies.txt
```

Now remove the plaintext cookie file:

```bash
rm cookies.txt
```

Add the encrypted file to your repository:

```bash
git add cookies.txt.gpg .gitignore
git commit -m "Add encrypted cookies file"
git push origin main
```

> Make sure `.gitignore` contains `cookies.txt` – this prevents accidental commits of the plaintext cookie.

### 4. Add the decryption secret to GitHub

- Go to your repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.
- **Name:** `COOKIE_DECRYPT_KEY`
- **Secret:** paste the random key you generated earlier.
- Click **Add secret**.

### 5. Prepare Python helpers

Ensure the following Python scripts are present in the repository root (they are already part of this repo):

- `check_and_trigger.py` – reads the log and dispatches auto downloads.
- `record_upload_time.py` – records upload timestamps per folder.
- `cleanup_audio.py` – removes files older than 24 hours (used in auto mode).

No extra configuration is needed – they will automatically use folder‑specific record files (e.g., `upload_times_audio_downloads.txt`).

### 6. Workflow files

The repository contains two workflow files inside `.github/workflows/`:

| File | Purpose |
|------|---------|
| `Multi-Platform Downloader-auto🔐.yml` | **Automatic mode** – triggered by `check_log.yml` or manually. Downloads audio only, cleans up after 24 h. |
| `Multi-Platform Downloader-costume🔐.yml` | **Manual mode** – you can choose video/audio and any folder. No automatic clean‑up. |
| `check_log.yml` | Periodically (every 10 minutes) checks the RSS log and triggers the auto downloader for new items. |

All workflow files already include the decryption step and the retry logic for Git pushes.

---

## 📥 How to Use

### Automatic (scheduled) downloads

- The `check_log.yml` workflow runs every 10 minutes.
- It reads the log from `https://raw.githubusercontent.com/alipoorkaramali/youtube-news-watcher/main/logs/new_videos.txt`
- For each new YouTube URL, it dispatches the **auto downloader** with `folder=audio_downloads`.
- Files are saved in `audio_downloads/`.
- Older files are automatically removed after 24 hours.

### Manual downloads (via GitHub UI)

1. Go to the **Actions** tab of your repository.
2. Select the workflow **`🎬🎵🔐👋 NEW2-costume-Multi-Platform Downloader`**.
3. Click **Run workflow**.
4. Fill in the parameters:
   - `platform`: `youtube` or `soundcloud`
   - `url`: full video/audio URL
   - `format`: `video` or `audio` (video only for YouTube/SoundCloud if available)
   - `folder`: custom folder name (default `downloads`)
5. Click **Run workflow** – the download starts immediately and the file will appear in the specified folder.

### Downloading the result

- All downloaded files are committed directly to the repository inside the chosen folder.
- Small files (single file < 90 MB) are also attached to the **latest release** – you can download them from `https://github.com/alipoorkaramali/youtube-SoundCloud-downloader/releases/tag/latest`.
- Large video files are automatically split into ZIP parts (90 MB each) and stored in the repository.

---

## 🔒 Security Overview

| Component | How it is protected |
|-----------|----------------------|
| Plaintext `cookies.txt` | Never stored in the repository. |
| Encrypted `cookies.txt.gpg` | Stored in the repository, but can only be decrypted with the secret key. |
| Decryption key `COOKIE_DECRYPT_KEY` | Stored as a GitHub **secret** – never exposed in logs (if handled carefully). |
| GitHub Actions runner | Decrypts the cookie on‑the‑fly into a temporary file, uses it for `yt-dlp`, and never commits it. |

> **Important:** Even if someone forks your public repository, they cannot decrypt `cookies.txt.gpg` without the secret key.

---

## 🛠️ Customisation & Troubleshooting

### Changing the log source

Edit `check_and_trigger.py` and update the `LOG_URL` variable.

### Modifying clean‑up age

In `cleanup_audio.py`, change the line `cutoff = now - timedelta(hours=24)` to any other value (e.g., `hours=48`).

### Adding more folders

The scripts automatically create separate record files for each folder. You can use any folder name.

### Concurrency errors (Git push rejected)

The auto workflow includes a **retry loop** (5 attempts, 10 seconds delay). If you still see `rejected` errors, increase `MAX_RETRIES` inside the workflow file.

### Workflow fails at decryption step

- Make sure `cookies.txt.gpg` exists in the root of your repository.
- Verify that the `COOKIE_DECRYPT_KEY` secret matches exactly the key used for encryption.
- Check that `gpg` is installed (the runner’s Ubuntu image includes it by default).

### Manual downloads do not clean up old files

That’s intentional – only the auto workflow (`folder=audio_downloads`) triggers the 24‑hour cleanup.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 💬 Support & Contributing

- For bugs or feature requests, please [open an issue](https://github.com/alipoorkaramali/youtube-SoundCloud-downloader/issues).
- Pull requests are welcome – keep the code clean and respect the existing structure.

**Enjoy your automated downloads!** 🎧
