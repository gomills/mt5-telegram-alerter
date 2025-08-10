from logging import Logger
from typing import Any

from app.telegram_alerting.opened_position_alerting import send_position_opened_to_telegram
from app.telegram_alerting.closed_position_alerting import send_partial_close_to_telegram


def open_position_tracker(
    mt5_position: Any,
    tick: Any | None,
    logger: Logger,
    open_positions: dict,
    telegram_bot_token: str,
    telegram_chat_id: int,
):
    """
    Tracks open positions and handles new position notifications or partial closures.
    
    Routes to appropriate handler based on whether the position is already being tracked.

    Arguments:
        mt5_position (Any): MT5 position object containing position details
        tick (Any | None): Current market tick data for the symbol
        logger (Logger): Logger instance for recording operations
        open_positions (dict): Dictionary of currently tracked open positions
        telegram_bot_token (str): Telegram bot token for notifications
        telegram_chat_id (int): Telegram chat ID for sending messages

    Returns:
        None: Function returns the result of notification functions
    """

    position_identifier = mt5_position.identifier

    # Position is already tracked. So, only check if there are partials and notify if yes
    if position_identifier in open_positions:
        return _handle_tracked_open_position(
            mt5_position,
            tick,
            logger,
            open_positions,
            telegram_bot_token,
            telegram_chat_id,
        )

    # Position is new. Just save it to open_positions and notify
    else:
        entry_info = {
            "price": mt5_position.price_open,
            "sl": mt5_position.sl,
            "tp": mt5_position.tp,
            "position_type": mt5_position.type,
            "symbol": mt5_position.symbol,
            "last_volume_after_partial": float(mt5_position.volume),
            "last_partial_price": 0,
            "initial_volume": float(mt5_position.volume),
            "last_volume": float(mt5_position.volume),
            "profit_sign": "be",
        }

        open_positions[position_identifier] = entry_info

        return send_position_opened_to_telegram(
            entry_info=entry_info,
            telegram_bot_token=telegram_bot_token,
            telegram_chat_id=telegram_chat_id,
            logger=logger,
        )


def _handle_tracked_open_position(
    mt5_position: Any,
    tick: Any | None,
    logger: Logger,
    open_positions: dict,
    telegram_bot_token: str,
    telegram_chat_id: int,
):
    """
    Handles updates for positions that are already being tracked.
    
    Updates position profit status and checks for partial closures.
    Sends Telegram notification if partial closure is detected.

    Arguments:
        mt5_position (Any): MT5 position object containing current position details
        tick (Any | None): Current market tick data for the symbol
        logger (Logger): Logger instance for recording operations
        open_positions (dict): Dictionary of currently tracked open positions
        telegram_bot_token (str): Telegram bot token for notifications
        telegram_chat_id (int): Telegram chat ID for sending messages

    Returns:
        None: Function may return the result of partial closure notification
    """
    entry_info = open_positions[mt5_position.identifier]

    _update_position_data(logger, entry_info, tick)

    # Check if we have a partial closure
    entry_info["last_volume"] = float(mt5_position.volume)

    if entry_info["last_volume"] < entry_info["last_volume_after_partial"]:
        closed_percentage = (
            abs(
                entry_info["last_volume"]
                - float(entry_info["last_volume_after_partial"])
            )
            / float(entry_info["initial_volume"])
            * 100
        )
        entry_info["last_volume_after_partial"] = entry_info["last_volume"]
        entry_info["last_partial_price"] = mt5_position.price_current

        closure_proportion_str = f"{round(closed_percentage)}"

        return send_partial_close_to_telegram(
            entry_info,
            closure_proportion_str,
            telegram_bot_token,
            telegram_chat_id,
            logger,
        )


def _update_position_data(logger: Logger, entry_info: dict, tick: Any | None):
    """
    Updates position profit status based on current market price proximity to TP, SL or BE.
    
    Calculates which level (take profit, stop loss, or breakeven) the current price is closest to
    and updates the profit_sign accordingly. Handles exceptions gracefully.

    Arguments:
        entry_info (dict): Dictionary containing position information including price, tp, sl
        tick (Any | None): Current market tick data containing bid and ask prices

    Returns:
        None: Function modifies entry_info dictionary in place
    """
    try:
        if not tick:
            return
        else:
            live_price = (tick.ask + tick.bid) / 2

            diff_map = {
                "tp": abs(live_price - entry_info["tp"]),
                "sl": abs(live_price - entry_info["sl"]),
                "be": abs(live_price - entry_info["price"]),
            }

            sorted_diff_map = sorted(diff_map.items(), key=lambda x: x[1])

            lowest_key = sorted_diff_map[0][0]

            entry_info["profit_sign"] = lowest_key

            return
    except Exception as e:
        logger.info(f"Error when updating position data: {str(e)[:50]}")
        return
