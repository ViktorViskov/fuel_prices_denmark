from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

def mount_static_files(SERVER: FastAPI):
    # mount all files in "/app/static directory" like static files
    SERVER.mount("/", StaticFiles(directory="app/static"), name="html_js_css")