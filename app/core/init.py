# libs
from datetime import date, datetime
from fastapi import FastAPI
import threading
from threading import Thread
from time import sleep
from pr.app import load_prices

# init function, exec 1 time when server was started
def INIT(SERVER: FastAPI):
  # create variables
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
    SERVER.data = load_prices()

    # time of list update
    SERVER.last_update = datetime.now()

    # pause 30 minuts
    sleep(1800)