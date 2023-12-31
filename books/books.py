from fastapi import FastAPI, Body

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


app = FastAPI()


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def get_books_by_title(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def get_books_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def get_books_by_author_and_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get('author').casefold() == book_author.casefold() and
            book.get('category').casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create_book")
async def create_book(book=Body()):
    BOOKS.append(book)


@app.put("/books/update_book")
async def update_book(book=Body()):
    for idx in range(len(BOOKS)):
        if BOOKS[idx].get('title').casefold() == book.get('title').casefold():
            BOOKS[idx] = book


@app.delete("/books/delete_book/{book_title}")
async def delete_book_by_title(book_title: str):
    for idx in range(len(BOOKS)):
        if BOOKS[idx].get('title').casefold() == book_title.casefold():
            BOOKS.pop(idx)
            break
