from requests import request
from typing import Union

from bs4 import BeautifulSoup

from app.core.schemes import FuelPricesList

_COMPANY_NAME = "CIRCLEK"
_LINK = "https://www.circlek.dk/priser"


def _load_html() -> Union[str, None]:
    try:
        return request("GET", _LINK).text
    except Exception:
        print("%s: Can not make requst to %s" % (_COMPANY_NAME, _LINK))
        return None


def _parse_prices_from_html(html_page: str) -> Union[FuelPricesList, None]:
    # parsing values from html tags
    try:
        bs = BeautifulSoup(html_page, "html.parser")

        tag_list = bs.find(class_="uk-table uk-table-striped uk-table-responsive cols-7").find_all(
            class_="views-field views-field-price-gross")

        g95 = tag_list[1].text.strip().split(": ")[1].replace(",", ".")
        g100 = tag_list[2].text.strip().split(": ")[1].replace(",", ".")
        d = tag_list[3].text.strip().split(": ")[1].replace(",", ".")
        dp = tag_list[4].text.strip().split(": ")[1].replace(",", ".")
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

    try:
        parsed_dp = float(dp)
    except Exception:
        print("%s: Can not parse '%s' to dp" % (_COMPANY_NAME, dp))
        parsed_dp = None

    return FuelPricesList(_COMPANY_NAME, None, parsed_g95, parsed_g100, parsed_d, parsed_dp)


def get_prices() -> Union[FuelPricesList, None]:
    html_page = _load_html()

    if html_page:
        return _parse_prices_from_html(html_page)

    else:
        return None
