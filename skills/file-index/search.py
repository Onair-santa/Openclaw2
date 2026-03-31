#!/usr/bin/env python3
"""Поиск по индексированным файлам"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path("/home/openclaw/.openclaw/workspace/data/file_index.db")

def search(query, limit=20, use_fts=True):
    """Поиск по базе"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if use_fts:
        # FTS5 поиск - сначала найдём ID файлов
        c.execute('''
            SELECT rowid FROM file_search WHERE file_search MATCH ? LIMIT ?
        ''', (query, limit))
        rowids = [r[0] for r in c.fetchall()]
        
        if not rowids:
            conn.close()
            return []
        
        # Теперь получим информацию о файлах
        placeholders = ','.join('?' * len(rowids))
        c.execute(f'''
            SELECT f.path, f.filename, f.extension, f.size_bytes, 
                   fc.word_count, fc.line_count
            FROM files f
            LEFT JOIN file_content fc ON f.id = fc.file_id
            WHERE f.id IN ({placeholders})
        ''', rowids)
        results = c.fetchall()
        conn.close()
        return results
    else:
        # Обычный LIKE поиск
        c.execute('''
            SELECT path, filename, extension, size_bytes, NULL, NULL
            FROM files
            WHERE filename LIKE ? OR path LIKE ?
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
        results = c.fetchall()
        conn.close()
        return results

def main():
    if len(sys.argv) < 2:
        print("Usage: search.py <query> [--limit N] [--no-fts]")
        print("Example: search.py 'python' --limit 10")
        sys.exit(1)
    
    query = sys.argv[1]
    limit = 20
    use_fts = True
    
    if '--limit' in sys.argv:
        idx = sys.argv.index('--limit')
        limit = int(sys.argv[idx + 1])
    
    if '--no-fts' in sys.argv:
        use_fts = False
    
    results = search(query, limit, use_fts)
    
    print(f"🔍 Поиск: '{query}' (найдено: {len(results)})")
    print("=" * 60)
    
    for row in results:
        path, filename, ext, size, words, lines = row
        size_kb = round(size / 1024, 1) if size else 0
        print(f"📄 {filename} {ext}")
        print(f"   Путь: {path}")
        print(f"   Размер: {size_kb} KB")
        if words:
            print(f"   Слова: {words}, Строки: {lines}")
        print("")

if __name__ == "__main__":
    main()
