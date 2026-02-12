from app.entries_tracking.entries_tracking.entry_info import EntryInfo
from app.config import CLOSED_POSITION_MESSAGE, PARTIAL_CLOSE_MESSAGE
from app.telegram_service.sending_retry import send_telegram_request
from app.telegram_service.tp_relation import format_price


def send_position_closed_to_telegram(
    entry_info: EntryInfo,
    tick: float | None,
    telegram_bot_token: str,
    telegram_chat_id: str,
) -> str:
    """alerts of a closed position and its information to given telegram group"""

    # get outcome string
    if entry_info.profit_sign == 1:
        outcome = "$TP$"
    elif entry_info.profit_sign == -1:
        outcome = "SL"
    else:
        outcome = "BE"

    # fill all placeholders with entry's info
    message = CLOSED_POSITION_MESSAGE
    message = message.replace("{symbol}", entry_info.symbol)
    message = message.replace("{position_type}", entry_info.position_type)
    message = message.replace("{price}", format_price(entry_info.price))
    message = message.replace("{close_price}", format_price(tick))
    message = message.replace("{outcome}", outcome)

    # send message
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    return send_telegram_request(url, payload)


def send_partial_close_to_telegram(
    entry_info: EntryInfo,
    closure_proportion: float,
    last_partial_price: float | None,
    telegram_bot_token: str,
    telegram_chat_id: str,
) -> str:
    """alerts of a partially closed position and its information to given telegram group"""

    # fill all placeholders with entry's info
    message = PARTIAL_CLOSE_MESSAGE
    message = message.replace("{symbol}", entry_info.symbol)
    message = message.replace("{price}", format_price(entry_info.price))
    message = message.replace("{level}", format_price(last_partial_price))
    message = message.replace(
        "{closure_proportion}", str(round((closure_proportion * 100)))
    )

    # send message
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    return send_telegram_request(url, payload)
