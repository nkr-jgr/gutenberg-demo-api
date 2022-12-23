from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from functools import lru_cache
from databases import Database
from typing import List

from .queries import *
from .parser import parse_to_json
from .response import ResponseModel
from .logger import get_logger
from .config import Settings

# get logs in fastapi
# https://fastapi.tiangolo.com/tutorial/request-files/

app = FastAPI()

settings = Settings()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = Database(settings.DATABASE_URL)

@lru_cache()
def get_settings():
    return Settings()

logger = get_logger(__name__, get_settings())

@app.get("/")
def home():
    logger.error("HEY")
    return {"Howdy": "World !"}

@app.get("/logs")
async def get_logs():
    def iterfile():  #
        with open(settings.LOG_FILENAME, mode="rb") as file_like:  #
            yield from file_like
    return StreamingResponse(iterfile())

@app.get("/books/{page}/", response_model=ResponseModel)
async def get_books(
    page: int,
    request: Request
):
    logger.info("Request for get_books with parameters ")
    response = ResponseModel(items=[], count=0)
    await database.connect()
    end = settings.PAGINATION_ITEMS*page
    start = end-settings.PAGINATION_ITEMS+1
    logger.info("Fetching query results ")
    data = await database.fetch_all( get_query(str(start), str(end), dict(request.query_params)))
    response.items = parse_to_json(data)
    response.count = len(data)
    if len(data) == settings.PAGINATION_ITEMS:
        response.next = "/books/"+str(page+1)+"/"+str(request.query_params)

    return response
