import pytest
from fastapi.testclient import TestClient
from app.main import app, get_service
from app.schemas import RecommendationResponse

client = TestClient(app)

# Teste simples do Health Check
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# Teste de Recomendações com Injeção de Dependência (Mock)
def test_get_recommendations_mocked():
    # resposta falsa para simular o Google
    mock_response = {
        "count": 1,
        "results": [
            {
                "name": "Lugar de Teste",
                "address": "Rua Fictícia, 123",
                "rating": 5.0,
                "types": ["test"]
            }
        ]
    }
    async def mock_get_places(location: str):
        return mock_response
    
    # Sobrescrita de Dependência: Dizet ao FastAPI para usar o nosso mock
    # em vez de chamar a função real que vai ao Google
    app.dependency_overrides[get_service] = lambda: mock_get_places

    response = client.get("/recommendations?location=Recife")
    
    # Limpamos a sobrescrita após o teste
    app.dependency_overrides = {}

    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["results"][0]["name"] == "Lugar de Teste"