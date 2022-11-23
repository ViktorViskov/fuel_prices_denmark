from typing import Dict
from json import dumps

from fastapi.responses import *
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.core.schemes import FuelPricesList
from app.core.schemes import Storage
from app.core.page_model import PageModel


def config_routes(server: FastAPI, storage: Storage):
    templates = Jinja2Templates(directory="app/view")

    @server.get("/", response_class=HTMLResponse)
    async def main_page(req: Request):
        return PageModel.main_page(req, storage, templates)

    @server.get("/api", response_class=JSONResponse, response_model=Dict)
    async def api():
        return {"prices": storage.current_prices, "lastUpdateTime": storage.last_update_time}
