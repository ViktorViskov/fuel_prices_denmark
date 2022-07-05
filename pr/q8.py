# libs
from requests import request

# class to parse data from Q8 station
class Q8_STATION:
  # variables
  link = "https://www.q8.dk/-/api/PriceViewProduct/GetPriceViewProducts"
  header = {"Content-Type": "text/html"}
  form = """{"FuelsIdList": [
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

  # method for load data
  def load(self):
    self.response = request("POST", self.link, headers=self.header, data=self.form).json()

  # method for parsing data
  def parse(self):
    self.q8_raw = list(map(lambda data: data["PriceInclVATInclTax"], self.response["Products"] ))

  # method for get prices
  def get_prices(self):
    try:
      # make request
      self.load()

      # parse
      self.parse()

      # result
      return {"95":self.q8_raw[0], "100":self.q8_raw[1], "d":self.q8_raw[2], "d+":self.q8_raw[3]}
    
    # catch errors
    except:
      return {"95":"Err","100":"Err", "d":"Err", "d+":"Err"}
  