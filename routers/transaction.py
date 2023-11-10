from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

router = FastAPI()


class TransactionRequest(BaseModel):
    from_account_id: str
    to_account_id: str
    amount: float


class TransactionResponse(BaseModel):
    transaction_id: str


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
def initiate_transaction(transaction_data: TransactionRequest):
    # Validate from_account_id, to_account_id, and amount
    if not transaction_data.from_account_id or not transaction_data.to_account_id or transaction_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid account IDs or amount")

    # Id logic
    transaction_id = "123456"

    return {"transaction_id": transaction_id}