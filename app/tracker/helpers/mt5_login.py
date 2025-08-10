from typing import Any
from logging import Logger

def initialize_metatrader(mt5: Any, credentials_dict: dict, logger: Logger) -> bool:
    """
    Initializes and logs into MetaTrader 5 terminal.

    Parameters:
        credentials_dict (dict): user input credentials (Telegram and MT5)
        logger (logging.Logger): Logger instance for error reporting

    Returns:
        bool: True if initialization and login successful, False otherwise
    """
    mt5.initialize()
    if not mt5.initialize():
        logger.info(f"Failed to connect to terminal: {mt5.last_error()}")
        return False

    authorized = mt5.login(
        credentials_dict["TRADING_ACCOUNT_NUMBER"],
        password=credentials_dict["TRADING_ACCOUNT_PASSWORD"],
        server=credentials_dict["TRADING_ACCOUNT_SERVER"],
    )
    if not authorized:
        logger.info(f"Failed to login: {mt5.last_error()}")
        return False

    return True