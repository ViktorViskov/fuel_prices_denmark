from os import popen
from typing import Union

from requests import request
from PIL import Image
from PIL import ImageOps
from PIL.Image import Image as Image_
from bs4 import BeautifulSoup

from app.core.schemes import FuelPricesList

_COMPANY_NAME = "GOON"
_LINK = "https://goon.nu/priser/#Aktuellepumpepriser"
_PATH_TO_TEMP_FOLDER = "/tmp"


def _load_html() -> Union[str, None]:
    try:
        return request("GET", _LINK).text
    except Exception:
        print("%s: Request error" % (_COMPANY_NAME))
        return None


def _parse_image_link_from_html(html: str) -> Union[str, None]:
    try:
        bs = BeautifulSoup(html, "html.parser")
    except Exception:
        print("%s: Cant not parse html" % (_COMPANY_NAME))
        return None

    try:
        image_tag = bs.find(name="img", alt="priser")
        return image_tag['data-src']
    except Exception:
        print("%s: Cant not parse image url from html" % (_COMPANY_NAME))


def _load_image(link: str) -> Union[Image_, None]:
    try:
        response = request("GET", link, stream=True)
        img = Image.open(response.raw)
        return img
    except Exception as e:
        print(e)
        print("%s: Cant load image by link '%s'" % (_COMPANY_NAME, link))
        return None


def _cut_prices_from_image(img: Image_) -> None:
    # cutting prices (l,t,r,b) and preparation for ssorc application.
    # After preparation save files to temp folder in system
    prepared_image = ImageOps.invert(img.convert('L').point(
        lambda x: 255 if x > 0 else 0, '1'))

    prepared_image.crop((60, 176, 190, 224)).save(
        "%s/g92.jpg" % (_PATH_TO_TEMP_FOLDER))
    prepared_image.crop((60, 232, 190, 280)).save(
        "%s/g95.jpg" % (_PATH_TO_TEMP_FOLDER))
    prepared_image.crop((60, 289, 190, 337)).save(
        "%s/d.jpg" % (_PATH_TO_TEMP_FOLDER))


def _parse_price_from_images() -> Union[FuelPricesList, None]:
    try:
        g92 = popen("ssocr -d 5 -T %s/g92.jpg" %
                    (_PATH_TO_TEMP_FOLDER)).read().strip()
        parsed_g92 = float(g92)
    except Exception:
        print("%s: Can not parse g92 from ssocr")
        g92 = None

    try:
        g95 = popen("ssocr -d 5 -T %s/g95.jpg" %
                    (_PATH_TO_TEMP_FOLDER)).read().strip()
        parsed_g95 = float(g95)
    except Exception:
        print("%s: Can not parse g95 from ssocr")
        g95 = None

    try:
        d = popen("ssocr -d 5 -T %s/d.jpg" %
                  (_PATH_TO_TEMP_FOLDER)).read().strip()
        parsed_d = float(d)
    except Exception:
        print("%s: Can not parse d from ssocr")
        d = None
    return FuelPricesList(_COMPANY_NAME, parsed_g92, parsed_g95, None, parsed_d, None)


def get_prices():
    html = _load_html()
    img_link = _parse_image_link_from_html(html)
    img = _load_image(img_link)

    if img:
        _cut_prices_from_image(img)
        return _parse_price_from_images()
    else:
        return None
