#!/usr/bin/env python3
"""Инициализация SQLite базы для индексации файлов workspace"""

import sqlite3
import os
from pathlib import Path

DB_PATH = Path("/home/openclaw/.openclaw/workspace/data/file_index.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Таблица файлов
c.execute('''
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE NOT NULL,
    filename TEXT NOT NULL,
    extension TEXT,
    size_bytes INTEGER,
    created_at REAL,
    modified_at REAL,
    content_hash TEXT,
    content_type TEXT,
    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Таблица содержимого (для текстовых файлов)
c.execute('''
CREATE TABLE IF NOT EXISTS file_content (
    file_id INTEGER PRIMARY KEY,
    content_text TEXT,
    word_count INTEGER,
    line_count INTEGER,
    FOREIGN KEY (file_id) REFERENCES files(id)
)
''')

# Таблица тегов
c.execute('''
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
''')

# Связь файлы-теги
c.execute('''
CREATE TABLE IF NOT EXISTS file_tags (
    file_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (file_id, tag_id),
    FOREIGN KEY (file_id) REFERENCES files(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
)
''')

# Индексы для поиска
c.execute('CREATE INDEX IF NOT EXISTS idx_files_path ON files(path)')
c.execute('CREATE INDEX IF NOT EXISTS idx_files_ext ON files(extension)')
c.execute('CREATE INDEX IF NOT EXISTS idx_files_modified ON files(modified_at)')
c.execute('CREATE INDEX IF NOT EXISTS idx_content_text ON file_content(content_text)')
c.execute('CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name)')

# FTS5 для полнотекстового поиска
c.execute('''
CREATE VIRTUAL TABLE IF NOT EXISTS file_search USING fts5(
    filename,
    content_text,
    path,
    content='file_content',
    content_rowid='file_id'
)
''')

conn.commit()
conn.close()

print(f"✅ База создана: {DB_PATH}")
print(f"📊 Таблицы: files, file_content, tags, file_tags, file_search (FTS5)")
