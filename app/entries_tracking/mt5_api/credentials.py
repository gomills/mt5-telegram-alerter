from dataclasses import dataclass

from app.config import (
    MT5_NUMBER,
    MT5_PASSWORD,
    MT5_SERVER,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)


@dataclass
class Credentials:
    telegram_bot_token: str
    telegram_chat_id: str
    mt5_number: int
    mt5_password: str
    mt5_server: str


def get_credentials() -> Credentials:
    return Credentials(
        mt5_number=MT5_NUMBER,
        mt5_password=MT5_PASSWORD,
        mt5_server=MT5_SERVER,
        telegram_bot_token=TELEGRAM_BOT_TOKEN,
        telegram_chat_id=TELEGRAM_CHAT_ID,
    )
