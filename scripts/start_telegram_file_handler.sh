#!/bin/bash
# Запуск Telegram File Handler в tmux сессии

SESSION_NAME="telegram_files"
SCRIPT_PATH="/home/picoclaw/.picoclaw/scripts/telegram_file_handler.py"

cd /home/picoclaw

# Проверяем, запущена ли сессия
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "⚠️ Сессия $SESSION_NAME уже запущена"
    echo "Подключиться: tmux attach -t $SESSION_NAME"
    exit 0
fi

# Устанавливаем зависимости если нужно
if ! python3 -c "import aiohttp" 2>/dev/null; then
    echo "📦 Установка aiohttp..."
    python3 -m pip install aiohttp --user
fi

# Создаём сессию tmux
tmux new-session -d -s "$SESSION_NAME" -n "handler"

# Запускаем скрипт
tmux send-keys -t "$SESSION_NAME" "python3 $SCRIPT_PATH" C-m

echo "✅ Telegram File Handler запущен в tmux сессии '$SESSION_NAME'"
echo "📁 Файлы сохраняются в: ~/Изображения/TelegramPics/"
echo ""
echo "Команды:"
echo "  tmux attach -t $SESSION_NAME  - посмотреть логи"
echo "  tmux kill-session -t $SESSION_NAME  - остановить"
echo "  ls ~/Изображения/TelegramPics/  - список файлов"
