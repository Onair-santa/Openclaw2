# MEMORY.md — Индекс памяти

## ⚠️ КРИТИЧЕСКИЕ ПРАВИЛА — ЧИТАТЬ ПЕРВЫМ ДЕЛОМ

### Формат ответов

- **КОРОТКО** — без воды, без вступлений
- **БЕЗ рассуждений** — не писать "думаю", "полагаю", "кажется"
- **БЕЗ повторения команд** — не дублировать то, что сказал пользователь
- **БЕЗ отчётов о процессе** — не писать "читаю файл", "ищу", "проверяю"
- **ТОЛЬКО результат** — ответ, данные, или вопрос если критично

### Поведение

- **НЕ делать без команды** — ждать команду или спросить разрешения
- **Вопрос ≠ команда** — если спросили "работает?" → ответить да/нет

---

## 🗄️ FILE INDEX (SQLite)

**Путь:** `/home/openclaw/.openclaw/workspace/data/file_index.db`

**Команды:**
```bash
python3 /home/openclaw/.openclaw/workspace/skills/file-index/search.py "запрос"
python3 /home/openclaw/.openclaw/workspace/skills/file-index/index_files.py
```

---

## 🔧 EXEC CONFIG

**Статус:** exec работает без approval (tools.exec.ask = "off")

---

## 🔐 ELEVATED ACCESS

**Включено:** tools.elevated.enabled = true
**Владелец:** allowFrom.telegram = ["34793946"]

---

## 📦 SKILLS

**Путь:** `/home/openclaw/.openclaw/workspace/skills/`

| Skill | Назначение | Команда |
|-------|------------|---------|
| `crypto/` | Курсы криптовалют | `*крипта` |
| `file-index/` | SQLite индексация | search.py |
| `pdf-to-md/` | PDF → Markdown | |
| `playfetch/` | Парсинг Playwright | |
| `system-check/` | Проверка систем | `* проверка` |
| `tron-wallet/` | TRON мониторинг | `*баланс` |

---

## 💰 TRON WALLET

**Адрес:** `TFZyBiqYPxdbgyDwN5Junf5exuT1pW39DP`
**Команда:** `*баланс`
**Cron:** 5 мин (id: bf6046f0-8d49-4546-94e1-22a5ef4c5198)
**Файлы:** `skills/tron-wallet/check_wallet.py`, `skills/tron-wallet/last_txs.json`

---

## 📅 CRON JOBS

| ID | Name | Расписание | Delivery |
|----|------|-----------|----------|
| `bf6046f0...` | TRON Wallet Monitor | каждые 5 мин | Telegram ✅ |
| `5658aa3f...` | nightly-cleanup | 3:00 MSK | Telegram ✅ |
| `666954d4...` | github-backup-daily | 3:00 MSK | none |
| `f772a4b5...` | health-morning-check | 8:00 MSK | Telegram ✅ |

---

## 🐙 GITHUB BACKUP

**Repo:** `Onair-santa/Openclaw2`
**URL:** `https://github.com/Onair-santa/Openclaw2`
**Remote:** `github` (в workspace git config)
**Branch:** `master`
**Token:** сохранён в remote URL

---

## ⚙️ ENV

```bash
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
export OLLAMA_HOST=http://192.168.0.180:11434
```

---

## ✅ СТАТУС (2026-03-31 03:45)

| Компонент | Статус |
|-----------|--------|
| OpenClaw | 2026.3.28 ✅ |
| Gateway | Active ✅ |
| Ollama | 16 models ✅ |
| Chromium | Running (CDP 18800) ✅ |
| File-index DB | 24 files ✅ |
| GitHub backup | Working ✅ |
| Tron monitor | Working ✅ |
| Exec | без approval ✅ |
| Elevated | включено ✅ |

---

## 🔑 КЛЮЧЕВЫЕ ПУТИ

| Ресурс | Путь |
|--------|------|
| Workspace | `/home/openclaw/.openclaw/workspace/` |
| Skills | `/home/openclaw/.openclaw/workspace/skills/` |
| Data | `/home/openclaw/.openclaw/workspace/data/` |
| Logs | `/home/openclaw/.openclaw/logs/` |
| Extensions | `/home/openclaw/.openclaw/extensions/` |
| Ollama | `http://192.168.0.180:11434` |

---

## 👤 OWNER

**Telegram:** 34793946 (AVK / DepartmentX)
**GitHub:** Onair-santa
**Timezone:** Europe/Moscow
