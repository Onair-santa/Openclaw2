---
name: tron-wallet
description: "*баланс, проверь баланс, баланс кошелька, состояние кошелька, баланс trx, баланс usdt, баланс trc20"
---

# TRON Wallet Monitor

## Описание
Мониторинг TRON-кошелька: TRX + USDT (TRC-20). Автоматические уведомления при поступлении средств.

## Команды

### *баланс
Показать текущий баланс кошелька.

**Триггеры:** `*баланс`, `баланс`, `проверь баланс`, `баланс кошелька`, `состояние кошелька`, `баланс trx`, `баланс usdt`

**Вывод:**
- TRX balance
- USDT (TRC-20) balance  
- Последние транзакции

## Конфигурация
- Адрес кошелька: `TFZyBiqYPxdbgyDwN5Junf5exuT1pW39DP`
- Токены: TRX, USDT (TRC-20)
- Интервал проверки: каждые 5 минут (cron)
- Состояние: `last_txs.json`

## Автоматический мониторинг
Cron job каждые 5 минут проверяет новые входящие транзакции. При обнаружении — отправляет уведомление в чат.

## Tronscan API
- TRX transactions: `https://apilist.tronscan.org/api/transaction`
- TRC-20 transfers: `https://apilist.tronscan.org/api/token_trc20/transfers`
- Balance: `https://apilist.tronscan.org/api/account`
- Free, no API key required
