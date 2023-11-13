from fastapi import FastAPI
from models import models
from db.database import engine
from routers import user
from routers import debit_card, credit_card
from routers import account, transaction

app = FastAPI(
    title="Online-payment processing platform ",
    description="This server is aimed to support online payment requests",
    version="1.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(debit_card.router)
app.include_router(credit_card.router)
app.include_router(account.router)
app.include_router(transaction.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
