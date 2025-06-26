import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from datetime import datetime, timedelta

# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from db.database import Base, get_db
from models import schemas


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_event(test_db):
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    response = client.post(
        "/events/",
        json={
            "name": "Test Event",
            "location": "Test Location",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_capacity": 2,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Event"
    assert "id" in data


def test_register_attendee(test_db):
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    event_response = client.post(
        "/events/",
        json={
            "name": "Test Event for Registration",
            "location": "Test Location",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_capacity": 2,
        },
    )
    event_id = event_response.json()["id"]

    response = client.post(
        f"/events/{event_id}/register",
        json={"name": "Test User", "email": "test@example.com"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"


def test_register_duplicate_attendee(test_db):
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    event_response = client.post(
        "/events/",
        json={
            "name": "Test Event for Duplicate",
            "location": "Test Location",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_capacity": 2,
        },
    )
    event_id = event_response.json()["id"]
    client.post(
        f"/events/{event_id}/register",
        json={"name": "Test User", "email": "test@example.com"},
    )
    response = client.post(
        f"/events/{event_id}/register",
        json={"name": "Another User", "email": "test@example.com"},
    )
    assert response.status_code == 400, response.text
    assert response.json()["detail"] == "Email already registered for this event"


def test_register_for_full_event(test_db):
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    event_response = client.post(
        "/events/",
        json={
            "name": "Test Event for Capacity",
            "location": "Test Location",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_capacity": 1,
        },
    )
    event_id = event_response.json()["id"]
    client.post(
        f"/events/{event_id}/register",
        json={"name": "Test User 1", "email": "user1@example.com"},
    )
    response = client.post(
        f"/events/{event_id}/register",
        json={"name": "Test User 2", "email": "user2@example.com"},
    )
    assert response.status_code == 400, response.text
    assert response.json()["detail"] == "Event at full capacity"
