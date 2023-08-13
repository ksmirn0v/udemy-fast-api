from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

import models
from database import engine, session


app = FastAPI()


models.base.metadata.create_all(bind=engine)


class TodosRequest(BaseModel):

    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


def get_db():

    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get('/todos', status_code=status.HTTP_200_OK)
async def get_all_records(db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Todos).all()


@app.get('/todos/{record_id}', status_code=status.HTTP_200_OK)
async def get_records_by_id(db: Annotated[Session, Depends(get_db)], record_id: int = Path(gt=0)):
    output = db.query(models.Todos).filter(models.Todos.id == record_id).first()
    if output is not None:
        return output
    raise HTTPException(
        status_code=404,
        detail=f"The record with id={record_id} was not found in the database!"
    )


@app.post('/todos/create-todo', status_code=status.HTTP_201_CREATED)
async def add_record(db: Annotated[Session, Depends(get_db)], todos_request: TodosRequest):
    todos_model = models.Todos(**todos_request.model_dump())
    db.add(todos_model)
    db.commit()
