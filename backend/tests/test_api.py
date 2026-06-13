from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_resume():
    payload = {
        "resume_text": "Data Science Intern\n- Made dashboard for sales team\n- Used Python to clean data",
        "target_role": "Machine Learning Engineer",
        "location": "Hong Kong",
        "work_type": "Full time",
        "work_mode": "Hybrid",
    }

    response = client.post("/api/v1/analyze", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert len(data["extracted_bullets"]) == 2
    assert len(data["polished_bullets"]) == 2
    assert len(data["job_matches"]) > 0
