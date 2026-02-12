import MetaTrader5 as mt5  # type: ignore
from typing import Any

from app.entries_tracking.entries_tracking.entry_info import EntryInfo
from app.entries_tracking.mt5_api.credentials import Credentials
from app.telegram_service.closed_position import (
    send_partial_close_to_telegram,
)
from app.telegram_service.open_position import (
    send_position_opened_to_telegram,
    send_sl_to_be_to_telegram,
)


def evaluate_current_mt5_entry(
    open_mt5_position: Any,
    closed_entries: set[str],
    open_entries: dict[str, EntryInfo],
    credentials: Credentials,
    logger: Any
) -> None:
    """receives a currently open MT5 entry and continues action if it's either new or partially closed"""

    # get entry info
    id = open_mt5_position.identifier
    position_type = "VENTA" if open_mt5_position.type == 1 else "COMPRA"
    symbol = open_mt5_position.symbol
    volume = open_mt5_position.volume
    price = open_mt5_position.price_open
    tp = open_mt5_position.tp
    sl = open_mt5_position.sl

    # try to get current tick
    tick_data = mt5.symbol_info_tick(symbol)  # type: ignore
    tick = None

    if tick_data:
        try:
            if tick_data.bid:
                tick = tick_data.bid
            elif tick_data.ask:
                tick = tick_data.ask
        except Exception:
            pass

    # it has been closed already
    if id in closed_entries:
        return

    # we're tracking it already, have to check if partial closure and update its profit sign
    elif id in open_entries.keys():
        _handle_tracked_entry(
            open_entries=open_entries,
            entry_id=id,
            tick=tick,
            current_volume=volume,
            current_sl=sl,
            credentials=credentials,
            logger=logger
        )

    # it's new, add it to the list and alert through telegram
    else:
        entry_info = EntryInfo(
            id=id,
            position_type=position_type,
            symbol=symbol,
            volume=volume,
            profit_sign=0,
            price=price,
            initial_sl=sl,
            tp=tp,
            sl=sl,
        )

        open_entries[id] = entry_info

        result = send_position_opened_to_telegram(
            entry_info=entry_info,
            telegram_bot_token=credentials.telegram_bot_token,
            telegram_chat_id=credentials.telegram_chat_id,
        )

        logger.info(f">>> sent tg message: {result}")


def _handle_tracked_entry(
    open_entries: dict[str, EntryInfo],
    entry_id: str,
    tick: float | None,
    current_volume: float,
    current_sl: float,
    credentials: Credentials,
    logger: Any
) -> None:
    """Handle updates to an already tracked entries (partial closes, SL to BE and profit signs)"""

    # get current entry from the open entries record
    entry_info = open_entries[entry_id]

    # update profit sign according to which level tick is closest
    if tick:
        dist_from_tp = abs(tick - entry_info.tp)
        dist_from_sl = abs(tick - entry_info.initial_sl)
        dist_from_price = abs(tick - entry_info.price)

        if dist_from_tp < dist_from_sl and dist_from_tp < dist_from_price:
            entry_info.profit_sign = 1  # moving towards TP
        elif dist_from_sl < dist_from_tp and dist_from_sl < dist_from_price:
            entry_info.profit_sign = -1  # moving towards SL
        else:
            entry_info.profit_sign = 0  # at breakeven

    # check for partial closure (volume decreased)
    if current_volume < entry_info.volume:
        result = send_partial_close_to_telegram(
            entry_info=entry_info,
            closure_proportion=1 - current_volume / entry_info.volume,
            last_partial_price=tick,
            telegram_bot_token=credentials.telegram_bot_token,
            telegram_chat_id=credentials.telegram_chat_id,
        )
        entry_info.volume = current_volume

        logger.info(f">>> sent tg message: {result}")

    # check for SL move to BE
    if current_sl != entry_info.sl:
        result = send_sl_to_be_to_telegram(
            entry_info=entry_info,
            telegram_bot_token=credentials.telegram_bot_token,
            telegram_chat_id=credentials.telegram_chat_id,
        )
        entry_info.sl = current_sl
        
        logger.info(f">>> sent tg message: {result}")
