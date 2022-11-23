from requests import request
from typing import Union
from bs4 import BeautifulSoup

from app.core.schemes import FuelPricesList

_COMPANY_NAME = "OK"
_LINK = "https://www.ok.dk/offentlig/produkter/braendstof/priser/vejledende-standerpriser"


def _load_html() -> Union[str, None]:
    try:
        return request("GET", _LINK).text
    except Exception:
        print("%s: Can not make requst to %s" % (_COMPANY_NAME, _LINK))
        return None


def _parse_prices_from_html(html_page: str) -> Union[FuelPricesList, None]:

    # parsing string from html tags
    try:
        bs = BeautifulSoup(html_page, "html.parser")
        g95 = bs.find(id="b43a7bead4f7493988aea7f7f98c0772").find(
            class_="flex-table__cell cell--val hidden-xs").text.strip().replace(" kr.", "").replace(",", ".")
        g100 = bs.find(id="8016cc45ece542508ab4fb0e109937fe").find(
            class_="flex-table__cell cell--val hidden-xs").text.strip().replace(" kr.", "").replace(",", ".")
        d = bs.find(id="c67c3750caac4293b591c23527ab4fc9").find(
            class_="flex-table__cell cell--val hidden-xs").text.strip().replace(" kr.", "").replace(",", ".")

    except Exception:
        print("%s: Html parsing error" % (_COMPANY_NAME))
        return None

    try:
        parsed_g95 = float(g95)

    except Exception:
        print("%s: Can not parse '%s' to g95" % (_COMPANY_NAME, g95))
        parsed_g95 = None

    try:
        parsed_g100 = float(g100)

    except Exception:
        print("%s: Can not parse '%s' to g100" % (_COMPANY_NAME, g100))
        parsed_g100 = None

    try:
        parsed_d = float(d)

    except Exception:
        print("%s: Can not parse '%s' to d" % (_COMPANY_NAME, d))
        parsed_d = None

    return FuelPricesList(_COMPANY_NAME, None, parsed_g95, parsed_g100, parsed_d, None)


def get_prices() -> Union[FuelPricesList, None]:
    html_page = _load_html()

    if html_page:
        return _parse_prices_from_html(html_page)

    else:
        return None
