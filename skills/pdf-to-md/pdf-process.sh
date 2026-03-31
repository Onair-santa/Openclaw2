#!/bin/bash
# PDF to Markdown + Database processor
# Usage: pdf-process.sh <input.pdf> "Название" "#теги"

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PDF_TO_MD="$SCRIPT_DIR/pdf-to-md.sh"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[PDF→DB]${NC} $1"; }
info() { echo -e "${BLUE}[INFO]${NC} $1"; }

# Check args
if [[ $# -lt 1 ]]; then
    echo "Использование: pdf-process.sh <input.pdf> [\"Название\"] [\"#теги\"]"
    echo ""
    echo "Примеры:"
    echo "  pdf-process.sh book.pdf \"Покер: Игры Разума\" \"#покер #тильт\""
    echo "  pdf-process.sh article.pdf \"Статья\" \"#стратегия\""
    exit 1
fi

PDF_FILE="$1"
TITLE="${2:-$(basename "$PDF_FILE" .pdf)}"
TAGS="${3:-#pdf}"

# Check file
[[ ! -f "$PDF_FILE" ]] && { echo "Ошибка: файл не найден $PDF_FILE"; exit 1; }

# Create temp MD file
TEMP_MD="/tmp/pdf_$(date +%s).md"

log "Конвертация PDF → Markdown..."
"$PDF_TO_MD" "$PDF_FILE" -o "$TEMP_MD"

# Check if conversion succeeded
[[ ! -f "$TEMP_MD" ]] && { echo "Ошибка конвертации"; exit 1; }

# Read content (first 3000 chars for preview)
PREVIEW=$(head -c 3000 "$TEMP_MD" | sed 's/"/\\"/g')

log "Добавление в memory-db..."

# Build full content with tags
FULL_CONTENT="$TITLE

$PREVIEW

[Полный текст в файле: $TEMP_MD]"

# Add to database
memory-db.sh note add "$TITLE" "$FULL_CONTENT" "$TAGS #pdf2md" || {
    echo "Предупреждение: не удалось добавить в базу, но файл создан: $TEMP_MD"
    exit 0
}

log "✅ Готово!"
info "Файл: $TEMP_MD"
info "База: memory-db.sh note search \"$TITLE\""

# Optional: move to workspace
WORKSPACE_MD="/home/pico/.openclaw/workspace/docs/$(basename "$PDF_FILE" .pdf).md"
mkdir -p "$(dirname "$WORKSPACE_MD")"
cp "$TEMP_MD" "$WORKSPACE_MD" 2>/dev/null && info "Сохранено: $WORKSPACE_MD"

exit 0