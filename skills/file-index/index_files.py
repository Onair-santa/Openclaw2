#!/usr/bin/env python3
"""Индексация файлов workspace в SQLite базу"""

import sqlite3
import os
import hashlib
from pathlib import Path
from datetime import datetime

DB_PATH = Path("/home/openclaw/.openclaw/workspace/data/file_index.db")
WORKSPACE = Path("/home/openclaw/.openclaw/workspace")

# Исключения
EXCLUDE_DIRS = {'node_modules', '.git', '__pycache__', '.openclaw-install-stage*'}
EXCLUDE_EXTS = {'.pyc', '.pyo', '.so', '.dll', '.exe'}
MAX_SIZE_MB = 10

def file_hash(path):
    """MD5 хэш файла"""
    hash_md5 = hashlib.md5()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def read_content(path):
    """Чтение текстового содержимого"""
    text_extensions = {'.md', '.txt', '.py', '.sh', '.js', '.ts', '.json', '.yaml', '.yml', '.toml', '.xml', '.csv', '.log'}
    if path.suffix.lower() not in text_extensions:
        return None, 0, 0
    try:
        content = path.read_text(errors='ignore')
        return content, len(content.split()), len(content.splitlines())
    except:
        return None, 0, 0

def index_file(cursor, path: Path):
    """Индексация одного файла"""
    try:
        stat = path.stat()
        content, words, lines = read_content(path)
        content_hash = file_hash(path)
        
        # Вставка файла
        cursor.execute('''
            INSERT OR REPLACE INTO files 
            (path, filename, extension, size_bytes, created_at, modified_at, content_hash, content_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            str(path),
            path.name,
            path.suffix.lower(),
            stat.st_size,
            stat.st_ctime,
            stat.st_mtime,
            content_hash,
            path.suffix.lower()
        ))
        
        file_id = cursor.execute('SELECT id FROM files WHERE path = ?', (str(path),)).fetchone()[0]
        
        # Сохранение содержимого
        if content:
            cursor.execute('''
                INSERT OR REPLACE INTO file_content (file_id, content_text, word_count, line_count)
                VALUES (?, ?, ?, ?)
            ''', (file_id, content, words, lines))
            
            # Обновление FTS индекса
            cursor.execute('''
                INSERT OR REPLACE INTO file_search (rowid, filename, content_text, path)
                VALUES (?, ?, ?, ?)
            ''', (file_id, path.name, content, str(path)))
        
        return True
    except Exception as e:
        print(f"⚠️ Ошибка: {path} — {e}")
        return False

def scan_workspace():
    """Сканирование workspace"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("🔍 Сканирование workspace...")
    indexed = 0
    errors = 0
    
    for root, dirs, files in os.walk(WORKSPACE):
        # Исключение папок
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if Path(file).suffix.lower() in EXCLUDE_EXTS:
                continue
            
            path = Path(root) / file
            
            # Пропуск больших файлов
            try:
                if path.stat().st_size > MAX_SIZE_MB * 1024 * 1024:
                    continue
            except:
                continue
            
            if index_file(c, path):
                indexed += 1
            else:
                errors += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Индексировано: {indexed} файлов")
    print(f"⚠️ Ошибок: {errors}")

if __name__ == "__main__":
    scan_workspace()
