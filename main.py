from fastapi import FastAPI
from models import models
from db.database import engine
from routers import user
from routers import debit_card, credit_card
from routers import account, transaction

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(debit_card.router)
app.include_router(credit_card.router)
app.include_router(account.router)
app.include_router(transaction.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
