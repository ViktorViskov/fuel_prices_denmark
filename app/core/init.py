# libs
from datetime import date, datetime
import json
from fastapi import FastAPI
import threading
from threading import Thread
from time import sleep
from pr.app import load_prices

# init function, exec 1 time when server was started
def INIT(SERVER: FastAPI):
  # create variables
  SERVER.last = {} # need dump and read from file
  SERVER.new = {}
  SERVER.data = {}
  SERVER.last_update = ""

  # crete thread
  SERVER.a = True
  load_thread = Thread(target=load, args=(SERVER,), daemon=True)
  load_thread.start()

# method for load data
def load(SERVER: FastAPI):
  while True:
    # load and attemp data
    # SERVER.new = load_prices()
    SERVER.new = json.loads(open("test.json").read())

    # variable for check error in new data
    is_error = False

    # check for all data is exist
    for station in SERVER.new:
      for fuel_type in SERVER.new[station]:
        if SERVER.new[station][fuel_type] == "Err":
          is_error = True
          break

    if is_error:
      SERVER.last_update = "ERROR %s ERROR" % datetime.now()
      sleep(900)
      continue



    # check and update current prices
    if SERVER.new != SERVER.data:
      SERVER.last = SERVER.data
      SERVER.data = SERVER.new
      open("dump.json", "w").write(json.dumps(SERVER.last))


    # time of list update
    SERVER.last_update = datetime.now()

    # pause 30 minuts
    sleep(1800)