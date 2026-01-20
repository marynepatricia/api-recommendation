from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from app.database.database import engine, Base, get_db
from app.services import get_places_from_google
from app.schemas import RecommendationResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="API de Recomendação de Lugares", lifespan=lifespan)

def get_service():
    return get_places_from_google

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    location: str = Query(..., description="Localização para busca"),
    service_func = Depends(get_service),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await service_func(location, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))