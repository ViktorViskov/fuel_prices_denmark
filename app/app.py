# libs
from time import sleep
from fastapi import FastAPI
from app.core.router import ROUTER
from app.core.middleware import MIDDLEWARE
from app.core.cors import CORS
from app.core.static import STATIC
from app.core.init import INIT
from pr.app import load_prices
from threading import Thread

# 
# configs
# 

# class for present this web server
class WEB_SERVER(FastAPI):

    # constructor
    def __init__(self):

        # use super constuctor
        super().__init__(docs_url=None, redoc_url=None)

        # enable CORS
        # CORS(self)

        # enable middleware
        # MIDDLEWARE(self)

        # enable routing
        ROUTER(self)

        # enable static files
        STATIC(self)

        # init function 
        INIT(self)