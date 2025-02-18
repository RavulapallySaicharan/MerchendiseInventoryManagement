import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db

# Create a new database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

# Use the test database
app.dependency_overrides[get_db] = test_db

# Test login functionality

def test_login_success(test_db):
    # First, register a user
    response = client.post(
        "/register",
        json={"email": "testuser@example.com", "username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200

    # Then, login with the registered user
    response = client.post(
        "/token",
        data={"username": "testuser@example.com", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure(test_db):
    # Attempt to login with incorrect credentials
    response = client.post(
        "/token",
        data={"username": "wronguser@example.com", "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

# Test register functionality

def test_register_success(test_db):
    response = client.post(
        "/register",
        json={"email": "newuser@example.com", "username": "newuser", "password": "newpassword"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@example.com"


def test_register_failure_existing_email(test_db):
    # Attempt to register with an existing email
    response = client.post(
        "/register",
        json={"email": "testuser@example.com", "username": "anotheruser", "password": "anotherpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

# Test change password functionality

def test_change_password_success(test_db):
    # First, request a password reset
    response = client.post(
        "/reset-password",
        json={"email": "testuser@example.com"}
    )
    assert response.status_code == 200
    reset_token = response.json()["token"]

    # Then, change the password using the reset token
    response = client.post(
        "/change-password",
        json={"token": reset_token, "new_password": "newtestpassword"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password has been successfully changed"


def test_change_password_failure_invalid_token(test_db):
    # Attempt to change password with an invalid token
    response = client.post(
        "/change-password",
        json={"token": "invalidtoken", "new_password": "irrelevant"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired reset token"
