# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("biosim_world.html", {"request": request})


# @app.get("/items/{item_id}", response_class=HTMLResponse)
# def read_item(request: Request, item_id: int):
#     return templates.TemplateResponse("item.html", {"request": request, "item_id": item_id})
