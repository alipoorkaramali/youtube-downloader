# 🎬🎵 دانلودر خودکار یوتیوب و ساندکلاد با آپلود مستقیم به Mega.nz

[![GitHub release](https://img.shields.io/github/v/release/alipoorkaramali/youtube-SoundCloud-downloader)](https://github.com/alipoorkaramali/youtube-SoundCloud-downloader/releases/latest)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/alipoorkaramali/youtube-SoundCloud-downloader/.github/workflows/Multi-Platform-Downloader-auto-Mega.yml)](https://github.com/alipoorkaramali/youtube-SoundCloud-downloader/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

یک سیستم **کاملاً خودکار، امن و بدون نیاز به سرور اختصاصی** برای دانلود ویدیو و صوت از **یوتیوب و ساندکلاد** و آپلود مستقیم به **ابر شخصی Mega.nz** – تماماً درون GitHub Actions اجرا می‌شود.

---

## ✨ قابلیت‌های کلیدی

- **دانلود خودکار** از یوتیوب و ساندکلاد با چک کردن لاگ (RSS-like) هر ۱۰ دقیقه.
- **دانلود دستی** با انتخاب ویدیو یا صوت، کیفیت، و پوشه دلخواه.
- **آپلود مستقیم به Mega.nz** – فایل‌ها هرگز در مخزن گیت‌هاب ذخیره نمی‌شوند.
- **تقسیم فایل به ZIP‌های چندبخشی** (اختیاری) – باز کردن قطعات در ویندوز با WinRAR یا 7‑Zip به سادگی یک دوبار کلیک است.
- **کش کردن rclone و yt-dlp** – سرعت اجرای مجدد بسیار بالاست.
- **جلوگیری از دانلود تکراری** – بررسی همزمان هش لینک، عنوان اصلی و عنوان نرمالایز شده.
- **امنیت کامل** – کوکی‌ها و تنظیمات مگا با GPG رمزگذاری می‌شوند و فقط درون رانر رمزگشایی می‌گردند.
- **بازیابی آسان در صورت قطعی اینترنت** – فایل‌های قدیمی با پسوند `.old` غیرفعال شده‌اند اما در مواقع ضروری قابل بازگشت هستند (توضیح در بخش پایانی).

---

## 🗂 ساختار مخزن (فایل‌های اصلی)

| فایل/پوشه | نقش |
|-----------|------|
| `.github/workflows/Multi-Platform-Downloader-auto-Mega.yml` | **دانلودر خودکار** – اجرا توسط تریگر یا به‌صورت دستی، آپلود به مگا |
| `.github/workflows/Multi-Platform-Downloader-costume-Mega.yml` | **دانلودر دستی** – با گزینه‌های ویدیو/صدا و کیفیت انتخابی |
| `.github/workflows/check_log.yml` | **تریگر خودکار** – هر ۱۰ دقیقه لاگ را چک کرده و ورک‌فلو خودکار را فعال می‌کند |
| `check_and_trigger.py` | اسکریپت پایتون – لاگ را پردازش کرده و لینک‌های جدید را تشخیص می‌دهد |
| `rclone_mega.conf.gpg` | تنظیمات رمزگذاری شده Mega.nz (ایمیل و رمز) |
| `cookies.txt.gpg` | کوکی رمزگذاری شده یوتیوب (برای ویدیوهای خصوصی یا سن‌محدود) |
| `processed.txt`, `processed_titles.txt` | فایل‌های وضعیت – جلوگیری از دانلود تکراری |

> فایل‌های `.old` (مانند `auto_audio_downloader-V1.old`) نسخه‌های قدیمی هستند که غیرفعال شده‌اند. در صورت افتادن اینترنت و نیاز به روش ساده‌تر، می‌توانید پسوند آن‌ها را به `.yml` تغییر دهید.

---

## 🔧 راه‌اندازی (گام به گام)

### 1️⃣ پیش‌نیازها

- یک حساب **GitHub** (رایگان کافی است).
- یک حساب **Mega.nz** (برای ذخیره فایل‌های دانلود شده).
- (اختیاری) کوکی یوتیوب در قالب Netscape – اگر ویدیوی عمومی دانلود می‌کنید نیازی نیست.

### 2️⃣ دریافت مخزن

```bash
git clone https://github.com/alipoorkaramali/youtube-SoundCloud-downloader.git
cd youtube-SoundCloud-downloader
