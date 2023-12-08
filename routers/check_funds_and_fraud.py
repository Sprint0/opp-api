from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models.models import Account, CreditCard, DebitCard

router = APIRouter()


class FundAndFraudCheckRequest(BaseModel):
    account_id: int
    amount: float
    card_id: int
    card_type: str
    user_id: int


# Fetch database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create database instance
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/check_funds_and_fraud", status_code=201)
def check_funds_and_fraud_endpoint(db: db_dependency, request: FundAndFraudCheckRequest):
    if not request.user_id or not request.card_id or not request.card_type or \
            not request.account_id or not request.amount or request.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid Request, missing request parameters")

    user_id, card_id, account_id, card_type, amount = \
        request.user_id, request.card_id, request.account_id, request.card_type, request.amount
    account_user_id = db.query(Account.user_id).filter(Account.id == account_id).first()[0]

    if account_user_id != user_id:
        raise HTTPException(status_code=400, detail="Account doesn't belong to user")

    if card_type == "Credit":
        card_user = db.query(CreditCard.user_id).filter(CreditCard.id == card_id).first()
        if card_user != user_id:
            raise HTTPException(status_code=400, detail="Card doesn't belong to user")
    else:
        card_user = db.query(DebitCard.user_id).filter(CreditCard.id == card_id).first()
        if card_user != user_id:
            raise HTTPException(status_code=400, detail="Card doesn't belong to user")
        balance = db.query(Account.balance).filter(Account.id == account_id).first()
        if balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient fund")

    if check_fraud(amount) is False:
        raise HTTPException(status_code=400, detail="Amount exceeding limits")
    return {"Check result": "pass"}


# Check if this transaction may be fraud
def check_fraud(amount):
    if amount >= 10000:
        return False
    return True
