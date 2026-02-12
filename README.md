# MT5 Telegram Alerting

Script that alerts a Telegram group of opened, closed, partially closed and break evened MT5 entries.

## Setup & Usage

1. Modify app/config.py with Telegram bot&group and MT5 account details:

```python
MT5_NUMBER = 9999999999
MT5_PASSWORD = "XXXXXXXXX"
MT5_SERVER = "XXXXXXXXXXX"
TELEGRAM_BOT_TOKEN = "123456789:AAAbbbCCCdddEEEfffGGGhhhIIIjjjKKKlllMMM"
TELEGRAM_CHAT_ID = "-999999999"
```

2. Modify app's logging as well as app/config.py Telegram messages to suit your needs

3. Run main.py

I suggest to use a Windows 11 VPS with Python3 and MetaTrader5 terminal installed for high availability.

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
point it's the closest to (TP, SL or BE).
