from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_validate_debit_card_valid():
    valid_debit_card = {
        "card_number": "4147202464191053",
        "expiration_date": "12/25",
        "cvv": "123",
    }

    response = client.post("/debitCard", json=valid_debit_card)

    assert response.status_code == 201

    assert response.json() == {"message": "Debit card is valid"}


def test_validate_debit_card_invalid():
    invalid_debit_card = {
        "card_number": "1234567890123456",
        "expiration_date": "05/22",
        "cvv": "abc",
    }

    response = client.post("/validate-debit-card", json=invalid_debit_card)

    assert response.status_code == 201

    assert response.json() == {"message": "Debit card is invalid"}
