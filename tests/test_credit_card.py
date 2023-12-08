from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_validate_credit_card():
    response = client.post(
        "/validate-credit-card",
        json={
            "card_number": "4392268888888888",
            "expiration_date": "12/25",
            "cvv": "567",
            "user_id": 3,
        },
    )
    assert response.status_code == 400


def test_read_credit_cards():
    user_id = 1
    response = client.get(f"/credit-cards?user_id={user_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
