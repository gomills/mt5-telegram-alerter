from logging import Logger
from typing import Any

from app.entries_tracking.mt5_api.credentials import Credentials


def initialize_metatrader(mt5: Any, credentials: Credentials, logger: Logger) -> None:
    """
    Initializes and logs into MetaTrader 5 terminal.

    Raises exception on error.
    """

    mt5.initialize()
    if not mt5.initialize():
        raise Exception(f"failed to even connect to terminal: {mt5.last_error()}")

    authorized = mt5.login(
        credentials.mt5_number,
        password=credentials.mt5_password,
        server=credentials.mt5_server,
    )

    if not authorized:
        raise Exception(f"failed to login to terminal: {mt5.last_error()}")
