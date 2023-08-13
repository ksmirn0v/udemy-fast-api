from fastapi import FastAPI

import models
from database import engine


app = FastAPI()


models.base.metadata.create_all(bind=engine)
