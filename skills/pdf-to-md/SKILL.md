---
name: pdf-to-md
description: Конвертация PDF в Markdown и занесение в базу знаний
---

# PDF to Markdown Skill

Конвертирует PDF файлы в Markdown с помощью `pdftotext`, сохраняет структуру и заносит в memory-db.

## Установка зависимостей

```bash
sudo apt-get install -y poppler-utils   # для pdftotext
```

## Использование

### Простая конвертация
```bash
pdf-to-md.sh /path/to/file.pdf
# Вывод: /path/to/file.md
```

### Конвертация + занесение в базу
```bash
pdf-process.sh /path/to/file.pdf "Название книги" "#тег1 #тег2"
# Создаёт Markdown и добавляет заметку в memory-db
```

### Параметры
- `-o, --output` — путь для сохранения MD
- `-p, --pages` — диапазон страниц (1-50)
- `-db, --database` — занести в memory-db после конвертации

## Примеры

```bash
# Полная книга
pdf-to-md.sh ~/books/poker.pdf

# Только главы 1-3
pdf-to-md.sh ~/books/poker.pdf -p 1-50

# Конвертация + база
pdf-process.sh ~/books/poker.pdf "Покер: Игры Разума" "#покер #психология #тильт"
```

## Структура выходного Markdown

```markdown
# Название документа

**Источник:** `original.pdf`  
**Страниц:** 242  
**Дата:** 2026-03-12

---

## Содержание

- [Глава 1](#глава-1)
- ...

---

## Глава 1

Текст главы...

---

## Глава 2

...
```

## Интеграция с memory-db

```bash
# Поиск по конвертированным книгам
memory-db.sh note search "тильт"
memory-db.sh note search "месть" | grep "Покер"
```

## Ограничения

- Только текстовые PDF (не сканы)
- Для сканов использовать OCR (tesseract)
- Сложное форматирование может теряться