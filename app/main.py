from fastapi import FastAPI, Query, HTTPException
from app.services import get_places_from_google
from app.schemas import RecommendationResponse

app = FastAPI(title="API de Recomendação de Lugares")

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    location: str = Query(..., description="Localização para busca de lugares")
):
    """
    Recebe uma localização e devolve uma lista de lugares recomendados.
    """
    try:
        return await get_places_from_google(location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))