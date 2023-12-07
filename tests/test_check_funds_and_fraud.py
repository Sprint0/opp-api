import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models.models import Base
from routers.check_funds_and_fraud import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db:
            db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# Test cases
def test_check_funds_and_fraud_endpoint():
    # Create a test transaction
    test_transaction = {"transaction_id": 1, "account_id": 1, "amount": -100.0}

    # Test an invalid request (e.g., negative amount)
    response = client.post("/check_funds_and_fraud", json=test_transaction)
    assert response.status_code == 400
    assert "Invalid Request" in response.text


# Run the tests
if __name__ == "__main__":
    # Create tables in the test database
    Base.metadata.create_all(bind=engine)

    # Run the tests
    pytest.main(["-v", __file__])
