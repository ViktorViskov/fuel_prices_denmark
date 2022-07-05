# libs
from requests import request
from bs4 import BeautifulSoup

# class to parse data from OK station
class CIRCLE_STATION:
  # variables
  link = "https://www.circlek.dk/priser"

  # method for load data
  def load(self):
    self.response = request("GET", self.link).text

  # method for parsing data
  def parse(self):
    # load prices
    bs = BeautifulSoup(self.response, "html.parser")

    # search tag
    self.raw = bs.find(class_="uk-table uk-table-striped uk-table-responsive cols-7").find_all(class_="views-field views-field-price-gross")

    #  parsing prices
    self.b_95 = self.raw[1].text.strip().split(": ")[1]
    self.b_100 = self.raw[2].text.strip().split(": ")[1]
    self.d = self.raw[3].text.strip().split(": ")[1]
    self.dp = self.raw[4].text.strip().split(": ")[1]

  # method for get prices
  def get_prices(self):
    try:
      # make request
      self.load()

      # parse
      self.parse()

      # result
      return {"95":self.b_95, "100":self.b_100, "d":self.d, "d+":self.dp}
    
    # catch errors
    except:
      return {"95":"Err", "100":"Err", "d":"Err", "d+":"Err"}

  