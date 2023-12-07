from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models.models import Account, Transaction

router = APIRouter()


class FundAndFraudCheckRequest(BaseModel):
    transaction_id: int
    account_id: int
    amount: float


class FundAndFraudCheckResponse(BaseModel):
    transaction_id: int
    account_id: int
    amount: float
    status: str


# Fetch database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create database instance
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/check_funds_and_fraud", response_model=FundAndFraudCheckResponse, status_code=201)
def check_funds_and_fraud_endpoint(db: db_dependency, request: FundAndFraudCheckRequest):
    if not request.transaction_id or not request.account_id or request.amount or request.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid Request")

    transaction_id, account_id = request.transaction_id, request.account_id
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id)
    account = db.query(Account).filter(Account.id == account_id)
    amount = transaction.amount
    balance = account.balance
    if check_fraud(amount) is False or check_funds(amount, balance) is False:
        new_status = "Rejected"
        transaction.status = new_status
    db.refresh(transaction)
    return transaction


# Check if the card provided has enough balance
def check_funds(amount, balance):
    if amount > balance:
        return False
    return True


# Check if this transaction may be fraud
def check_fraud(amount):
    if amount >= 10000:
        return False
    return True
