from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models.models import Transaction, Account
from sqlalchemy import func

router = APIRouter()


class TransactionRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float
    status: str


class TransactionResponse(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    amount: float
    status: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
def initiate_transaction(db: db_dependency, transaction_data: TransactionRequest):
    # Validate from_account_id, to_account_id, and amount
    if not transaction_data.from_account_id or not transaction_data.to_account_id or transaction_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid account IDs or amount")

    create_transaction_model = Transaction(
        from_account_id=transaction_data.from_account_id,
        to_account_id=transaction_data.to_account_id,
        amount=transaction_data.amount,
        status=transaction_data.status,
    )
    db.add(create_transaction_model)
    db.commit()
    db.refresh(create_transaction_model)
    return create_transaction_model


@router.get("/balance")
def calculate_total_balance(db: db_dependency, user_id: int):
    account_ids = db.query(Account.id).filter(Account.user_id == user_id).all()
    account_ids = [account_id[0] for account_id in account_ids]
    total_balance = 0
    for account_id in account_ids:
        # Calculate total incoming funds for each account
        total_incoming = db.query(func.sum(Transaction.amount)).filter(Transaction.to_account_id == account_id,
                                                                       Transaction.status == 'Completed').scalar() or 0

        # Calculate total outgoing funds for each account
        total_outgoing = db.query(func.sum(Transaction.amount)).filter(Transaction.from_account_id == account_id,
                                                                       Transaction.status == 'Completed').scalar() or 0

        # Add the net balance of this account to the total balance
        total_balance += (total_incoming - total_outgoing)
    round_balance = round(total_balance, 4)
    return {"user_id": user_id, "total_balance": round_balance}
