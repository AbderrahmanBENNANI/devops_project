import json
from app import create_app

def test_health():
    client = create_app().test_client()
    assert client.get("/health").status_code == 200

def test_cv_pdf():
    client = create_app().test_client()
    payload = {"full_name":"Ada Lovelace","email":"ada@example.com","skills":["Python"]}
    response = client.post("/api/v1/documents/cv/pdf", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"

def test_reject_unknown_fields():
    client = create_app().test_client()
    response = client.post("/api/v1/documents/cv/pdf", json={"full_name":"Ada Lovelace","email":"a@b.com","admin":True})
    assert response.status_code == 400
