from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_check_funds_and_fraud_endpoint():
    # Test case for successful fund check and fraud detection
    response = client.post("/check_funds_and_fraud", json={"card_number": "4147202464191053", "amt": 100.00})
    assert response.status_code == 200
    assert response.json() == {"success": True, "msg": "Card number has sufficient funds and is not fraudulent"}

    # Test case for unsuccessful fund check or fraud detection
    response = client.post("/check_funds_and_fraud", json={"card_number": "4147202464191054", "amt": 100000.00})
    assert response.status_code == 400
    assert response.json() == {"detail": "Fund check or fraud detection failed"}
