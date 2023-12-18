# backend server
from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = open("index.html").read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/d3_data")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
