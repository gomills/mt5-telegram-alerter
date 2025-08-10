from logging import Logger
from typing import Any

from app.tracker.positions_trackers.closed_positions_tracker import closed_positions_tracker 
from app.tracker.positions_trackers.open_positions_tracker import open_position_tracker

def handle_positions(
    open_mt5_positions: Any | None,
    tick: Any | None,
    logger: Logger,
    open_positions: dict,
    closed_positions: dict,
    telegram_bot_token: str,
    telegram_chat_id: int,
    ):

    # If there's currently open positions in the terminal, check if they are new or have partial closures
    if open_mt5_positions:
        for position in open_mt5_positions:
            open_position_tracker(
                mt5_position=position,
                tick=tick,
                logger=logger,
                open_positions=open_positions,
                telegram_bot_token=telegram_bot_token,
                telegram_chat_id=telegram_chat_id
            )

    # If we have tracked open positions that are not in open_mt5_positions, means they are closed
    closed_positions_tracker(
        open_mt5_positions=open_mt5_positions,
        logger=logger,
        open_positions=open_positions,
        closed_positions=closed_positions,
        telegram_bot_token=telegram_bot_token,
        telegram_chat_id=telegram_chat_id
    )
