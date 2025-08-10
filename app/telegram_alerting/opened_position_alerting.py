from logging import Logger
import requests # type: ignore


def send_position_opened_to_telegram(
    entry_info: dict,
    telegram_bot_token: str,
    telegram_chat_id: int,
    logger: Logger
    ) -> None:

    position_type = "BUY" if entry_info['position_type'] == 0 else "SELL"

    tp_relation = _get_tp_relation(entry_info)

    message = f"""
*** New Trade | {entry_info['symbol']} ***
──────────────
> Type: {position_type}
> Price: {entry_info['price']:.5f}
> Take Profit: {entry_info['tp']:.5f}
> Stop Loss: {entry_info['sl']:.5f}
> Ratio: 1:{tp_relation}
        """.strip()
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        logger.info(f"Telegram opening message response: {response.status_code}, Success: {response.ok}...")
    except Exception as e:
        logger.info(f"Failed to send Telegram message: {e}")

def _get_tp_relation(entry_info: dict) -> float:

    entry_price = entry_info['price']
    sl = entry_info['sl']
    tp = entry_info['tp']

    raw_sl_distance = abs(sl - entry_price)
    raw_tp_distance = abs(tp - entry_price)

    return round((raw_tp_distance / raw_sl_distance), 1)
