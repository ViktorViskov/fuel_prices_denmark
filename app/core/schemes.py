from typing import Union
from typing import Tuple
from datetime import datetime
from datetime import date
from dataclasses import dataclass

@dataclass
class FuelPricesList:
    # Model for represend price list from one fuel seller.
    seller: str
    g_92: Union[float, None]
    g_95: Union[float, None]
    g_100: Union[float, None]
    d: Union[float, None]
    d_plus: Union[float, None]


@dataclass
class Storage:
    current_day_of_week: int = date.today().weekday()
    current_prices: Tuple[FuelPricesList] = ()
    yesterday_prices: Tuple[FuelPricesList] = ()
    last_update_time: datetime = None

@dataclass
class FuelPriceListWithHistory(FuelPricesList):
    g_92_diff: Union[float, None] = None
    g_95_diff: Union[float, None] = None
    g_100_diff: Union[float, None] = None
    d_diff: Union[float, None] = None
    d_plus_diff: Union[float, None] = None