from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


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


@app.get("/books", status_code=status.HTTP_200_OK)
async def get_book():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(
        status_code=404,
        detail=f"a book with id={book_id} doesn't exist!"
    )


@app.get("/book/{title}", status_code=status.HTTP_200_OK)
async def get_book_by_title(title: str = Path(min_length=3)):
    for book in BOOKS:
        if book.title == title:
            return book


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    book = Book(**book_request.model_dump())
    create_id(book=book)
    BOOKS.append(book)


@app.put("/books/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest):
    book_changed = False
    for idx in range(len(BOOKS)):
        if BOOKS[idx].id == book_request.id:
            BOOKS[idx] = Book(**book_request.model_dump())
            book_changed = not book_changed
    if not book_changed:
        raise HTTPException(
            status_code=404,
            detail=f"a book with id={book_request.id} was not found!"
        )


@app.delete("/books/delete-book/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Query(gt=0)):
    book_deleted = False
    for idx in range(len(BOOKS)):
        if BOOKS[idx].id == book_id:
            BOOKS.pop(idx)
            book_deleted = not book_deleted
            break
    if not book_deleted:
        raise HTTPException(
            status_code=404,
            detail=f"a book with id={book_id} was not found!"
        )


def create_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
