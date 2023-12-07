from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models import DebitCard

router = APIRouter()


class DebitCardInfo(BaseModel):
    card_number: str
    expiration_date: str
    cvv: str
    user_id: int


class DebitCardResp(BaseModel):
    card_number: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/validate-debt-card", status_code=status.HTTP_201_CREATED)
async def validate_debt_card(db: db_dependency, debt_card_info: DebitCardInfo):
    if is_valid_debit_card(debt_card_info):
        debit_card = DebitCard(
            card_number=debt_card_info.card_number,
            expiration_date=debt_card_info.expiration_date,
            cvv=debt_card_info.cvv,
            user_id=debt_card_info.user_id,
        )
        db.add(debit_card)
        db.commit()
        db.refresh(debit_card)
        return {"message": "Debt card is valid and has been saved to the database"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid debt card"
        )


@router.get("/debit-cards", response_model=List[DebitCardResp])
def read_debit_cards(db: db_dependency, user_id: int):
    query = db.query(DebitCard)
    query = query.filter(DebitCard.user_id == user_id)
    debit_cards = query.all()
    return debit_cards


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
