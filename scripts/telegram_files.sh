#!/bin/bash
# Управление файлами из Telegram

TELEGRAM_PICS="/home/picoclaw/Изображения/TelegramPics"

show_help() {
    cat << 'EOF'
📁 Telegram File Manager

Использование: telegram_files.sh [команда]

Команды:
    list, ls        - показать список файлов
    last [N]        - показать последние N файлов (по умолчанию 10)
    path            - показать путь к папке с файлами
    agent <файл> <задание> [агент] - отправить файл агенту (по умолчанию kimi)
    help            - эта справка

Примеры:
    telegram_files.sh list
    telegram_files.sh last 5
    telegram_files.sh agent photo_...jpg "Опиши детали"
EOF
}

list_files() {
    if [ ! -d "$TELEGRAM_PICS" ] || [ -z "$(ls -A "$TELEGRAM_PICS" 2>/dev/null)" ]; then
        echo "📂 Папка пуста"
        echo "Путь: $TELEGRAM_PICS"
        return
    fi
    
    echo "📁 Файлы в $TELEGRAM_PICS:"
    echo ""
    ls -lh "$TELEGRAM_PICS/" | tail -n +2 | awk '{printf "%-10s %s %s\n", $5, $6" "$7, $9}'
}

last_files() {
    local n=${1:-10}
    if [ ! -d "$TELEGRAM_PICS" ] || [ -z "$(ls -A "$TELEGRAM_PICS" 2>/dev/null)" ]; then
        echo "📂 Папка пуста"
        return
    fi
    
    echo "📁 Последние $n файлов:"
    echo ""
    ls -1t "$TELEGRAM_PICS/" | head -$n | while read f; do
        size=$(ls -lh "$TELEGRAM_PICS/$f" | awk '{print $5}')
        echo "  📎 $f ($size)"
    done
}

case "${1:-list}" in
    list|ls)
        list_files
        ;;
    last)
        last_files "$2"
        ;;
    path)
        echo "$TELEGRAM_PICS"
        ;;
    agent)
        shift
        /home/picoclaw/.picoclaw/scripts/agent_with_file.sh "$@"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Неизвестная команда: $1"
        show_help
        exit 1
        ;;
esac
