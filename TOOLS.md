# TOOLS.md — Локальные заметки

## File Index (SQLite база)

**Путь:** `/home/openclaw/.openclaw/workspace/data/file_index.db`

**Назначение:** Индексация, поиск и хранение метаданных всех файлов в workspace.

### Быстрые команды

```bash
# Инициализация
python3 /home/openclaw/.openclaw/workspace/skills/file-index/init_db.py

# Индексация
python3 /home/openclaw/.openclaw/workspace/skills/file-index/index_files.py

# Поиск FTS5
python3 /home/openclaw/.openclaw/workspace/skills/file-index/search.py "запрос"

# SQL запрос напрямую
sqlite3 /home/openclaw/.openclaw/workspace/data/file_index.db \
  "SELECT COUNT(*) FROM files;"
```

### Структура БД

| Таблица | Назначение |
|---------|------------|
| `files` | Метаданные (путь, размер, хэш, даты) |
| `file_content` | Текстовое содержимое |
| `tags` | Теги |
| `file_tags` | Связь файлы-теги |
| `file_search` | FTS5 для полнотекстового поиска |

### Индексируемые форматы

`.md`, `.txt`, `.py`, `.sh`, `.js`, `.ts`, `.json`, `.yaml`, `.yml`, `.toml`, `.xml`, `.csv`, `.log`

### Исключения

`node_modules/`, `.git/`, `__pycache__/`, файлы >10MB, бинарные файлы

## Playwright

**Статус:** Установлен (npx playwright@1.58.2)
**Chromium:** Скачан (167.3 MiB)
**Скилл:** `/home/openclaw/.openclaw/workspace/skills/playfetch/`

## TTS (Text-to-Speech)

**Статус:** edge-tts v7.2.8 установлен ✅
**Команда:** `edge-tts --text "<текст>" --voice ru-RU-SvetlanaNeural --write-media /tmp/msg.mp3`
**Голоса:** ru-RU-SvetlanaNeural (женский), ru-RU-DmitryNeural (мужской)
**Отправка:** Через `message` tool как аудиофайл (не voice message)

**Пример:**
```bash
edge-tts --text "Привет" --voice ru-RU-SvetlanaNeural --write-media /tmp/tts.mp3
message action=send channel=telegram target=telegram:34793946 media=/tmp/tts.mp3
```

## Skills

**Путь:** `/home/openclaw/.openclaw/workspace/skills/`
**Владелец:** openclaw:openclaw

### Список

- `crypto/` — курсы криптовалют
- `file-index/` — SQLite индексация файлов
- `pdf-to-md/` — конвертация PDF в Markdown
- `playfetch/` — парсинг через Playwright
- `workspace-startup/` — файлы для чтения при старте


**Команда:** `*баланс` (баланс, проверь баланс, баланс trx, баланс usdt)
**Cron:** 5 мин (id: bf6046f0-8d49-4546-94e1-22a5ef4c5198)
**API:** Tronscan (бесплатный)

## Конфиг (exec без approval)

```json
"tools": {
  "exec": {
    "ask": "off",
    "security": "full"
  },
  "elevated": {
    "enabled": true,
    "allowFrom": {
      "telegram": ["34793946"]
    }
  }
}
```

## Env переменной (производительность)

```bash
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
```

## ✅ Статус (2026-03-22 22:54)

**Все права:** openclaw:openclaw
- workspace/*.md ✅
- workspace/skills/ ✅
- workspace/data/ ✅

**Exec:** без approval (ask=off)
**Elevated:** включено для 34793946
**memorySearch:** ollama + qwen3-embedding:0.6b
