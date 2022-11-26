from databases import Database
from fastapi import FastAPI, Request
from typing import List
from fastapi.responses import StreamingResponse
from .queries import *
from .parser import parse_to_json
from .response import ResponseModel
from .logger import get_logger

# get logs in fastapi
# https://fastapi.tiangolo.com/tutorial/request-files/

logger = get_logger(__name__)

app = FastAPI()
database = Database('postgres://book_store_nkrjgr_user:sxjrGPGByXVQIM3wdLLKtuDk0Orfsdg1@dpg-ce12fio2i3mkuce8pm90-a/book_store_nkrjgr')


@app.get("/")
def home():
    return {"Howdy": "World !"}

@app.get("/logs")
async def get_logs():
    def iterfile():  #
        with open('./fastapi.log', mode="rb") as file_like:  #
            yield from file_like
    return StreamingResponse(iterfile())

@app.get("/books/{page}/", response_model=ResponseModel)
async def get_books(
    page: int,
    request: Request
):
    response = ResponseModel(items=[], count=0)
    await database.connect()
    end = 25*page
    start = end-24
    data = await database.fetch_all( get_query(str(start), str(end), dict(request.query_params)))
    response.items = parse_to_json(data)
    response.count = len(data)
    if len(data) == 25:
        response.next = "/books/"+str(page+1)+"/"+str(request.query_params)

    return response
