# MT5 Telegram Alerting

A simple program that integrates with MetaTrader 5 (MT5) to alert a Telegram group about entries.

## Features

- Alerts for new entries
- Alerts for partial closures
- Alerts for full closures
- Supports multiple entries BUT one symbol at a time. This can be changed but is not suitable for my usage

## Requirements

- Python
- uv package manager
- MetaTrader 5
- Telegram group, bot token and chat ID (ask ChatGPT to set that up)

## Setup & Usage

1. Create a credentials YAML file with your Telegram bot&group and MT5 account details:

```yaml
TELEGRAM_BOT_TOKEN: "123456789:AAAbbbCCCdddEEEfffGGGhhhIIIjjjKKKlllMMM"
TELEGRAM_CHAT_ID: -611111111111
ACCOUNT_NUMBER: 91111111
ACCOUNT_PASSWORD: "81111111"
ACCOUNT_SERVER: "FTMO-Demo"
SYMBOL: "EURUSD"
```

2. Install dependencies:
    ```bash
    uv sync
    ```

2. Compile `main.py` using [PyInstaller](https://pyinstaller.org/):
   ```bash
   pyinstaller --onefile main.py
   ```
3. Run the compiled executable.

## Developer Info

### Format of `mt5.positions_get()`

Returns a tuple of `TradePosition` objects:

```python
TradePosition(
    ticket=189189,
    time=891894,
    time_msc=849489489489,
    time_update=45648948949,
    time_update_msc=89484948,
    type=1,
    magic=0,
    identifier=486456489,
    reason=0,
    volume=1.0,
    price_open=1.111111,
    sl=0.0,
    tp=0.0,
    price_current=1.11111,
    swap=0.0,
    profit=1.0,
    symbol='EURUSD',
    comment='',
    external_id=''
)
```

#### Example: Partial Closure

Before:
```python
TradePosition(
    ticket=67531693,
    ...
    volume=1.0,
    profit=-4.0,
    ...
)
```
After:
```python
TradePosition(
    ticket=67531693,
    ...
    volume=0.5,
    profit=-2.0,
    ...
)
```

### Note
Status of a closed position is an aproximation with the last tick info. MT5 won't allow you access
to closed positions' details immediately when they close, so the status is based on the last known tick data and to which
point it's the closest to (TP, SL or BE). This is the reason why there's faulty results for fully closed positions without
reaching TP or SL. Which you shouldn't be doing anyway ;)
