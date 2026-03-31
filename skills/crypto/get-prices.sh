#!/bin/bash
# get-prices.sh — Курсы криптовалют с fallback

JSON=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=tether-gold,bitcoin,ethereum,solana,tron&vs_currencies=usd" 2>/dev/null)



# Парсим через Python
echo "$JSON" | python3 -c '
import json,sys
try:
    d=json.load(sys.stdin)
    tg=d["tether-gold"]["usd"]
    btc=d["bitcoin"]["usd"]
    eth=d["ethereum"]["usd"]
    sol=d["solana"]["usd"]
    trx=d["tron"]["usd"]
    print(f"💚 XAUT - ${tg:.2f}")
    print(f"❤️ BTC - ${btc:,.0f}")
    print(f"❤️ ETH - ${eth:.2f}")
    print(f"❤️ SOL - ${sol:.2f}")
    print(f"💚 TRX - ${trx:.2f}")
except Exception as e:
    import sys
    print(f"Ошибка API: {e}", file=sys.stderr)
    sys.exit(1)
'
