#!/bin/bash
# PDF to Markdown converter
# Usage: pdf-to-md.sh <input.pdf> [options]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log() { echo -e "${GREEN}[PDF→MD]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1" >&2; exit 1; }

# Check dependencies
command -v pdftotext &>/dev/null || error "pdftotext не найден. Установите: sudo apt-get install poppler-utils"

# Parse arguments
INPUT_FILE=""
OUTPUT_FILE=""
PAGES=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -p|--pages)
            PAGES="$2"
            shift 2
            ;;
        -h|--help)
            echo "Использование: pdf-to-md.sh <input.pdf> [options]"
            echo ""
            echo "Опции:"
            echo "  -o, --output <file>   Путь для сохранения MD"
            echo "  -p, --pages <range>     Диапазон страниц (1-50)"
            echo "  -h, --help             Показать помощь"
            exit 0
            ;;
        -*)
            error "Неизвестная опция: $1"
            ;;
        *)
            if [[ -z "$INPUT_FILE" ]]; then
                INPUT_FILE="$1"
            else
                error "Слишком много аргументов"
            fi
            shift
            ;;
    esac
done

# Validate input
[[ -z "$INPUT_FILE" ]] && error "Не указан входной PDF файл"
[[ ! -f "$INPUT_FILE" ]] && error "Файл не найден: $INPUT_FILE"

# Determine output file
if [[ -z "$OUTPUT_FILE" ]]; then
    OUTPUT_FILE="${INPUT_FILE%.pdf}.md"
fi

# Get PDF info
log "Анализ PDF: $INPUT_FILE"
PAGE_COUNT=$(pdfinfo "$INPUT_FILE" 2>/dev/null | grep Pages | awk '{print $2}' || echo "?")
log "Страниц: $PAGE_COUNT"

# Build pdftotext command
PDFTOTEXT_OPTS="-layout -enc UTF-8"

if [[ -n "$PAGES" ]]; then
    log "Конвертируем страницы: $PAGES"
    PDFTOTEXT_OPTS="$PDFTOTEXT_OPTS -f $(echo $PAGES | cut -d- -f1) -l $(echo $PAGES | cut -d- -f2)"
else
    log "Конвертируем все страницы"
fi

# Convert
log "Конвертация в Markdown..."

# Create header
cat > "$OUTPUT_FILE" << EOF
# $(basename "$INPUT_FILE" .pdf)

**Источник:** \`$INPUT_FILE\`  
**Страниц:** $PAGE_COUNT  
**Дата конвертации:** $(date +%Y-%m-%d)

---

EOF

# Extract text and append
if [[ -n "$PAGES" ]]; then
    pdftotext $PDFTOTEXT_OPTS "$INPUT_FILE" - >> "$OUTPUT_FILE" 2>/dev/null
else
    pdftotext $PDFTOTEXT_OPTS "$INPUT_FILE" - >> "$OUTPUT_FILE" 2>/dev/null
fi

# Post-process: fix common issues
log "Пост-обработка..."

# Remove excessive blank lines
sed -i '/^[[:space:]]*$/N;/^[[:space:]]*\n[[:space:]]*$/d' "$OUTPUT_FILE" 2>/dev/null || true

# Add page markers (if full conversion)
if [[ -z "$PAGES" ]]; then
    sed -i 's/\f/\n\n---\n\n**Конец страницы**\n\n---\n\n/g' "$OUTPUT_FILE" 2>/dev/null || true
fi

# Success
FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
log "✅ Готово: $OUTPUT_FILE ($FILE_SIZE)"

echo "$OUTPUT_FILE"