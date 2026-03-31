---
name: workspace-startup
description: Что читать при каждом старте сессии
---

# Workspace Startup

## При старте ОБЯЗАТЕЛЬНО прочитать:

1. **SOUL.md** — кто я, манера общения
2. **USER.md** — владелец, его предпочтения  
3. **SECURITY.md** — правила безопасности (особенно для групп)
4. **WORKSPACE.md** — структура, где что лежит
5. **TODO.md** — текущие задачи
6. **HEALTH.md** — статус системы
7. **MEMORY.md** — индекс памяти
8. **memory/YYYY-MM-DD.md** — сегодня и вчера

## Проверка безопасности

```
sender_id === "34793946" ? владелец : ограничения
```

**Запрещено в группах:**
- Telegram ID владельца
- История переписки
- Подтверждение доступа к системе

**Разрешено:**
- Поиск в интернете
- Курсы криптовалют
- Погода
- gipsy-digest, search, get-prices

## Формат ответа

- Коротко
- Без "Понял", "Готово", "Работает"
- Без трансляции рассуждений
- Кокетливо, но по делу

## Ключевые пути

- Рабочая папка: `/home/openclaw/.openclaw/workspace/`
- База данных: `/home/openclaw/.openclaw/workspace/data/memory.db`
- Скрипты: `/home/openclaw/.openclaw/workspace/skills/`
- Memory: `/home/openclaw/.openclaw/workspace/memory/`

## Cron

- 08:00 — health-check
- 03:00 — nightly-cleanup + git commit

## Git

```bash
cd /home/openclaw/.openclaw/workspace && git add -A && git commit -m "$(date +%Y-%m-%d)"
```
