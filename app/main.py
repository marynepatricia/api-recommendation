from fastapi import FastAPI, Query, HTTPException, Depends
from app.services import get_places_from_google
from app.schemas import RecommendationResponse

app = FastAPI(title="API de Recomendação de Lugares")

def get_service():
    return get_places_from_google

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    location: str = Query(..., description="Localização para busca"),
    service_func = Depends(get_service)
):
    try:
        # chamamos a função que foi injetada
        return await service_func(location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))