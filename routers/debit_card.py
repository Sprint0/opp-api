from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class DebitCardInfo(BaseModel):
    card_number: str
    expiration_date: str
    cvv: str


@router.post("/validate-debit-card")
async def validate_debit_card(debit_card_info: DebitCardInfo):
    if is_valid_debit_card(debit_card_info):
        return {"message": "Debit card is valid"}
    else:
        return {"message": "Debit card is invalid"}


def is_valid_debit_card(debit_card_info: DebitCardInfo):
    return True
