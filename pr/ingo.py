# libs
from requests import request
from bs4 import BeautifulSoup

# class to parse data from OK station
class INGO_STATION:
  # variables
  link = "https://www.ingo.dk/br%C3%A6ndstofpriser/aktuelle-br%C3%A6ndstofpriser"

  # method for load data
  def load(self):
    self.response = request("GET", self.link).text

  # method for parsing data
  def parse(self):
    # load ok prices
    bs = BeautifulSoup(self.response, "html.parser")

    # search tag
    self.raw = bs.find_all(class_="views-field views-field-price-gross")

    #  parsing prices
    self.b_95 = self.raw[1].text.strip().split(": ")[1]
    self.b_95p = self.raw[3].text.strip().split(": ")[1]
    self.d = self.raw[2].text.strip().split(": ")[1]

  # method for get prices
  def get_prices(self):
    try:
      # make request
      self.load()

      # parse
      self.parse()

      # result
      return {"95":self.b_95, "95+":self.b_95p, "d":self.d}
    
    # catch errors
    except:
      return {"95":"Err", "95+":"Err", "d":"Err"}
  