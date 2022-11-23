from requests import request
from typing import Union

from bs4 import BeautifulSoup

from app.core.schemes import FuelPricesList

_COMPANY_NAME = "INGO"
_LINK = "https://www.ingo.dk/br%C3%A6ndstofpriser/aktuelle-br%C3%A6ndstofpriser"


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
        tag_list = bs.find_all(class_="views-field views-field-price-gross")

        g95 = tag_list[1].text.strip().split(": ")[1].replace(",", ".")
        g100 = tag_list[3].text.strip().split(": ")[1].replace(",", ".")
        d = tag_list[2].text.strip().split(": ")[1].replace(",", ".")
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
