from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models.models import Transaction, Account
from sqlalchemy import func
from datetime import datetime
from fastapi import Query

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


def parse_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    return None


@router.get("/balance")
def calculate_total_balance(db: db_dependency, user_id: int,
                            start_date: str = Query(None),
                            end_date: str = Query(None)):
    start = parse_date(start_date)
    end = parse_date(end_date)
    account_ids = db.query(Account.id).filter(Account.user_id == user_id).all()
    account_ids = [account_id[0] for account_id in account_ids]
    total_balance = 0
    for account_id in account_ids:
        query_incoming = db.query(func.sum(Transaction.amount)).filter(
            Transaction.to_account_id == account_id,
            Transaction.status == 'Completed'
        )
        query_outgoing = db.query(func.sum(Transaction.amount)).filter(
            Transaction.from_account_id == account_id,
            Transaction.status == 'Completed'
        )

        if start_date:
            query_incoming = query_incoming.filter(Transaction.timestamp >= start)
            query_outgoing = query_outgoing.filter(Transaction.timestamp >= start)
        if end_date:
            query_incoming = query_incoming.filter(Transaction.timestamp <= end)
            query_outgoing = query_outgoing.filter(Transaction.timestamp <= end)

        total_incoming = query_incoming.scalar() or 0
        total_outgoing = query_outgoing.scalar() or 0

        # Add the net balance of this account to the total balance
        total_balance += (total_incoming - total_outgoing)
    round_balance = round(total_balance, 4)
    return {"user_id": user_id, "total_balance": round_balance}


@router.get("/transactions_of_account")
def get_all_transactions(db: db_dependency, account_id: int):
    transactions = db.query(Transaction).filter(Transaction.from_account_id == account_id or
                                                Transaction.to_account_id == account_id).all()
    total_balance = 0
    for transaction in transactions:
        transaction_id = transaction.id
        from_account_id = transaction.from_account_id
        to_account_id = transaction.to_account_id
        amount = transaction.amount
        status = transaction.status
        timestamp = transaction.timestamp
        print(f"Transaction ID: {transaction_id}, Amount: {amount}, status: {status}, \n"
              f"From: {from_account_id}, To: {to_account_id}, Date: {timestamp})")
        if from_account_id == account_id:
            total_balance -= amount
        else:
            total_balance += amount
    print(f"Account Id: {account_id}, Total Balance: {total_balance}")


@router.get("/accounts_receivables")
def get_all_accounts_receivables(db: db_dependency):
    pending_transactions = db.query(Transaction).filter(Transaction.status == "Pending").all()
    for transaction in pending_transactions:
        transaction_id = transaction.id
        amount = transaction.amount
        to_account = transaction.to_account_id
        print(f"Transaction ID: {transaction_id}, Amount: {amount}, Account Receiving: {to_account})")
