cat > README.txt << 'EOL'
DOCKER DOWNLOAD ORGANIZER
=========================

Auto-organizes your Downloads folder into categorized subfolders. Dockerized for easy setup.

QUICK START
-----------
git clone https://github.com/hjj672/dor.git
cd dor
docker-compose up -d

WHAT IT ORGANIZES
-----------------
- Videos: .mp4, .mov, .avi, .mkv
- Images: .jpg, .png, .gif, .webp
- Documents: .pdf, .docx, .xlsx, .txt
- Archives: .zip, .rar, .tar.gz
- Scripts: .sh, .py, .js
- Audio: .mp3, .wav, .ogg
- Executables: .exe, .deb, .appimage
- +10 more categories - fully customizable

MANAGEMENT
----------
# Start/Stop
docker-compose up -d
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

CUSTOMIZE
---------
Edit organizer.py to add file types:

FILE_CATEGORIES = {
    "YourCategory": [".ext1", ".ext2"],
}

NEED HELP?
----------
Check logs: docker-compose logs
Ensure Docker is installed
Modify docker-compose.yml for custom paths

---
Works on Windows, Mac, Linux | No Python setup required
EOL
