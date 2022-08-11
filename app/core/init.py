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
  SERVER.last = {}
  SERVER.new = {}
  SERVER.data = {}
  SERVER.last_update = ""
  SERVER.dump_day = date.today().weekday() # default variable for today

  # crete thread
  SERVER.a = True
  load_thread = Thread(target=load, args=(SERVER,), daemon=True)
  load_thread.start()

# method for load data
def load(SERVER: FastAPI):
  while True:
    # load and attemp data
    SERVER.new = load_prices()

    # chech when was last update and if its new day replace last data
    if SERVER.dump_day != date.today().weekday() and SERVER.data:
      
      # replace data
      SERVER.last = SERVER.data

      # replace day
      SERVER.dump_day = date.today().weekday()

    # update data
    SERVER.data = SERVER.new

    # time of list update
    SERVER.last_update = datetime.now()

    # pause 30 minuts
    sleep(1800)
