#!/bin/bash
# Анализ файла (я делаю это сама)
# Использование: agent_with_file.sh <файл> <задание>

TELEGRAM_PICS="/home/picoclaw/Изображения/TelegramPics"

FILE="$1"
shift
TASK="$*"

if [ -z "$FILE" ]; then
    echo "❌ Укажите файл"
    echo ""
    echo "Использование: agent_with_file.sh <файл> <задание>"
    echo ""
    echo "Доступные файлы:"
    ls -1t "$TELEGRAM_PICS/" 2>/dev/null | head -20 || echo "(папка пуста)"
    exit 1
fi

# Проверяем полный путь или имя файла
if [ -f "$FILE" ]; then
    SOURCE="$FILE"
else
    SOURCE="$TELEGRAM_PICS/$FILE"
fi

if [ ! -f "$SOURCE" ]; then
    echo "❌ Файл не найден: $FILE"
    exit 1
fi

echo "📁 Анализирую файл: $SOURCE"
echo "📝 Задание: ${TASK:-Опиши что изображено}"
echo "✅ Приступаю к анализу самостоятельно."
