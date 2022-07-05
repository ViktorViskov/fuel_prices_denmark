# libs
from dataclasses import replace
from requests import request
from bs4 import BeautifulSoup

# class to parse data from OK station
class OK_STATION:
  # variables
  ok = "https://www.ok.dk/offentlig/produkter/braendstof/priser"

  # method for load data
  def load(self):
    self.response = request("GET", self.ok).text

  # method for parsing data
  def parse(self):
    # load ok prices
    bs = BeautifulSoup(self.response, "html.parser")
    self.ok_b95 = bs.find(id="b43a7bead4f7493988aea7f7f98c0772").find(class_="flex-table__cell cell--val hidden-xs").text.strip().replace(" kr.", "")
    self.ok_b100 = bs.find(id="8016cc45ece542508ab4fb0e109937fe").find(class_="flex-table__cell cell--val hidden-xs").text.strip().replace(" kr.", "")
    self.ok_d = bs.find(id="c67c3750caac4293b591c23527ab4fc9").find(class_="flex-table__cell cell--val hidden-xs").text.strip().replace(" kr.", "")

  # method for get prices
  def get_prices(self):
    try:
      # make request
      self.load()

      # parse
      self.parse()

      # result
      return {"95":self.ok_b95, "100":self.ok_b100, "d":self.ok_d}
    
    # catch errors
    except:
      return {"95":"Err","100":"Err", "d":"Err"}
  