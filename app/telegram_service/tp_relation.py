from app.entries_tracking.entries_tracking.entry_info import EntryInfo


def format_price(price: float | None) -> str:
    """
    Formats a price for display.
    Uses 5 decimals if price < 10, otherwise no decimals.
    Returns "n/a" if price is None.
    """
    if not price:
        return "n/a"

    decimals = 5 if price < 10 else 0

    return str(round(price, decimals))


def get_tp_relation(entry_info: EntryInfo) -> float:
    """
    Returns the relation of the TP according to SL and TP placement when an entry is recently opened.
    Example: for SL = 0; price = 1; TP = 2; returns 2.0
    """

    entry_price = entry_info.price
    sl = entry_info.sl
    tp = entry_info.tp

    raw_sl_distance = abs(sl - entry_price)
    raw_tp_distance = abs(tp - entry_price)

    return round((raw_tp_distance / raw_sl_distance) if raw_sl_distance > 0 else 0, 1)
