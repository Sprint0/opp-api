from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class AccountRequest(BaseModel):
    user_id: str
    account_type: str
    initial_balance: float


class AccountResponse(BaseModel):
    account_id: str


@router.post("/accounts", response_model=AccountResponse, status_code=201)
def create_account(account_data: AccountRequest):
    # Validate user_id and account_type
    if not account_data.user_id or not account_data.account_type:
        raise HTTPException(status_code=400, detail="Invalid user ID or account type")

    # Need id logic here
    account_id = "5678"

    return {"account_id": account_id}
