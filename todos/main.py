from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from database import engine, session


app = FastAPI()


models.base.metadata.create_all(bind=engine)


def get_db():

    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def get_all_records(db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Todos).all()
