import httpx
import unicodedata
import re 

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core import GOOGLE_API_KEY
from app.schemas import RecommendationResponse, PlaceRecommendation
from app.database.models import SearchHistory

def normalize_query(text: str) -> str:
    """Transforma a frase numa chave única e normalizada para a cache."""
    text = text.lower().strip()
    
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    
    text = re.sub(r'[^\w\s]', '', text)
    
    words = text.split()
    stopwords = {"em", "de", "do", "da", "no", "na", "para", "com"}
    meaningful_words = [w for w in words if w not in stopwords]
    
    meaningful_words.sort()
    
    return "_".join(meaningful_words)

async def get_places_from_google(query_utilizador: str, db: AsyncSession) -> RecommendationResponse:
    """
    Procura lugares com lógica de cache baseada em chaves normalizadas.
    """

    check_query = query_utilizador.lower()
    
    palavras_intencao = {
        "restaurante", "hotel", "museu", "parque", "cafe", "bar", 
        "comer", "visitar", "onde", "turismo", "ponto", "atração"
    }
    
    if not any(p in check_query for p in palavras_intencao):
        query_final_google = f"Pontos turísticos em {query_utilizador}"
    else:
        query_final_google = query_utilizador

    search_key = normalize_query(query_final_google)

    query = select(SearchHistory).where(SearchHistory.search_query == search_key)
    result = await db.execute(query)
    cached_search = result.scalars().first()

    if cached_search:
        return RecommendationResponse(**cached_search.response_data)
    
    coords = await get_coordinates(query_utilizador)

    url = "https://places.googleapis.com/v1/places:searchText"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.types"
    }
    
    payload = {
        "textQuery": query_final_google,
        "maxResultCount": 10
    }

    if coords:
        payload["locationBias"] = {
            "circle": {
                "center": {"latitude": coords["lat"], "longitude": coords["lng"]},
                "radius": 5000.0
            }
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

    processed_places.sort(key=lambda x: x.rating, reverse=True)

    final_response = RecommendationResponse(
        count=len(processed_places),
        results=processed_places
    )

    new_cache_entry = SearchHistory(
        search_query=search_key,
        response_data=final_response.model_dump()
    )
    
    db.add(new_cache_entry)
    await db.commit()

    return final_response

async def get_coordinates(address: str) -> dict:
    """Transforma endereço em latitude/longitude usando Google Geocoding API."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                location = data["results"][0]["geometry"]["location"]
                return location 
    return None