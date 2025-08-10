from logging import Logger
import requests # type: ignore

def send_position_closed_to_telegram(
    entry_info: dict,
    telegram_bot_token: str,
    telegram_chat_id: int,
    logger: Logger
    ) -> None:


    position_type = "BUY" if entry_info['position_type'] == 0 else "SELL"

    if entry_info['profit_sign'] == "tp":  
        result = "$TP$"
    elif entry_info['profit_sign'] == "sl":
        result = "SL"
    else:
        result = "BE"

    message = f"""
*** Closed Trade | {entry_info['symbol']} ***
──────────────
> Type: {position_type}
> Entry Price: {entry_info['price']:.5f}
> Result: {result}
        """.strip()
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        logger.info(f"Telegram opening message response: {response.status_code}, Succes: {response.ok}...")
    except Exception as e:
        logger.info(f"Failed to send Telegram message: {e}")

def send_partial_close_to_telegram(
    entry_info: dict,
    closure_proportion: str,
    telegram_bot_token: str,
    telegram_chat_id: int,
    logger: Logger
    ) -> None:

    level = f"{entry_info['last_partial_price']:.5f}" if entry_info['last_partial_price'] else "N/A"

    message = f"""
* Partial Close | {entry_info['symbol']} *
────────────
> Level    : {level}
> Percent  : {closure_proportion}%
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