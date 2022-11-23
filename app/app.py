from fastapi import FastAPI

from app.core.routes import config_routes
from app.core.static import mount_static_files
from app.core.workers import start_workers
from app.core.schemes import Storage

web_server = FastAPI(docs_url=None, redoc_url=None)
storage = Storage()

config_routes(web_server, storage)
mount_static_files(web_server)

# start thread for load price from different sellers
start_workers(storage)
