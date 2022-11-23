from typing import Tuple

from app.core.schemes import FuelPricesList
import fuel_parser.ok as ok
import fuel_parser.q8 as q8
import fuel_parser.f24 as f24
import fuel_parser.circlek as circlek
import fuel_parser.ingo as ingo
import fuel_parser.goon as goon


def load_prices() -> Tuple[FuelPricesList]:

    data = (
        ok.get_prices(),
        q8.get_prices(),
        f24.get_prices(),
        circlek.get_prices(),
        ingo.get_prices(),
        goon.get_prices(),
    )

    return data
