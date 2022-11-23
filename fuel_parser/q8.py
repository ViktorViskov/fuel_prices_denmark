from typing import Union
from json import loads

from requests import request

from app.core.schemes import FuelPricesList

_COMPANY_NAME = "Q8"
_LINK = "https://www.q8.dk/-/api/PriceViewProduct/GetPriceViewProducts"
_REQUEST_HEADER = {"Content-Type": "text/html"}
_REQUEST_DATA = """{"FuelsIdList": [
  {
      "ProductCode": "22251",
      "Index": 0
  },
  {
      "ProductCode": "22601",
      "Index": 1
  },
  {
      "ProductCode": "24451",
      "Index": 2
  },
  {
      "ProductCode": "24337",
      "Index": 3
  }
]}"""


def _load_json() -> Union[str, None]:
    try:
        return request("POST", _LINK, headers=_REQUEST_HEADER, data=_REQUEST_DATA).text
    except Exception:
        print("%s: Request error" % (_COMPANY_NAME))
        return None


def _parse_from_json(json: str) -> Union[FuelPricesList, None]:
    try:
        fuel_price_dict = loads(json)["Products"]
    except Exception:
        print("%s: Json converting error" % (_COMPANY_NAME))
        return None

    try:
        # searching object by fuel name and parse price to float
        g95 = next(
            (fuel for fuel in fuel_price_dict if fuel["Name"] == "GoEasy 95 E10"), None)
        parsed_g95 = float(
            g95["PriceInclVATInclTax"].replace(",", "."))
    except:
        print("%s: Can not parse g95" % (_COMPANY_NAME))
        parsed_g95 = None

    try:
        # searching object by fuel name and parse price to float
        g100 = next(
            (fuel for fuel in fuel_price_dict if fuel["Name"] == "GoEasy 95 Extra E5"), None)
        parsed_g100 = float(
            g100["PriceInclVATInclTax"].replace(",", "."))
    except:
        print("%s: Can not parse g100" % (_COMPANY_NAME))
        parsed_g100 = None

    try:
        # searching object by fuel name and parse price to float
        d = next(
            (fuel for fuel in fuel_price_dict if fuel["Name"] == "GoEasy Diesel"), None)
        parsed_d = float(
            d["PriceInclVATInclTax"].replace(",", "."))
    except:
        print("%s: Can not parse d" % (_COMPANY_NAME))
        parsed_d = None

    try:
        # searching object by fuel name and parse price to float
        dp = next(
            (fuel for fuel in fuel_price_dict if fuel["Name"] == "GoEasy Diesel Extra"), None)
        parsed_dp = float(
            dp["PriceInclVATInclTax"].replace(",", "."))
    except:
        print("%s: Can not parse dp" % (_COMPANY_NAME))
        parsed_dp = None

    return FuelPricesList(_COMPANY_NAME, None, parsed_g95, parsed_g100, parsed_d, parsed_dp)


def get_prices() -> Union[FuelPricesList, None]:
    json = _load_json()

    if json:
        return _parse_from_json(json)
    else:
        return None
