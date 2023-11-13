from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from models.models import Base, Users
from routers.user import get_db

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


def test_create_user():
    Base.metadata.create_all(bind=engine)

    user_data = {
        "email": "testuser@example.com",
        "username": "testuser",
        "first_name": "Test",
        "surname": "User",
        "password": "securepassword",
        "phone_number": "1234567890",
        "is_active": True
    }

    response = client.post("/users", json=user_data)
    assert response.status_code == 201

    test_db = next(override_get_db())
    user_in_db = test_db.query(Users).filter(Users.email == user_data["email"]).first()

    assert user_in_db is not None
    assert user_in_db.email == user_data["email"]
    assert user_in_db.username == user_data["username"]
    assert user_in_db.first_name == user_data["first_name"]
    assert user_in_db.surname == user_data["surname"]
    Base.metadata.drop_all(bind=engine)
