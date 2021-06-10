from fastapi.testclient import TestClient
import main

client = TestClient(main)
def test_main_resource():
    response_auth = client.get("/")
    assert response_auth.status_code == 200