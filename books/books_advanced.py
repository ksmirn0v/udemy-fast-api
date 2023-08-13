from fastapi import FastAPI, Body

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


BOOKS = [
    Book(id=1, title="title 1", author="author 1", description="description 1", rating=5),
    Book(id=2, title="title 2", author="author 2", description="description 2", rating=5),
    Book(id=3, title="title 3", author="author 3", description="description 3", rating=1),
]


@app.get("/books")
def get_book():
    return BOOKS


@app.post("/books/create_book")
def create_book(body=Body()):
    BOOKS.append(body)
