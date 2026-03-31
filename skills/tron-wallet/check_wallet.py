#!/usr/bin/env python3
"""
TRON Wallet Monitor
Проверяет входящие транзакции TRX и USDT на кошельке.
"""

import json
import sys
import os
import urllib.request
import urllib.parse
from datetime import datetime

# Конфигурация
WALLET_ADDRESS = "TFZyBiqYPxdbgyDwN5Junf5exuT1pW39DP"
STATE_FILE = "/home/openclaw/.openclaw/workspace/skills/tron-wallet/last_txs.json"

# API endpoints (используем trongrid.io)
TRONGRID_API = "https://api.trongrid.io/v1"
TRONSCAN_API = "https://apilist.tronscan.org/api"

# USDT TRC-20 contract
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"


def api_get(url, params=None):
    """GET запрос к API."""
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"API error: {e}", file=sys.stderr)
        return None


def get_balance():
    """Получить баланс кошелька через trongrid.io + tronscan."""
    balance = {"trx": 0.0, "usdt": 0.0}
    
    # TRX Balance через trongrid
    result = api_get(f"{TRONGRID_API}/accounts/{WALLET_ADDRESS}")
    if result and result.get("data"):
        balance["trx"] = int(result["data"][0].get("balance", 0)) / 1e6
    
    # USDT Balance через Tronscan (у них другой формат)
    result = api_get(f"{TRONSCAN_API}/account", {
        "address": WALLET_ADDRESS
    })
    if result and result.get("trc20token_balances"):
        for t in result["trc20token_balances"]:
            if t.get("tokenAbbr") == "USDT":
                balance["usdt"] = int(t.get("balance", "0")) / 1e6
                break
    
    return balance


def get_incoming_transactions(limit=10):
    """Получить входящие транзакции (TRX + USDT)."""
    all_txs = []
    
    # === TRX Transactions через Tronscan ===
    result = api_get(f"{TRONSCAN_API}/transaction", {
        "address": WALLET_ADDRESS,
        "sort": "-timestamp",
        "limit": str(limit),
        "direction": "in",
        "count": "true"
    })
    
    if result and result.get("data"):
        for tx in result["data"]:
            if tx.get("toAddress") == WALLET_ADDRESS:
                tx_type = tx.get("tokenType", "trc10")
                token = tx.get("tokenAbbr", "TRX") if tx_type == "trc10" else "TRX"
                amount = float(tx.get("amount", 0))
                
                all_txs.append({
                    "hash": tx["hash"],
                    "token": token,
                    "amount": amount,
                    "timestamp": tx.get("timestamp", 0),
                    "type": "trx"
                })
    
    # === USDT TRC-20 через Tronscan ===
    result = api_get(f"{TRONSCAN_API}/token_trc20/transfers", {
        "address": WALLET_ADDRESS,
        "sort": "-block_ts",
        "limit": str(limit)
    })
    
    if result and result.get("token_transfers"):
        for tx in result["token_transfers"]:
            if tx.get("to_address") == WALLET_ADDRESS:
                token_info = tx.get("tokenInfo", {})
                decimals = int(token_info.get("tokenDecimal", 6))
                amount_raw = tx.get("quant", "0")
                
                # Skip approval/other non-transfer events
                event_type = tx.get("event_type", "")
                if event_type != "Transfer":
                    continue
                
                try:
                    amount = int(amount_raw) / (10 ** decimals)
                except:
                    amount = 0
                
                all_txs.append({
                    "hash": tx["transaction_id"],
                    "token": "USDT",
                    "amount": amount,
                    "timestamp": tx.get("block_ts", 0),
                    "from_address": tx.get("from_address", ""),
                    "type": "trc20"
                })
    
    # Сортируем по времени (новые первые)
    all_txs.sort(key=lambda x: x["timestamp"], reverse=True)
    return all_txs[:limit]


def format_amount(amount, token):
    """Форматирование суммы."""
    if token == "USDT":
        return f"${amount:,.2f}"
    elif token == "TRX":
        return f"{amount:,.2f} TRX"
    else:
        return f"{amount} {token}"


def load_last_state():
    """Загрузить последнее состояние."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {"last_trx_hash": None, "last_usdt_hash": None}


def save_state(state):
    """Сохранить состояние."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def check_and_notify():
    """
    Основная проверка кошелька.
    Returns: (new_transactions, messages)
    """
    state = load_last_state()
    txs = get_incoming_transactions(limit=20)
    
    new_incoming = []
    
    for tx in txs:
        tx_hash = tx["hash"]
        token = tx["token"]
        
        # Определяем ключ состояния
        if token == "USDT":
            last_hash = state.get("last_usdt_hash")
        else:
            last_hash = state.get("last_trx_hash")
        
        # Пропускаем уже известные
        if last_hash and tx_hash == last_hash:
            break
        
        new_incoming.append(tx)
    
    # Если есть новые — обновляем состояние
    if new_incoming:
        # Обновляем последние хеши
        for tx in new_incoming:
            if tx["token"] == "USDT":
                state["last_usdt_hash"] = tx["hash"]
            else:
                state["last_trx_hash"] = tx["hash"]
        
        save_state(state)
    
    return new_incoming


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # Ручная проверка — вывод в stdout
        balance = get_balance()
        txs = get_incoming_transactions(limit=5)
        
        print(f"=== TRON Wallet Monitor ===")
        print(f"Address: {WALLET_ADDRESS}")
        print()
        print(f"Balance:")
        print(f"  TRX:  {balance['trx']:,.6f}")
        print(f"  USDT: ${balance['usdt']:,.2f}")
        print()
        print("Recent transactions:")
        for tx in txs:
            ts = datetime.fromtimestamp(tx["timestamp"]/1000).strftime("%Y-%m-%d %H:%M")
            print(f"  {ts} | {format_amount(tx['amount'], tx['token']):>15} | {tx['hash'][:20]}...")
    else:
        # Автоматическая проверка (cron) — результат парсится
        new_txs = check_and_notify()
        
        if new_txs:
            messages = []
            for tx in new_txs:
                ts = datetime.fromtimestamp(tx["timestamp"]/1000).strftime("%Y-%m-%d %H:%M")
                amount_str = format_amount(tx["amount"], tx["token"])
                
                msg = f"💰 Входящая транзакция!\n"
                msg += f"Токен: {tx['token']}\n"
                msg += f"Сумма: {amount_str}\n"
                msg += f"Время: {ts}\n"
                msg += f"Hash: `{tx['hash'][:32]}...`"
                
                if tx.get("from_address"):
                    msg += f"\nОт: `{tx['from_address'][:10]}...`"
                
                messages.append(msg)
            
            print("\n\n".join(messages))
        else:
            print("No new transactions")
