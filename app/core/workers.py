from datetime import date
from datetime import datetime
from threading import Thread
from time import sleep

from fuel_parser.controll import load_prices
from app.core.schemes import Storage


WORKER_UPDATE_SECONDS = 1800


def start_workers(storage: Storage):
    load_thread = Thread(target=_start_price_worker,
                         args=(storage,), daemon=True)
    load_thread.start()


def _start_price_worker(storage: Storage):
    while True:
        new_prices = load_prices()

        # check for new day and if its true, replace 
        if storage.current_day_of_week != date.today().weekday():
            storage.yesterday_prices = storage.current_prices
            storage.current_day_of_week = date.today().weekday()
        
        storage.current_prices = new_prices
        storage.last_update_time = datetime.now()

        sleep(WORKER_UPDATE_SECONDS)
