from fastapi import FastAPI
from models import models
from db.database import engine
from routers import user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
