from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Ensure the API is alive."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_lint_valid_sql():
    """Test that clean SQL returns success and no violations."""
    payload = {
        "sql": "SELECT * FROM users;",
        "dialect": "postgres"
    }
    response = client.post("/lint", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["violations"]) == 0

def test_lint_and_fix_invalid_sql():
    """Test that messy SQL returns violations and a fixed version."""
    payload = {
        "sql": "select        * from me",
        "dialect": "mysql"
    }
    response = client.post("/lint", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is False
    assert len(data["violations"]) > 0

    assert "SELECT * FROM me \n" in data["fixed_sql"]
    assert "        " not in data["fixed_sql"]

def test_unsupported_dialect():
    """Test that an invalid dialect is handled (SQLFluff usually raises an error)."""
    payload = {
        "sql": "SELECT 1",
        "dialect": "not_a_real_dialect"
    }
    response = client.post("/lint", json=payload)
    assert response.status_code == 500
    assert "SQLFluff Error" in response.json()["detail"]

def test_empty_sql_input():
    """Test Pydantic validation for min_length=1."""
    payload = {
        "sql": "",
        "dialect": "postgres"
    }
    response = client.post("/lint", json=payload)
    assert response.status_code == 422