from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


class Book:

    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):

    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'example title',
                'author': 'example author',
                'description': 'example description',
                'rating': 5,
            }
        }


BOOKS = [
    Book(id=1, title="title 1", author="author 1", description="description 1", rating=5),
    Book(id=2, title="title 2", author="author 2", description="description 2", rating=5),
    Book(id=3, title="title 3", author="author 3", description="description 3", rating=1),
]


@app.get("/books")
def get_book():
    return BOOKS


@app.post("/books/create_book")
def create_book(book_request: BookRequest):
    book = Book(**book_request.model_dump())
    create_id(book=book)
    BOOKS.append(book)


def create_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
