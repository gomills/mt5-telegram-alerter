from dataclasses import dataclass
from typing import Literal


@dataclass
class EntryInfo:
    id: str
    position_type: Literal["COMPRA", "VENTA"]
    symbol: str
    volume: float
    profit_sign: Literal[-1, 0, 1]
    price: float
    initial_sl: float
    tp: float
    sl: float
