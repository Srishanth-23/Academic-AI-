import traceback
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

try:
    response = client.post("/auth/login", json={"email": "student@test.com", "password": "password123"})
    print("STATUS CODE:", response.status_code)
    print("RESPONSE:", response.json())
except Exception as e:
    print("EXCEPTION CAUGHT:")
    traceback.print_exc()
