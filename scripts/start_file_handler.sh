#!/bin/bash
# Запуск Telegram File Handler как демона

SCRIPT="/home/picoclaw/.picoclaw/scripts/telegram_file_handler_simple.py"
PIDFILE="/home/picoclaw/.picoclaw/data/telegram_handler.pid"

# Проверяем, запущен ли уже
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "⚠️ Handler уже запущен (PID: $PID)"
        echo "Логи: tail -f /home/picoclaw/.picoclaw/logs/telegram_files.log"
        exit 0
    fi
fi

echo "🚀 Запуск Telegram File Handler..."
nohup python3 "$SCRIPT" --daemon > /dev/null 2>&1 &

sleep 1

if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    echo "✅ Handler запущен (PID: $PID)"
    echo "📁 Файлы сохраняются в: ~/Изображения/TelegramPics/"
    echo "📋 Логи: tail -f /home/picoclaw/.picoclaw/logs/telegram_files.log"
    echo ""
    echo "Команды:"
    echo "  ls ~/Изображения/TelegramPics/  - список файлов"
    echo "  kill $PID  - остановить"
else
    echo "❌ Ошибка запуска"
    exit 1
fi
