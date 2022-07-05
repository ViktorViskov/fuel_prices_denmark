# stations
import subprocess

from pr.ok import OK_STATION
from pr.q8 import Q8_STATION
from pr.f24 import F24_STATION
from pr.circle import CIRCLE_STATION
from pr.ingo import INGO_STATION
from pr.goon import GOON_STATION

# load prices
def load_prices():
  # result
  data = {
    "OK":OK_STATION().get_prices(),
    "Q8":Q8_STATION().get_prices(),
    "F24":F24_STATION().get_prices(),
    "Circle":CIRCLE_STATION().get_prices(),
    "Ingo":INGO_STATION().get_prices(),
    "Goon":GOON_STATION().get_prices(),
  }

  return data