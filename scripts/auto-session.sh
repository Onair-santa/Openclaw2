#!/bin/bash
# auto-session.sh - Автоматическое сохранение сессии в SQLite и файл
DB_PATH="/home/picoclaw/.picoclaw/workspace/data/memory.db"
MEM_DIR="/home/picoclaw/.picoclaw/workspace/memory/$(date +%Y%m)"
FILE_PATH="$MEM_DIR/$(date +%Y-%m-%d).md"

mkdir -p "$MEM_DIR"

# Сохранение в файл
echo "# Session $(date +%Y-%m-%d)" > "$FILE_PATH"
echo "" >> "$FILE_PATH"
echo "**Date:** $(date +%Y-%m-%d)" >> "$FILE_PATH"
echo "**Status:** ✅ Автосохранение" >> "$FILE_PATH"
echo "" >> "$FILE_PATH"
echo "## Summary" >> "$FILE_PATH"
echo "Автоматическое сохранение сессии." >> "$FILE_PATH"
echo "" >> "$FILE_PATH"
echo "## Details" >> "$FILE_PATH"
echo "- Сессия сохранена автоматически в $(date +%H:%M)" >> "$FILE_PATH"
echo "- Файл: $FILE_PATH" >> "$FILE_PATH"

# Сохранение в SQLite
sqlite3 "$DB_PATH" "INSERT INTO sessions (date, summary) VALUES ('$(date +%Y-%m-%d)', 'Auto-save');"

echo "Session saved at $(date)" >> /home/picoclaw/.picoclaw/logs/auto-session.log
