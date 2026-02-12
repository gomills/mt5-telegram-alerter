from app.telegram_service.tp_relation import get_tp_relation, format_price
from app.entries_tracking.entries_tracking.entry_info import EntryInfo
from app.telegram_service.sending_retry import send_telegram_request
from app.config import OPEN_POSITION_MESSAGE, SL_TO_BE_MESSAGE


def send_position_opened_to_telegram(
    entry_info: EntryInfo, telegram_bot_token: str, telegram_chat_id: str
) -> str:
    """sends an alert to the given telegram group that a position was opened"""

    # fill all placeholders with entry's info
    tp_relation = get_tp_relation(entry_info)

    message = OPEN_POSITION_MESSAGE
    message = message.replace("{symbol}", entry_info.symbol)
    message = message.replace("{position_type}", entry_info.position_type)
    message = message.replace("{price}", format_price(entry_info.price))
    message = message.replace("{tp}", format_price(entry_info.tp))
    message = message.replace("{sl}", format_price(entry_info.sl))
    message = message.replace(
        "{tp_relation}", str(tp_relation) if tp_relation > 0 else "n/a"
    )

    # send message
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    return send_telegram_request(url, payload)


def send_sl_to_be_to_telegram(
    entry_info: EntryInfo, telegram_bot_token: str, telegram_chat_id: str
) -> str:
    """sends an alert to the given telegram group that the SL was moved to breakeven"""

    # fill all placeholders with entry's info
    message = SL_TO_BE_MESSAGE
    message = message.replace("{symbol}", entry_info.symbol)
    message = message.replace("{price}", format_price(entry_info.price))

    # send message
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    return send_telegram_request(url, payload)
