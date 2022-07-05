# libs
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Function for define middleware logick
def MIDDLEWARE(SERVER: FastAPI):
    @SERVER.middleware("http")
    async def middleware(req: Request, call_back):
        # controll for localhost
        if "127.0.0.1" in req.client:
            response = await call_back(req)
        else:
            response = JSONResponse({"message": "Allowed only localhost"})

        # return response for client
        return response