import MetaTrader5 as mt5  # type: ignore
from typing import Any
import logging
import time

from app.tracker.positions_trackers.generic_positions_tracker import handle_positions
from app.tracker.helpers.user_input import ask_for_input, parse_yaml_file
from app.tracker.helpers.mt5_login import initialize_metatrader
from app.tracker.helpers.logger_setup import initialize_logger


def initialize_alerter():
    """
    Initializes and runs the MT5 position alerting system.
    
    This is the main entry point that sets up logging and starts the user input gathering process.

    Arguments:
        None

    Returns:
        None: Function returns the result of _gather_user_input()
    """

    # Initialize program's logger
    logger = initialize_logger()

    print(
"""\n
|¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬|
|MT5 TELEGRAM ALERTER by gomills|
|¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬|\n"""
    )

    return _gather_user_input(logger)


def _gather_user_input(logger: logging.Logger):
    """
    Gathers user credentials and establishes MT5 connection.
    
    Continuously prompts user for credentials until successful MT5 login is achieved.
    Handles keyboard interrupts gracefully by shutting down MT5 connection.

    Arguments:
        logger (logging.Logger): Logger instance for recording operations

    Returns:
        None: Function returns the result of _tracker_loop() on success, or None on KeyboardInterrupt
    """
    # Gather user input and keep trying until we manage to connect to MT5 account
    credentials_dict: dict[str, Any] = {}
    mt5_login_success = None
    attempt_number = 1

    try:

        while not credentials_dict or not mt5_login_success:
            credentials_path = ask_for_input(attempt_number)
            print("")
            credentials_dict = parse_yaml_file(credentials_path, logger)
            if not credentials_dict:
                attempt_number += 1
                continue

            mt5_login_success = initialize_metatrader(mt5, credentials_dict, logger)
            if not mt5_login_success:
                logger.info("Failed MT5 login. Check your credentials/network")
            
            continue

        return _tracker_loop(credentials_dict, logger)

    except KeyboardInterrupt:
        mt5.shutdown()
        return print("\n<>zZZ MT5 Telegram Alerter going to sleep zZZ<>")


def _tracker_loop(credentials_dict: dict, logger: logging.Logger):
    """
    Main tracking loop that continuously monitors MT5 positions.
    
    Initializes position tracking dictionaries and runs an infinite loop to check for position changes.
    Note: This function runs indefinitely until interrupted by KeyboardInterrupt

    Arguments:
        credentials_dict (dict): Dictionary containing MT5 and Telegram credentials
        logger (logging.Logger): Logger instance for recording operations

    Returns:
        None: Function runs indefinitely in a loop
    """
    # Here we store the tracked positions (check README.md to check the structure and format of an open/closed position)
    open_positions: dict = {}
    closed_positions: dict = {}

    # Initialize loop to check constantly for MT5 terminal positions
    logger.info("Recording entries...")
    while True:

        _check_for_positions_iteration(
            credentials_dict=credentials_dict,
            logger=logger,
            open_positions=open_positions,
            closed_positions=closed_positions,
        )

        time.sleep(2)


def _check_for_positions_iteration(
    credentials_dict: dict,
    logger: logging.Logger,
    open_positions: dict,
    closed_positions: dict,
) -> None:
    """
    Checks MT5 for position changes and handles position tracking.

    Parameters:
        credentials_dict (dict): Trading and Telegram credentials
        open_positions (dict): Currently tracked open positions
        closed_positions (dict): Currently tracked closed positions

    Returns:
        None
    """

    # Get latest MT5 open positions and tick for symbol
    open_mt5_positions = mt5.positions_get(symbol=credentials_dict["SYMBOL"])
    tick = mt5.symbol_info_tick(credentials_dict["SYMBOL"])

    handle_positions(
        open_mt5_positions=open_mt5_positions,
        tick=tick,
        logger=logger,
        open_positions=open_positions,
        closed_positions=closed_positions,
        telegram_bot_token=credentials_dict["TELEGRAM_BOT_TOKEN"],
        telegram_chat_id=credentials_dict["TELEGRAM_CHAT_ID"],
    )