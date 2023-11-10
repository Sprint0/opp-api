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
    # 1. Validate the credit card number using the Luhn algorithm
    if not is_luhn_valid(credit_card_info.card_number):
        return False

    # 2. Check if the expiration date is valid (You can add more specific date validation as needed)
    expiration_date = credit_card_info.expiration_date
    if not is_valid_expiration_date(expiration_date):
        return False

    # 3. Validate the CVV code (You can add more CVV validation logic as needed)
    cvv = credit_card_info.cvv
    if not is_valid_cvv(cvv):
        return False

    # All validations passed, the credit card is valid
    return True


def is_luhn_valid(card_number: str):
    """
    Validate the credit card number using the Luhn algorithm.
    """
    card_number = card_number.replace(" ", "")  # Remove spaces
    if not card_number.isdigit():
        return False

    digits = list(map(int, card_number))
    checksum = sum(digits[-2::-2] + [sum(divmod(d * 2, 10)) for d in digits[-1::-2]])
    return checksum % 10 == 0


def is_valid_expiration_date(expiration_date: str):
    """
    Validate the expiration date.
    You can add more specific date validation logic here if needed.
    """
    # Check if the expiration date has the correct format (MM/YY)
    try:
        expiration_date_obj = datetime.strptime(expiration_date, "%m/%y")
    except ValueError:
        return False

    # Check if the expiration date is in the future (you can customize this logic)
    current_date = datetime.now()
    if expiration_date_obj <= current_date:
        return False

    # You can add more date validation logic here as needed.

    return True


def is_valid_cvv(cvv: str):
    """
    Validate the CVV code.
    You can add more CVV validation logic here as needed.
    """
    # Check if the CVV consists of only digits and has a valid length (e.g., 3 or 4 digits)
    if not cvv.isdigit():
        return False

    if len(cvv) not in (3, 4):
        return False

    # You can add more CVV validation logic here, such as checking for valid patterns, etc.

    return True
