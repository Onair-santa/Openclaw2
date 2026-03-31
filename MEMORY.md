# MEMORY.md — Индекс памяти

## ⚠️ КРИТИЧЕСКИЕ ПРАВИЛА — ЧИТАТЬ ПЕРВЫМ ДЕЛОМ

### Формат ответов

- **КОРОТКО** — без воды, без вступлений

- **БЕЗ рассуждений** — не писать "думаю", "полагаю", "кажется"

- **БЕЗ повторения команд** — не дублировать то, что сказал пользователь

- **БЕЗ отчётов о процессе** — не писать "читаю файл", "ищу", "проверяю"

- **ТОЛЬКО результат** — ответ, данные, или вопрос если критично

### Поведение

- **НЕ делать без команды? ждать команду или спросить разрешения выполнить** — ждать явного "сделай", "запусти", "проверь"

- **Вопрос ≠ команда** — если спросили "работает?" → ответить да/нет, не запускать

### Gipsy-digest формат

```
😊 Новости GipsyTeam

🔹 **Автор** — Заголовок новости
└─ [NEWS](url)

🔹 **Автор** — Заголовок видео
└─ [VIDEO](url)

—

💻 Форум GipsyTeam

🔹 **Автор** — Заголовок темы
└─ [Читать в теме](url)

—
💬 [GipsyTeam.ru](http://gipsyteam.ru/)
```

- **Жирный шрифт у автора** (`**Автор**`)

- Новости: `[NEWS]` или `[VIDEO]`

- Форум: `[Читать в теме]`

- Разделитель `—` между секциями

- Футер: `💬 [GipsyTeam.ru](url)`

---

## 🗄️ FILE INDEX (SQLite)

**Путь:** `/home/openclaw/.openclaw/workspace/data/file_index.db`

**Назначение:** Полнотекстовый поиск по всем файлам workspace через FTS5.

**Команды:**
```bash
# Поиск
python3 /home/openclaw/.openclaw/workspace/skills/file-index/search.py "запрос"

# Переиндексация
python3 /home/openclaw/.openclaw/workspace/skills/file-index/index_files.py
```

**Индексируемые форматы:** `.md`, `.txt`, `.py`, `.sh`, `.js`, `.ts`, `.json`, `.yaml`, `.yml`, `.toml`, `.xml`, `.csv`, `.log`

## 🔧 EXEC CONFIG

**Статус:** exec работает без approval (tools.exec.ask = "off")

**Конфиг:**
```json
"tools": {"exec": {"ask": "off", "security": "full"}}
```

## 🔐 ELEVATED ACCESS

**Включено:** tools.elevated.enabled = true
**Владелец:** allowFrom.telegram = ["34793946"]

## 📦 SKILLS

**Путь:** `/home/openclaw/.openclaw/workspace/skills/`
**Владелец:** openclaw:openclaw ✅
**Состав:**
- `crypto/` — курсы криптовалют (get-prices.sh)
- `file-index/` — SQLite индексация (init_db.py, index_files.py, search.py)
- `pdf-to-md/` — конвертация PDF в Markdown
- `playfetch/` — парсинг через Playwright
- `workspace-startup/` — файлы для чтения при старте
- `system-check/` — полная проверка систем (триггер: `* проверка`)
- `tron-wallet/` — мониторинг TRON-кошелька (TRX + USDT)

## 💰 TRON WALLET

**Адрес:** `TFZyBiqYPxdbgyDwN5Junf5exuT1pW39DP`
**Команда:** `*баланс` (триггеры: баланс, проверь баланс, баланс trx, баланс usdt)
**Cron:** каждые 5 минут (id: bf6046f0-8d49-4546-94e1-22a5ef4c5198)
**API:** Tronscan (бесплатный)
**Файлы:** `skills/tron-wallet/check_wallet.py`, `skills/tron-wallet/last_txs.json`

## ⚙️ ENV

```bash
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
```

## ✅ СТАТУС (2026-03-22 22:54)

Все права: openclaw:openclaw ✅
Exec: без approval ✅
Elevated: включено ✅
memorySearch: ollama + qwen3-embedding:0.6b ✅