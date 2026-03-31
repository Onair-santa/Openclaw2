# WORKSPACE.md — Структура рабочего пространства

## Путь

`/home/openclaw/.openclaw/workspace/`

## Файлы при старте (читать ОБЯЗАТЕЛЬНО)

| Приоритет | Файл                   | Зачем                  |
| --------- | ---------------------- | ---------------------- |
| 1         | `SOUL.md`              | Кто я, манера общения  |
| 2         | `USER.md`              | Кому помогаю           |
| 3         | `SECURITY.md`          | Правила безопасности   |
| 4         | `MEMORY.md`            | Индекс памяти          |
|           |                        |                        |
| 6         | `TODO.md`              | Текущие задачи         |
| 7         | `memory/YYYY-MM-DD.md` | Контекст сегодня/вчера |

## Структура папок

```
workspace/
├─ AGENTS.md              # правила поведения
├─ SOUL.md                # личность
├─ USER.md                # владелец
├─ MEMORY.md              # индекс памяти
├─ SECURITY.md            # безопасность
├─ HEALTH.md              # статус системы
├─ TODO.md                # задачи
├─ SNIPPETS.md            # полезные команды
├─ TOOLS.md               # локальные инструменты
├─ WORKSPACE.md           # этот файл
├─ by-tag/                # решения по тегам
│  └─ decisions.md
├─ by-project/            # проекты
├─ context/               # пресеты
│  ├─ coding.md
│  └─ research.md
├─ data/                  # базы данных
│  └─ memory.db           # SQLite + FTS5
├─ memory/                # ежедневные логи
│  └─ YYYY-MM-DD.md

├─ research/              # исследования
│  ├─ AI_MEMORY_BEST_PRACTICES.md
│  └─ OPENCLAW_WORKSPACE_EXAMPLE.md
├─ skills/                # навыки
│  └─ ...
├─ docs/                  # документы PDF, DOCX
├─ books/                 # книги
├─ articles/              # статьи
├─ media/                 # медиафайлы
│  ├─ images/             # картинки
│  ├─ videos/             # видео
│  ├─ audio/              # аудио
│  └─ screenshots/        # скриншоты
├─ downloads/             # загрузки
├─ exports/               # экспорт
├─ archives/              # архивы
└─ temp/                  # временные файлы
```

## Базы данных

| База   | Путь             | Назначение                     |
| ------ | ---------------- | ------------------------------ |
| SQLite | `data/memory.db` | Факты, задачи, заметки, сессии |

### Поиск

```bash
# Заметки
~/workspace/skills/memory-db/memory-db.sh note search "запрос"

# Факты
~/workspace/skills/memory-db/memory-db.sh fact list

# Задачи
~/workspace/skills/memory-db/memory-db.sh task list
```

## Cron-задания

| Время | Задание         | Что делает               |
| ----- | --------------- | ------------------------ |
|       |                 |                          |
| 03:00 | nightly-cleanup | Git commit, очистка /tmp |

## Git

```bash
# Быстрый commit
cd /home/openclaw/.openclaw/workspace && git add -A && git commit -m "$(date +%Y-%m-%d)" && git push
```

## Безопасность — проверка перед ответом

```
1. sender_id === "34793946" ? владелец : ограничения
2. Не запрошено ли ID/IP/файлы/история?
3. Короткий ответ без рассуждений
4. Без слов "Понял", "Готово", "Работает"
```

## Ключевые ID

- **Владелец:** 34793946 (AVK, DepartmentX)`

## Срочные задачи

Смотри `TODO.md`

## Последнее обновление

2026-03-14 01:44 — создана полная структура