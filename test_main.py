from fastapi.testclient import TestClient
from main import app  # Ensure this is correct and the app is initialized in main.py

client = TestClient(app)

# Test Creating a Program
def test_create_program():
    response = client.post("/programs/", json={"name": "Test Program", "description": "Testing..."})
    # Using status code 201 for creation
    assert response.status_code == 201  # HTTP 201 is more common for successful POST that creates a resource
    assert response.json()["name"] == "Test Program"

# Test client registration
def test_register_client():
    response = client.post("/clients/", json={"name": "John Doe", "email": "john@example.com", "program_id": 1})
    # Ensure status code reflects successful creation
    assert response.status_code == 201  # Typically POST that creates a client returns 201
    assert response.json()["name"] == "John Doe"

# Test Client Enrollment
def test_enroll_client():
    response = client.post("/clients/1/enroll/?program_id=1")
    # Assuming the enrollment process is successful
    assert response.status_code == 200  # This could be 200 or 204 depending on the behavior
    assert response.json() == {"message": "Client John Doe enrolled in Test Program"}
