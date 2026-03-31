# SNIPPETS.md — Полезные команды

## Прокси

```bash
# Проверить SOCKS5
curl -s --socks5 38.180.175.70:8049 --proxy-user only:only1508 --max-time 10 -I https://www.gipsyteam.ru/

# Проверить Tor
curl -s --socks5 127.0.0.1:9050 --max-time 10 -I https://check.torproject.org/
```

## GipsyTeam

```bash
# Запустить дайджест
bash /home/picoclaw/.picoclaw/workspace/skills/gipsy-digest/gipsy-digest.sh

# Проверить доступность форума
curl -s --socks5 38.180.175.70:8049 --proxy-user only:only1508 --max-time 15 https://forum.gipsyteam.ru/ | wc -c
```

## Поиск

```bash
# SearXNG
bash /home/picoclaw/.picoclaw/workspace/skills/searxng/searxng-search.sh "запрос"

# DuckDuckGo
bash /home/picoclaw/.picoclaw/workspace/skills/firefox-fetch/ddg-search.sh "запрос" 5

# Fetch URL
bash /home/picoclaw/.picoclaw/workspace/skills/firefox-fetch/ffetch.sh https://example.com
```

## Крипта

```bash
# Курсы
bash /home/picoclaw/.picoclaw/workspace/skills/crypto/get-prices.sh
```

## Git

```bash
# Быстрый commit
cd /home/picoclaw/.picoclaw/workspace && git add -A && git commit -m "$(date +%Y-%m-%d)" && git push

# Проверить статус
git -C /home/picoclaw/.picoclaw/workspace status --short
```

## Система

```bash
# Проверить диск
df -h /home/pico

# Проверить память
free -h

# Проверить проксы
systemctl is-active tor
```

## Тестирование

```bash
# Проверить все скрипты
for s in /home/picoclaw/.picoclaw/workspace/skills/*/*.sh; do echo "Testing $s..."; timeout 10 bash "$s" 2>&1 | head -3; done
```
