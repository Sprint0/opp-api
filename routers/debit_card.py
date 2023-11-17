from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

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


def is_valid_debit_card(debit_card_info: DebitCardInfo) -> bool:
    def luhn_checksum(card_number):
        total = 0
        reverse_card_number = card_number[::-1]
        for i, digit in enumerate(reverse_card_number, start=1):
            if i % 2 == 0:
                doubled_digit = int(digit) * 2
                if doubled_digit > 9:
                    doubled_digit -= 9
                total += doubled_digit
            else:
                total += int(digit)
        return total % 10 == 0

    def validate_expiration_date(expiration_date):
        current_date = datetime.utcnow()
        exp_date = datetime.strptime(expiration_date, "%m/%y")
        return exp_date > current_date

    def validate_cvv(cvv):
        return len(cvv) in [3, 4] and cvv.isdigit()

    return (
        luhn_checksum(debit_card_info.card_number)
        and validate_expiration_date(debit_card_info.expiration_date)
        and validate_cvv(debit_card_info.cvv)
    )
