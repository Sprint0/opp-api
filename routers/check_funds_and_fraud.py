from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

router = APIRouter()


class FundAndFraudCheckRequest(BaseModel):
    card_number: str
    amt: float


@router.post("/check_funds_and_fraud")
def check_funds_and_fraud_endpoint(request: FundAndFraudCheckRequest):
    result = check_funds_and_fraud(request.card_number, request.amt)
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=400, detail=result["msg"])


def check_funds_and_fraud(card_number: str, amt: float):
    url = "https://223didiouo3hh4krxhm4n4gv7y0pfzxk.lambda-url.us-west-2.on.aws"
    data = {"card_number": card_number}
    response = requests.post(url, json=data)
    resp_data = response.json()
    if resp_data["success"] == "true":
        return {"success": True, "msg": "Card number has sufficient funds and is not fraudulent"}
    else:
        return {"success": False, "msg": "Fund check or fraud detection failed"}
