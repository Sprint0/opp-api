from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class CreditCardInfo(BaseModel):
    card_number: str
    expiration_date: str
    cvv: str


@router.post("/validate-credit-card")
async def validate_credit_card(credit_card_info: CreditCardInfo):
    if is_valid_credit_card(credit_card_info):
        return {"message": "Credit card is valid"}
    else:
        return {"message": "Credit card is invalid"}


def is_valid_credit_card(credit_card_info: CreditCardInfo):
    if not is_luhn_valid(credit_card_info.card_number):
        return False

    expiration_date = credit_card_info.expiration_date
    if not is_valid_expiration_date(expiration_date):
        return False

    cvv = credit_card_info.cvv
    if not is_valid_cvv(cvv):
        return False

    return True


def is_luhn_valid(card_number: str):
    card_number = card_number.replace(" ", "")
    if not card_number.isdigit():
        return False

    digits = list(map(int, card_number))
    checksum = sum(digits[-2::-2] + [sum(divmod(d * 2, 10)) for d in digits[-1::-2]])
    return checksum % 10 == 0


def is_valid_expiration_date(expiration_date: str):
    try:
        expiration_date_obj = datetime.strptime(expiration_date, "%m/%y")
    except ValueError:
        return False

    current_date = datetime.now()
    if expiration_date_obj <= current_date:
        return False

    return True


def is_valid_cvv(cvv: str):
    if not cvv.isdigit():
        return False

    if len(cvv) not in (3, 4):
        return False

    return True
