from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "metasnap-og-api"

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "docs" in response.json()

def test_generate_og_get_free_tier():
    response = client.get("/api/v1/og/generate?title=Launch+Day+Success&theme=nebula")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.headers["x-metasnap-tier"] == "free"
    assert len(response.content) > 1000  # Valid PNG image bytes

def test_generate_og_post_pro_tier():
    payload = {
        "title": "Scaling Distributed Microservices to 100k QPS",
        "subtitle": "Real-world architectural patterns for high-throughput backends",
        "brand_name": "HighScale Tech",
        "domain": "highscale.dev",
        "author": "Nikhil Jella",
        "handle": "@nikhil_dev",
        "badge": "ARCHITECTURE",
        "theme": "emerald"
    }
    headers = {"X-API-Key": "demo-pro-key-2026"}
    response = client.post("/api/v1/og/generate", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.headers["x-metasnap-tier"] == "pro"
    assert len(response.content) > 1000

def test_invalid_api_key_rejected():
    headers = {"X-API-Key": "invalid-bogus-key"}
    response = client.get("/api/v1/og/generate?title=Test", headers=headers)
    assert response.status_code == 401
    assert "Invalid MetaSnap API Key" in response.json()["detail"]
