# MT5 and Telegram credentials
MT5_NUMBER = 9999999999
MT5_PASSWORD = "XXXXXXXXX"
MT5_SERVER = "XXXXXXXXXXX"
TELEGRAM_BOT_TOKEN = "123456789:AAAbbbCCCdddEEEfffGGGhhhIIIjjjKKKlllMMM"
TELEGRAM_CHAT_ID = "-999999999"

# Any placeholder (text between {}) must always be present. Other text may be modified.
CLOSED_POSITION_MESSAGE = """
*** Operación Cerrada | {symbol} ***
──────────────
> Tipo: {position_type}
> Entrada: {price}
> Cierre: {close_price}
> Resultado: {outcome}
──────────────
Custom signature
""".strip()

PARTIAL_CLOSE_MESSAGE = """
*** Parcial Cerrado | {symbol} ***
────────────
> Entrada: {price}
> Cierre: {level}
> Porcentaje: {closure_proportion}
────────────
Custom signature
""".strip()

SL_TO_BE_MESSAGE = """
*** SL movido a BE | {symbol} ***
────────────
> Entrada: {price}
> Stop Loss: {price}
────────────
Custom signature
""".strip()

OPEN_POSITION_MESSAGE = """
*** Nueva Operación | {symbol} ***
──────────────
> Tipo: {position_type}
> Entrada: {price}
> Take Profit: {tp}
> Stop Loss: {sl}
> Relación: 1:{tp_relation}
──────────────
Custom signature
""".strip()

INIT_BANNER = """
\n
|¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬|
|MT5 TELEGRAM ALERTER by github.com/gomills|
|¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬|
\n
"""
