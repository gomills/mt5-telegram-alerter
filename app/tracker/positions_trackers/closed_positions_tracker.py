from logging import Logger
from typing import Any

from app.telegram_alerting.closed_position_alerting import send_position_closed_to_telegram


def closed_positions_tracker(
    open_mt5_positions: Any | None,
    logger: Logger,
    open_positions: dict,
    closed_positions: dict,
    telegram_bot_token: str,
    telegram_chat_id: int,
) -> None:
    """
    Tracks and identifies closed positions by comparing current MT5 positions with tracked positions.
    
    Routes to appropriate handler based on whether MT5 positions are currently open.

    Arguments:
        open_mt5_positions (Any | None): Current open positions from MT5 terminal
        logger (Logger): Logger instance for recording operations
        open_positions (dict): Dictionary of currently tracked open positions
        closed_positions (dict): Dictionary of tracked closed positions
        telegram_bot_token (str): Telegram bot token for notifications
        telegram_chat_id (int): Telegram chat ID for sending messages

    Returns:
        None
    """
    if not open_positions:
        return
    else:
        if not open_mt5_positions:
            return _handle_without_open_positions(
                logger=logger,
                open_positions=open_positions,
                closed_positions=closed_positions,
                telegram_bot_token=telegram_bot_token,
                telegram_chat_id=telegram_chat_id,
            )

        else:
            return _handle_with_open_positions(
                open_mt5_positions=open_mt5_positions,
                logger=logger,
                open_positions=open_positions,
                closed_positions=closed_positions,
                telegram_bot_token=telegram_bot_token,
                telegram_chat_id=telegram_chat_id,
            )


def _handle_without_open_positions(
    logger: Logger,
    open_positions: dict,
    closed_positions: dict,
    telegram_bot_token: str,
    telegram_chat_id: int,
):
    """
    Handles position tracking when no MT5 positions are currently open.
    
    Assumes all tracked positions are closed and sends notifications for unclosed positions.
    Clears both open and closed position dictionaries after processing.

    Arguments:
        logger (Logger): Logger instance for recording operations
        open_positions (dict): Dictionary of currently tracked open positions
        closed_positions (dict): Dictionary of tracked closed positions
        telegram_bot_token (str): Telegram bot token for notifications
        telegram_chat_id (int): Telegram chat ID for sending messages

    Returns:
        None
    """
    for position_id in open_positions.keys():
        if position_id not in closed_positions:
            send_position_closed_to_telegram(
                open_positions[position_id],
                telegram_bot_token,
                telegram_chat_id,
                logger,
            )

    # Clear the tracked positions once all have been handled
    open_positions.clear()
    closed_positions.clear()
    return


def _handle_with_open_positions(
    open_mt5_positions: Any,
    logger: Logger,
    open_positions: dict,
    closed_positions: dict,
    telegram_bot_token: str,
    telegram_chat_id: int,
):
    """
    Handles position tracking when MT5 positions are currently open. Needs special scenario
    because of possible partial positions, which are taken care in the open_positions_tracker.py
    
    Compares tracked positions with current MT5 positions to identify newly closed positions.
    Sends Telegram notifications for positions that are no longer open in MT5.

    Arguments:
        open_mt5_positions (Any): Current open positions from MT5 terminal
        logger (Logger): Logger instance for recording operations
        open_positions (dict): Dictionary of currently tracked open positions
        closed_positions (dict): Dictionary of tracked closed positions
        telegram_bot_token (str): Telegram bot token for notifications
        telegram_chat_id (int): Telegram chat ID for sending messages

    Returns:
        None
    """

    # Save the MT5 open positions id's
    currently_open_positions_ids = set()
    for mt5_position in open_mt5_positions:
        currently_open_positions_ids.add(mt5_position.identifier)

    for position_id in open_positions.keys():
        if position_id not in currently_open_positions_ids and position_id not in closed_positions:
            closed_positions[position_id] = open_positions[position_id]
            send_position_closed_to_telegram(
                closed_positions[position_id],
                telegram_bot_token,
                telegram_chat_id,
                logger,
            )
