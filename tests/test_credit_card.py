from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_validate_credit_card_valid():
    valid_credit_card = {
        "card_number": "4111111111111111",
        "expiration_date": "12/25",
        "cvv": "123",
    }

    response = client.post("/validate-credit-card", json=valid_credit_card)

    assert response.status_code == 201

    assert response.json() == {"message": "Credit card is valid"}


def test_validate_credit_card_invalid():
    invalid_credit_card = {
        "card_number": "1234567890123456",
        "expiration_date": "05/22",
        "cvv": "abc",
    }

    response = client.post("/validate-credit-card", json=invalid_credit_card)

    assert response.status_code == 201

    assert response.json() == {"message": "Credit card is invalid"}
