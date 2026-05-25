from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add():
    response = client.get("/add?a=10&b=5")
    assert response.status_code == 200
    assert response.json() == {"operation": "add", "result": 15.0}

def test_subtract():
    response = client.get("/subtract?a=10&b=5")
    assert response.status_code == 200
    assert response.json() == {"operation": "subtract", "result": 5.0}

def test_multiply():
    response = client.get("/multiply?a=10&b=5")
    assert response.status_code == 200
    assert response.json() == {"operation": "multiply", "result": 50.0}

def test_divide():
    response = client.get("/divide?a=10&b=5")
    assert response.status_code == 200
    assert response.json() == {"operation": "divide", "result": 2.0}

def test_divide_by_zero():
    response = client.get("/divide?a=10&b=0")
    assert response.status_code == 400
    assert response.json() == {"detail": "Division by zero is not allowed"}