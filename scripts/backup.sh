#!/bin/bash
# Скрипт ежедневного бэкапа рабочего пространства в GitHub
# Требует установленного CLI gh

BACKUP_DIR="/home/picoclaw/.picoclaw/workspace"
DATE=$(date +%Y%m%d_%H%M%S)
REPO="picoclaw-backup"

cd "$BACKUP_DIR"

# Инициализация репозитория, если нет
if [ ! -d ".git" ]; then
    git init
    git remote add origin https://github.com/OnlyPico/picoclaw-backup.git
fi

# Добавление файлов (исключая тяжелые данные если нужно)
git add .
git commit -m "Backup $DATE"
git push -u origin main
