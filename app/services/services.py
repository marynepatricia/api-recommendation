import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core import GOOGLE_API_KEY
from app.schemas import RecommendationResponse, PlaceRecommendation
from app.database.models import SearchHistory

async def get_places_from_google(localizacao: str, db: AsyncSession) -> RecommendationResponse:
    """
    Procura lugares no Google Places API com lógica de cache em PostgreSQL.
    """
    localizacao_norm = localizacao.lower().strip()

    query = select(SearchHistory).where(SearchHistory.location == localizacao_norm)
    result = await db.execute(query)
    cached_search = result.scalars().first()

    if cached_search:
        return RecommendationResponse(**cached_search.response_data)

    url = "https://places.googleapis.com/v1/places:searchText"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.types"
    }
    
    payload = {
        "textQuery": localizacao
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Erro na API externa: {response.status_code}")
            
        data = response.json()

    raw_places = data.get("places", [])
    processed_places = []

    for item in raw_places:
        place = PlaceRecommendation(
            name=item.get("displayName", {}).get("text", "Nome indisponível"),
            address=item.get("formattedAddress", "Endereço não encontrado"),
            rating=item.get("rating", 0.0),
            types=item.get("types", [])
        )
        processed_places.append(place)

    final_response = RecommendationResponse(
        count=len(processed_places),
        results=processed_places
    )

    new_cache_entry = SearchHistory(
        location=localizacao_norm,
        response_data=final_response.model_dump()
    )
    
    db.add(new_cache_entry)
    await db.commit()

    return final_response