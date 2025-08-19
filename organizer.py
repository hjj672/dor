import os
import shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration from environment variables
DOWNLOADS = os.getenv('DOWNLOADS_DIR', '/app/watch_folder')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# Set up logging
log_file = os.getenv('LOG_FILE', '/app/logs/organizer.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# File categories
FILE_CATEGORIES = {
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".webm"],
    "PDFs": [".pdf"],
    "Archives": [".zip", ".rar", ".tar.gz", ".7z", ".tar", ".gz"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".avif", ".webp", ".bmp"],
    "Scripts": [".sh", ".bash", ".py", ".js", ".rb", ".pl"],
    "Torrents": [".torrent"],
    "Debian_Packages": [".deb"],
    "Documents": [".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt", ".odt", ".ods"],
    "Audio": [".mp3", ".wav", ".ogg", ".flac", ".m4a"],
    "Executables": [".exe", ".msi", ".dmg", ".appimage", ".bin"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "Configs": [".yml", ".yaml", ".json", ".xml", ".conf", ".config"],
    "Code": [".html", ".css", ".js", ".java", ".c", ".cpp", ".h", ".php"]
}

class DownloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        try:
            if not event.is_directory:
                time.sleep(2)  # Wait for file to be fully written
                self.process_file(event.src_path)
                
        except Exception as e:
            logging.error(f"Error processing {event.src_path}: {e}")
    
    def process_file(self, file_path):
        if not os.path.isfile(file_path) or os.path.basename(file_path).startswith('.'):
            return
        
        filename = os.path.basename(file_path)
        
        # Skip partially downloaded files
        if any(filename.endswith(ext) for ext in ['.part', '.crdownload', '.tmp']):
            return
        
        _, file_ext = os.path.splitext(filename)
        file_ext = file_ext.lower()
        
        destination_folder = None
        for category, extensions in FILE_CATEGORIES.items():
            if file_ext in extensions:
                destination_folder = os.path.join(DOWNLOADS, category)
                break
        
        if not destination_folder:
            destination_folder = os.path.join(DOWNLOADS, "Others")
        
        os.makedirs(destination_folder, exist_ok=True)
        
        dest_path = os.path.join(destination_folder, filename)
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                new_filename = f"{base}_{counter}{ext}"
                dest_path = os.path.join(destination_folder, new_filename)
                counter += 1

        shutil.move(file_path, dest_path)
        logging.info(f"Moved: {filename} → {os.path.basename(destination_folder)}")

def organize_existing_files():
    """Organize existing files on startup"""
    logging.info("Organizing existing files in Downloads folder...")
    handler = DownloadHandler()
    
    for filename in os.listdir(DOWNLOADS):
        file_path = os.path.join(DOWNLOADS, filename)
        handler.process_file(file_path)

if __name__ == "__main__":
    try:
        logging.info(f"=== Download Organizer Starting ===")
        logging.info(f"Watching directory: {DOWNLOADS}")
        
        # Check if watch directory exists
        if not os.path.exists(DOWNLOADS):
            logging.error(f"Watch directory {DOWNLOADS} does not exist!")
            exit(1)
        
        # Organize existing files first
        organize_existing_files()
        
        # Start watching for new files
        event_handler = DownloadHandler()
        observer = Observer()
        observer.schedule(event_handler, DOWNLOADS, recursive=False)
        observer.start()
        
        logging.info("🚀 File watcher started successfully")
        logging.info("Press Ctrl+C to stop")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logging.info("Stopping organizer gracefully...")
        observer.stop()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
    finally:
        observer.join()
        logging.info("=== Download Organizer Stopped ===")