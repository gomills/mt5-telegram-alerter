import MetaTrader5 as mt5  # type: ignore
import logging
import time

from app.entries_tracking.mt5_api.credentials import get_credentials, Credentials
from app.telegram_service.closed_position import send_position_closed_to_telegram
from app.entries_tracking.mt5_api.mt5_login import initialize_metatrader
from app.entries_tracking.entries_tracking.entry_info import EntryInfo
from app.entries_tracking.entries_tracking.tracked_entries import (
    evaluate_current_mt5_entry,
)
from app.entries_tracking.logger.logger import initialize_logger
from app.config import INIT_BANNER


def initialize_alerter():
    """
    Initializes the MT5 position alerting system
    """

    # initialize program's logger
    logger = initialize_logger()

    # print initial banner
    logger.info(INIT_BANNER)

    # get credentials and try to connect to terminal with a retry mechanism
    credentials: Credentials = get_credentials()

    login_success = False
    attempt_number = 1

    while (not login_success) and (attempt_number < 4):
        if attempt_number != 1:
            logger.error(">>> retrying connection...")

        try:
            initialize_metatrader(mt5=mt5, credentials=credentials, logger=logger)
            logger.info(">>> successfully connected to MT5 terminal")
            login_success = True
        except Exception as e:
            logger.error(f">>> logging in error 👎: {str(e)}")
            time.sleep(2)
            continue
        finally:
            attempt_number += 1

    if login_success:
        logger.info(">>> APRETAR Ctrl+C PARA CERRAR PROGRAMA")
        return _tracker_loop(credentials, logger)
    else:
        logger.info(">>> closing program due to error 👋")
        time.sleep(2)


def _tracker_loop(credentials: Credentials, logger: logging.Logger):
    """
    Main tracking loop that continuously monitors MT5 positions.

    Initializes position tracking storage and runs an infinite loop to check for position changes.
    Note: This function runs indefinitely until interrupted by KeyboardInterrupt
    """

    # store the tracked positions
    open_entries: dict[str, EntryInfo] = {}
    closed_entries: set[str] = set()

    # enter loop to constantly check for MT5 terminal positions
    # (check README.md to check the structure and format of an open/partially_closed position)
    logger.info(">>> recording entries 👍")
    try:
        while True:
            _retrieve_entries_iteration(
                credentials=credentials,
                logger=logger,
                open_entries=open_entries,
                closed_entries=closed_entries,
            )

            time.sleep(2)
    except KeyboardInterrupt:
        logger.info(">>> stopping entries recording, good bye 👋")
        time.sleep(2)
    except Exception as e:
        logger.info(f">>> unexpected error occured 👎: {str(e)}")
        time.sleep(4)


def _retrieve_entries_iteration(
    credentials: Credentials,
    logger: logging.Logger,
    open_entries: dict[str, EntryInfo],
    closed_entries: set[str],
) -> None:
    """
    Retrieves current entries from MT5 terminal and manages each for respective entry tracking.
    """

    # get latest MT5 open entries
    open_mt5_entries = mt5.positions_get()  # type: ignore

    # iterate over the current mt5 entries to find new or partially closed ones
    for ps in open_mt5_entries:
        evaluate_current_mt5_entry(
            open_mt5_position=ps,
            closed_entries=closed_entries,
            open_entries=open_entries,
            credentials=credentials,
            logger=logger,
        )

    # now we have to check our stored open entries if they've been totally closed already
    to_pop = []
    for open_entry_id in open_entries.keys():
        is_currently_open = False

        for mt5_position in open_mt5_entries:
            if mt5_position.identifier == open_entry_id:
                is_currently_open = True
                break

        # it was closed. Add it to the to_pop record
        if not is_currently_open:
            to_pop.append(open_entry_id)

    # remove it from the open entries and add it to the closed ones
    for entry_id in to_pop:
        entry_info = open_entries[entry_id]
        open_entries.pop(entry_id, None)
        closed_entries.add(entry_id)

        # try to get current tick
        tick_data = mt5.symbol_info_tick(entry_info.symbol)  # type: ignore
        tick = None

        if tick_data:
            try:
                if tick_data.bid:
                    tick = tick_data.bid
                elif tick_data.ask:
                    tick = tick_data.ask
            except Exception:
                pass

        result = send_position_closed_to_telegram(
            entry_info=entry_info,
            tick=tick,
            telegram_bot_token=credentials.telegram_bot_token,
            telegram_chat_id=credentials.telegram_chat_id,
        )

        logger.info(f">>> sent tg message: {result}")
