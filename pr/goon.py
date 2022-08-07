# libs
from requests import request
from PIL import Image, ImageOps
from os import popen
from bs4 import BeautifulSoup


# class to parse data from OK station
class GOON_STATION:
  # variables
  link = "https://goon.nu/priser/#Aktuellepumpepriser"
  file_name = "prices.png"
  tmp_folder = "/tmp"

  # function for get link
  def get_link(self):
    # load page
    self.response = request("GET", self.link).text

    # load prices
    bs = BeautifulSoup(self.response, "html.parser")

    # search image tag
    self.raw = bs.find(name="img", alt="priser")

    # parse image link
    self.image_link = self.raw['data-src']

  # method for load data
  def load(self):
    self.response = request("GET", self.image_link, stream=True)

  # method for preprocessing image
  def preprocess_images(self):
    # read image
    img = Image.open(self.response.raw)

    # cutting (l,t,r,b) and preprocessing
    ImageOps.invert(img.crop((60, 176, 190, 224)).convert('L').point(lambda x : 255 if x > 0 else 0, '1')).save("%s/b92.jpg" % (self.tmp_folder))
    ImageOps.invert(img.crop((60, 232, 190, 280)).convert('L').point(lambda x : 255 if x > 0 else 0, '1')).save("%s/b95.jpg" % (self.tmp_folder))
    ImageOps.invert(img.crop((60, 289, 190, 337)).convert('L').point(lambda x : 255 if x > 0 else 0, '1')).save("%s/d.jpg" % (self.tmp_folder))

  # method for parsing data
  def parse(self):

    # parsing data from image 
    self.b_92 = popen("ssocr -d 5 -T %s/b92.jpg" % (self.tmp_folder)).read().strip()
    self.b_95 = popen("ssocr -d 5 -T %s/b95.jpg" % (self.tmp_folder)).read().strip()
    self.d = popen("ssocr -d 5 -T %s/d.jpg" % (self.tmp_folder)).read().strip()

    # check for empty and replace with err
    self.b_92 = "Err" if self.b_92 == "" else self.b_92
    self.b_95 = "Err" if self.b_95 == "" else self.b_95
    self.d = "Err" if self.d == "" else self.d


  # method for get prices
  def get_prices(self):
#    try:
      # make request
      self.get_link()

      # load image and process
      self.load()
      self.preprocess_images()

      # parse
      self.parse()

      # result
      return {"92":self.b_92, "95":self.b_95, "d":self.d}
    
    # catch errors
#    except:
#      return {"92":"Err", "95":"Err", "d":"Err"}
