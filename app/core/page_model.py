from typing import List

from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.core.schemes import Storage
from app.core.schemes import FuelPriceListWithHistory


class PageModel:
    def main_page(req: Request, storage: Storage, view: Jinja2Templates):
        current_prices = storage.current_prices
        yesterday_prices = storage.yesterday_prices
        current_prices_with_history: List[FuelPriceListWithHistory] = []

        for current_price in current_prices:
            if current_price:
                price_with_history = FuelPriceListWithHistory(seller=current_price.seller, g_92=current_price.g_92,
                                                              g_95=current_price.g_95, g_100=current_price.g_100, d=current_price.d, d_plus=current_price.d_plus)

                yesterday_price = next(
                    (y_price for y_price in yesterday_prices if y_price and current_price.seller == y_price.seller), None)

                try:
                    if yesterday_price:
                        if yesterday_price.g_92 and current_price.g_92:
                            price_with_history.g_92_diff = round(current_price.g_92 - yesterday_price.g_92, 1)
                        if yesterday_price.g_95 and current_price.g_95:
                            price_with_history.g_95_diff = round(current_price.g_95 - yesterday_price.g_95, 1)
                        if yesterday_price.g_100 and current_price.g_100:
                            price_with_history.g_100_diff = round(current_price.g_100 - yesterday_price.g_100, 1)
                        if yesterday_price.d and current_price.d:
                            price_with_history.d_diff = round(current_price.d - yesterday_price.d, 1)
                        if yesterday_price.d_plus and current_price.d_plus:
                            price_with_history.d_plus_diff = round(current_price.d_plus - yesterday_price.d_plus, 1)
                except Exception:
                    print("%s: Error with define price different" % (current_price.seller))
                    
                current_prices_with_history.append(price_with_history)

            else:
                continue

        return view.TemplateResponse("main.jinja", {"request": req, "s": current_prices_with_history, "last_update_time": str(storage.last_update_time).split(".")[0]})
