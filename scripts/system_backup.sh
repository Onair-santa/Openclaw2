#!/bin/bash
# Ежедневный бэкап всей системы picoclaw на GitHub

BASE_DIR="/home/picoclaw/.picoclaw"
TOKEN_FILE="$BASE_DIR/.github_token"
REPO_URL="github.com/Onair-santa/picoclaw-backup.git"
DATE=$(date +'%Y-%m-%d %H:%M:%S')

cd "$BASE_DIR"

# Проверка наличия токена
if [ ! -f "$TOKEN_FILE" ]; then
    echo "Error: $TOKEN_FILE not found. Please put your GitHub token in it."
    exit 1
fi

TOKEN=$(cat "$TOKEN_FILE" | tr -d ' \n\r')

# Инициализация git если нужно
if [ ! -d ".git" ]; then
    git init
    git remote add origin "https://$TOKEN@$REPO_URL"
    git branch -M main
else
    # Обновляем URL с актуальным токеном (на случай смены)
    git remote set-url origin "https://$TOKEN@$REPO_URL"
fi

# Настройка пользователя
git config user.name "picoclaw-backup-bot"
git config user.email "backup@picoclaw.local"

# Бэкап
git add .
git commit -m "System backup: $DATE"
git push -u origin main
