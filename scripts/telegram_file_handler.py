#!/usr/bin/env python3
"""
Telegram File Handler - автоматическое сохранение фото и документов из Telegram
Сохраняет файлы в ~/Изображения/TelegramPics/
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Настройка логирования
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

SAVE_DIR.mkdir(parents=True, exist_ok=True)
LAST_UPDATE_FILE.parent.mkdir(parents=True, exist_ok=True)

# Попытка импортировать telegram
async def download_file(file_id, file_name):
    """Скачивает файл из Telegram по file_id"""
    import aiohttp
    
    # Получаем file_path
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile"
        async with session.get(url, params={"file_id": file_id}) as resp:
            data = await resp.json()
            if not data.get("ok"):
                logger.error(f"Failed to get file info: {data}")
                return None
            file_path = data["result"]["file_path"]
            
        # Скачиваем файл
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        save_path = SAVE_DIR / file_name
        
        async with session.get(download_url) as resp:
            if resp.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await resp.read())
                logger.info(f"Saved: {save_path}")
                return str(save_path)
            else:
                logger.error(f"Download failed: {resp.status}")
                return None

async def process_updates():
    """Обрабатывает обновления от Telegram"""
    import aiohttp
    
    # Читаем последний обработанный update_id
    offset = 0
    if LAST_UPDATE_FILE.exists():
        offset = int(LAST_UPDATE_FILE.read_text().strip()) + 1
    
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        
        while True:
            try:
                params = {"offset": offset, "limit": 100}
                async with session.get(url, params=params) as resp:
                    data = await resp.json()
                    
                    if not data.get("ok"):
                        logger.error(f"API error: {data}")
                        await asyncio.sleep(5)
                        continue
                    
                    updates = data.get("result", [])
                    
                    for update in updates:
                        update_id = update["update_id"]
                        offset = update_id + 1
                        
                        message = update.get("message", {})
                        chat = message.get("chat", {})
                        chat_id = chat.get("id")
                        
                        # Обрабатываем фото
                        if "photo" in message:
                            photos = message["photo"]
                            # Берём фото максимального качества (последнее)
                            photo = photos[-1]
                            file_id = photo["file_id"]
                            file_unique_id = photo.get("file_unique_id", "unknown")
                            
                            # Генерируем имя файла
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            ext = "jpg"  # Telegram конвертирует в jpg
                            file_name = f"photo_{chat_id}_{timestamp}_{file_unique_id}.{ext}"
                            
                            logger.info(f"Downloading photo from chat {chat_id}")
                            saved_path = await download_file(file_id, file_name)
                            
                            if saved_path:
                                logger.info(f"Photo saved: {saved_path}")
                        
                        # Обрабатываем документы
                        elif "document" in message:
                            doc = message["document"]
                            file_id = doc["file_id"]
                            file_name = doc.get("file_name")
                            
                            if not file_name:
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                mime_type = doc.get("mime_type", "unknown")
                                ext = mime_type.split("/")[-1] if "/" in mime_type else "bin"
                                file_name = f"doc_{chat_id}_{timestamp}.{ext}"
                            
                            logger.info(f"Downloading document from chat {chat_id}: {file_name}")
                            saved_path = await download_file(file_id, file_name)
                            
                            if saved_path:
                                logger.info(f"Document saved: {saved_path}")
                        
                        # Обрабатываем видео
                        elif "video" in message:
                            video = message["video"]
                            file_id = video["file_id"]
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            ext = video.get("mime_type", "video/mp4").split("/")[-1]
                            file_name = f"video_{chat_id}_{timestamp}.{ext}"
                            
                            logger.info(f"Downloading video from chat {chat_id}")
                            saved_path = await download_file(file_id, file_name)
                            
                            if saved_path:
                                logger.info(f"Video saved: {saved_path}")
                        
                        # Сохраняем offset
                        LAST_UPDATE_FILE.write_text(str(update_id))
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error: {e}")
                await asyncio.sleep(5)

def main():
    try:
        import aiohttp
    except ImportError:
        logger.error("aiohttp not installed. Installing...")
        os.system(f"{sys.executable} -m pip install aiohttp --user")
        logger.info("Please restart the script")
        return
    
    logger.info("Starting Telegram File Handler...")
    logger.info(f"Save directory: {SAVE_DIR}")
    asyncio.run(process_updates())

if __name__ == "__main__":
    main()
