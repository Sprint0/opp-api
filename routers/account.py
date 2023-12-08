from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from db.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models.models import Account

router = APIRouter()


class AccountRequest(BaseModel):
    user_id: int


class AccountResp(BaseModel):
    id: int
    user_id: int
    balance: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/accounts",  response_model=AccountResp, status_code=status.HTTP_201_CREATED)
async def create_account(db: db_dependency, account_data: AccountRequest):
    create_account_model = Account(
        user_id=account_data.user_id,
        balance=0,
    )
    db.add(create_account_model)
    db.commit()
    db.refresh(create_account_model)
    return create_account_model


@router.get("/accounts")
def read_accounts(db: db_dependency, user_id: int):
    query = db.query(Account)
    query = query.filter(Account.user_id == user_id)
    accounts = query.all()
    return accounts
