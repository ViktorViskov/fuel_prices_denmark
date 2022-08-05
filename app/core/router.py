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
        return templates.TemplateResponse("main.jinja", {"request": req, "obj": SERVER.data, "last_update": str(SERVER.last_update).split(".")[0]})
    
    # get current prices
    @SERVER.get("/api/current", response_class=JSONResponse)
    async def processor( req: Request):      
        return JSONResponse(SERVER.data)
    
    # get month prices
    @SERVER.get("/api/month", response_class=JSONResponse)
    async def processor( req: Request):      
        return JSONResponse(SERVER.data)

    # get week prices
    @SERVER.get("/api/week", response_class=JSONResponse)
    async def processor( req: Request):      
        return JSONResponse(SERVER.data)
    

