import pytest
from fastapi.testclient import TestClient
from app.main import app, get_service
from app.schemas.schemas import RecommendationResponse

client = TestClient(app)

# Teste simples do Health Check
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# Teste de Recomendações com Injeção de Dependência (Mock)
def test_get_recommendations_mocked():
    # resposta falsa para simular o Google
    mock_response_unsorted = {
        "count": 2,
        "results": [
            {"name": "Lugar Ruim", "address": "Rua A", "rating": 2.0, "types": ["test"]},
            {"name": "Lugar Ótimo", "address": "Rua B", "rating": 5.0, "types": ["test"]}
        ]
    }

    async def mock_get_places(location: str, db=None):
        results = mock_response_unsorted["results"]
        results.sort(key=lambda x: x["rating"], reverse=True)
        return {"count": 2, "results": results}

    app.dependency_overrides[get_service] = lambda: mock_get_places
    
    response = client.get("/recommendations?location=Porto Alegre")
    app.dependency_overrides = {}

    data = response.json()
    assert data["results"][0]["rating"] == 5.0
    assert data["results"][1]["rating"] == 2.0