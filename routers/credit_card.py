from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import datetime
import requests
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models import CreditCard

router = APIRouter()


class CreditCardInfo(BaseModel):
    card_number: str
    expiration_date: str
    cvv: str
    user_id: int


class CreditCardResp(BaseModel):
    card_number: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/validate-credit-card", status_code=status.HTTP_201_CREATED)
async def validate_credit_card(db: db_dependency, credit_card_info: CreditCardInfo):
    if is_valid_credit_card(credit_card_info):
        credit_card = CreditCard(
            card_number=credit_card_info.card_number,
            expiration_date=credit_card_info.expiration_date,
            cvv=credit_card_info.cvv,
            user_id=credit_card_info.user_id,
        )
        db.add(credit_card)
        db.commit()
        db.refresh(credit_card)
        return {"message": "Credit card is valid and has been saved to the database"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credit card"
        )


@router.get("/credit-cards", response_model=List[CreditCardResp])
def read_credit_cards(db: db_dependency, user_id: int):
    query = db.query(CreditCard)
    query = query.filter(CreditCard.user_id == user_id)
    credit_cards = query.all()
    return credit_cards


def is_valid_credit_card(credit_card_info: CreditCardInfo):
    if not is_luhn_valid(credit_card_info.card_number):
        return False

    expiration_date = credit_card_info.expiration_date
    if not is_valid_expiration_date(expiration_date):
        return False

    cvv = credit_card_info.cvv
    if not is_valid_cvv(cvv):
        return False

    url = "https://c3jkkrjnzlvl5lxof74vldwug40pxsqo.lambda-url.us-west-2.on.aws"
    data = {"card_number": credit_card_info.card_number}
    response = requests.post(url, json=data)
    resp_data = response.json()
    if resp_data["success"] == "true":
        return True
    else:
        print(resp_data["msg"])
        return False


def is_luhn_valid(card_number: str):
    card_number = card_number.replace(" ", "")
    if not card_number.isdigit():
        return False

    digits = list(map(int, card_number))
    checksum = sum(digits[-2::-2] + [sum(divmod(d * 2, 10)) for d in digits[-1::-2]])
    return checksum % 10 == 0


def is_valid_expiration_date(expiration_date: str):
    current_date = datetime.utcnow()
    exp_date = datetime.strptime(expiration_date, "%m/%y")
    return exp_date > current_date


def is_valid_cvv(cvv: str):
    return len(cvv) in [3, 4] and cvv.isdigit()
