# libs
from datetime import date, datetime
import json
from fastapi import FastAPI
from os.path import exists
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
  SERVER.dump_day = date.today().weekday() # default variable for today

  # read dump
  if exists("dump.json"):
    SERVER.last = json.loads(open("dump.json").read())

  # crete thread
  SERVER.a = True
  load_thread = Thread(target=load, args=(SERVER,), daemon=True)
  load_thread.start()

# method for load data
def load(SERVER: FastAPI):
  while True:
    # load and attemp data
    SERVER.new = load_prices()

    # variable for check error in new data
    is_error = False

    # check for all data is exist
    for station in SERVER.new:
      for fuel_type in SERVER.new[station]:
        if SERVER.new[station][fuel_type] == "Err":
          is_error = True
          break

    if is_error:
      SERVER.last_update = "ERROR. Last update was %s" % datetime.now()
      sleep(900)
      continue



    # chech when was last update and if its new day replace last data
    if SERVER.dump_day != date.today().weekday() and SERVER.data:
      SERVER.last = SERVER.data
      open("dump.json", "w").write(json.dumps(SERVER.data))

    # update data
    SERVER.data = SERVER.new

    # time of list update
    SERVER.last_update = datetime.now()

    # pause 30 minuts
    sleep(1800)