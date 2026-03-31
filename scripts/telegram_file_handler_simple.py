#!/usr/bin/env python3
"""
Telegram File Handler - упрощённая версия без async
Сохраняет файлы в ~/Изображения/TelegramPics/
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error
import urllib.parse

# Настройка логирования
os.makedirs('/home/picoclaw/.picoclaw/logs', exist_ok=True)
os.makedirs('/home/picoclaw/.picoclaw/data', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/picoclaw/.picoclaw/logs/telegram_files.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "7877727829:AAHhH04F7EXBiUTRglZME4csW2SsnV5cvqM"
SAVE_DIR = Path("/home/picoclaw/Изображения/TelegramPics")
LAST_UPDATE_FILE = Path("/home/picoclaw/.picoclaw/data/telegram_last_update.txt")
PID_FILE = Path("/home/picoclaw/.picoclaw/data/telegram_handler.pid")

SAVE_DIR.mkdir(parents=True, exist_ok=True)

def api_request(method, params=None):
    """Выполняет запрос к Telegram API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    if params:
        query = urllib.parse.urlencode(params)
        url = f"{url}?{query}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        logger.error(f"API request failed: {e}")
        return {"ok": False, "error": str(e)}

def download_file(file_id, save_path):
    """Скачивает файл из Telegram по file_id"""
    # Получаем file_path
    result = api_request("getFile", {"file_id": file_id})
    if not result.get("ok"):
        logger.error(f"Failed to get file info: {result}")
        return False
    
    file_path = result["result"]["file_path"]
    download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    
    try:
        urllib.request.urlretrieve(download_url, save_path)
        return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return False

def process_updates():
    """Обрабатывает обновления от Telegram"""
    offset = 0
    if LAST_UPDATE_FILE.exists():
        try:
            offset = int(LAST_UPDATE_FILE.read_text().strip()) + 1
        except:
            pass
    
    while True:
        try:
            result = api_request("getUpdates", {"offset": offset, "limit": 100})
            
            if not result.get("ok"):
                logger.error(f"API error: {result}")
                time.sleep(5)
                continue
            
            updates = result.get("result", [])
            
            for update in updates:
                update_id = update["update_id"]
                offset = update_id + 1
                
                message = update.get("message", {})
                chat = message.get("chat", {})
                chat_id = chat.get("id")
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Обрабатываем фото
                if "photo" in message:
                    photos = message["photo"]
                    photo = photos[-1]  # Максимальное качество
                    file_id = photo["file_id"]
                    file_unique_id = photo.get("file_unique_id", "unknown")[:8]
                    
                    file_name = f"photo_{chat_id}_{timestamp}_{file_unique_id}.jpg"
                    save_path = SAVE_DIR / file_name
                    
                    logger.info(f"Downloading photo from chat {chat_id}")
                    if download_file(file_id, str(save_path)):
                        logger.info(f"✅ Photo saved: {save_path}")
                    else:
                        logger.error(f"❌ Failed to save photo")
                
                # Обрабатываем документы
                elif "document" in message:
                    doc = message["document"]
                    file_id = doc["file_id"]
                    file_name = doc.get("file_name")
                    
                    if not file_name:
                        mime_type = doc.get("mime_type", "unknown")
                        ext = mime_type.split("/")[-1] if "/" in mime_type else "bin"
                        file_name = f"doc_{chat_id}_{timestamp}.{ext}"
                    
                    # Делаем имя файла безопасным
                    file_name = "".join(c for c in file_name if c.isalnum() or c in "._- ")
                    save_path = SAVE_DIR / file_name
                    
                    logger.info(f"Downloading document: {file_name}")
                    if download_file(file_id, str(save_path)):
                        logger.info(f"✅ Document saved: {save_path}")
                    else:
                        logger.error(f"❌ Failed to save document")
                
                # Обрабатываем видео
                elif "video" in message:
                    video = message["video"]
                    file_id = video["file_id"]
                    ext = video.get("mime_type", "video/mp4").split("/")[-1]
                    file_name = f"video_{chat_id}_{timestamp}.{ext}"
                    save_path = SAVE_DIR / file_name
                    
                    logger.info(f"Downloading video from chat {chat_id}")
                    if download_file(file_id, str(save_path)):
                        logger.info(f"✅ Video saved: {save_path}")
                    else:
                        logger.error(f"❌ Failed to save video")
                
                # Сохраняем offset
                LAST_UPDATE_FILE.write_text(str(update_id))
            
            time.sleep(2 if updates else 5)  # Чаще проверяем если есть обновления
            
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(10)

def daemonize():
    """Запускает процесс как демон"""
    # Проверяем, не запущен ли уже
    if PID_FILE.exists():
        try:
            old_pid = int(PID_FILE.read_text().strip())
            if os.path.exists(f"/proc/{old_pid}"):
                logger.info(f"Handler already running (PID {old_pid})")
                sys.exit(0)
        except:
            pass
    
    # Двойной fork для создания демона
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        logger.error(f"Fork failed: {e}")
        sys.exit(1)
    
    os.chdir("/home/picoclaw")
    os.setsid()
    os.umask(0)
    
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        logger.error(f"Fork failed: {e}")
        sys.exit(1)
    
    # Сохраняем PID
    PID_FILE.write_text(str(os.getpid()))
    
    # Закрываем стандартные потоки
    sys.stdout.flush()
    sys.stderr.flush()
    
    with open('/dev/null', 'r') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open('/home/picoclaw/.picoclaw/logs/telegram_files.log', 'a+') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        daemonize()
    
    logger.info("=" * 50)
    logger.info("Telegram File Handler started")
    logger.info(f"Save directory: {SAVE_DIR}")
    logger.info("=" * 50)
    
    try:
        process_updates()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        if PID_FILE.exists():
            PID_FILE.unlink()
    except Exception as e:
        logger.exception("Fatal error")
        if PID_FILE.exists():
            PID_FILE.unlink()
        raise

if __name__ == "__main__":
    main()
