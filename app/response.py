from pydantic import BaseModel, HttpUrl
from typing import Union, List

class Author(BaseModel):
    name: str = None
    birth_year: int = None
    death_year: int = None

class Link(BaseModel):
    mime_type: str
    url: HttpUrl

class Book(BaseModel):
    gutenberg_id: int
    title: str = None
    author: List[Author] = None
    genre: Union[str, None] = None
    language: str = None
    subjects: List[str]  = None
    bookshelves: List[str]  = None
    links: List[Link] = None

class ResponseModel(BaseModel):
    count: int = 0
    next: str = None
    items: List[Book]
