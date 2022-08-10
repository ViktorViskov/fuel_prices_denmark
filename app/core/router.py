# libs
from fastapi.responses import *
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

# method for define different routes in web app
def ROUTER(SERVER: FastAPI):

    # jinja2 templates module
    templates = Jinja2Templates(directory="app/view")

    # main page route
    @SERVER.get("/", response_class=HTMLResponse)
    async def processor( req: Request):     
        # generate list with tags
        to_render = {}

        # creating tags
        for item in SERVER.data:
            to_render[item] = {}

            # check for every item
            for some_item in SERVER.data[item]:
                # define current price
                current_price = SERVER.data[item][some_item].replace(",",".")

                # check for last is exist and define different between prices
                price_diff = round(float(current_price) - float(SERVER.last[item][some_item].replace(",",".")), 2) if SERVER.last else 0

                # create element to show
                if price_diff == 0:
                    to_render[item][some_item] = "<span>%s</span>" % ( current_price, )
                elif price_diff > 0:
                    to_render[item][some_item] = "<span style=color:red>%s (%s)</span>" % (current_price, price_diff)
                else:
                    to_render[item][some_item] = "<span style=color:green>%s (%s)</span>" % (current_price, price_diff)

        return templates.TemplateResponse("main.jinja", {"request": req, "obj": to_render, "last": SERVER.last, "last_update": str(SERVER.last_update).split(".")[0]})