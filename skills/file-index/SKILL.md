---
name: file-index
description: SQLite база для индексации, поиска и хранения метаданных всех файлов в workspace. FTS5 полнотекстовый поиск.
---

# File Index Skill

SQLite база данных для индексации всех файлов в рабочем пространстве.

## Быстрый старт

```bash
# Инициализация базы
python3 /home/openclaw/.openclaw/workspace/skills/file-index/init_db.py

# Индексация файлов
python3 /home/openclaw/.openclaw/workspace/skills/file-index/index_files.py

# Поиск
python3 /home/openclaw/.openclaw/workspace/skills/file-index/search.py "запрос"
```

## Структура БД

| Таблица | Назначение |
|---------|------------|
| `files` | Метаданные файлов (путь, размер, хэш, даты) |
| `file_content` | Текстовое содержимое + статистика |
| `tags` | Теги для категоризации |
| `file_tags` | Связь файлы-теги |
| `file_search` | FTS5 виртуальная таблица для поиска |

## Поиск

### Полнотекстовый поиск

```bash
search.py "ключевые слова"
search.py "python" --limit 20
search.py "config" --ext .json
```

### SQL запросы

```sql
-- Последние изменённые файлы
SELECT path, filename, modified_at FROM files 
ORDER BY modified_at DESC LIMIT 10;

-- Поиск по содержимому
SELECT f.path, fc.content_text 
FROM files f 
JOIN file_content fc ON f.id = fc.file_id
WHERE fc.content_text LIKE '%запрос%';

-- FTS5 поиск
SELECT f.path, fs.* 
FROM file_search fs
JOIN files f ON f.id = fs.rowid
WHERE file_search MATCH 'запрос';

-- Файлы по расширению
SELECT extension, COUNT(*) as count 
FROM files GROUP BY extension ORDER BY count DESC;
```

## Скрипты

- `init_db.py` — создание БД и таблиц
- `index_files.py` — сканирование workspace
- `search.py` — поиск по базе

## Исключения

Не индексируются:
- `node_modules/`, `.git/`, `__pycache__/`
- Файлы >10MB
- Бинарные расширения: `.pyc`, `.so`, `.dll`, `.exe`

## Текстовые форматы

Индексируется содержимое:
`.md`, `.txt`, `.py`, `.sh`, `.js`, `.ts`, `.json`, `.yaml`, `.yml`, `.toml`, `.xml`, `.csv`, `.log`

## Пересиновка

```bash
# Полная переиндексация
python3 index_files.py

# Проверить статус
sqlite3 /home/openclaw/.openclaw/workspace/data/file_index.db \
  "SELECT COUNT(*) FROM files; SELECT COUNT(*) FROM file_content;"
```
