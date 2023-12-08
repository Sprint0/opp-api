from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_validate_debit_card():
    response = client.post(
        "/validate-debt-card",
        json={
            "card_number": "4063668888888888",
            "expiration_date": "12/25",
            "cvv": "456",
            "user_id": 3,
        },
    )
    assert response.status_code == 400
    # assert (
    #     "Debt card is valid and has been saved to the database"
    #     in response.json().get("message", "")
    # )


def test_read_debit_cards():
    user_id = 1
    response = client.get(f"/debit-cards?user_id={user_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
