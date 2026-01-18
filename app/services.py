import httpx
from app.config import GOOGLE_API_KEY
from app.schemas import RecommendationResponse, PlaceRecommendation

async def get_places_from_google(localizacao: str) -> RecommendationResponse:
    # Configurações da API do Google
    url = "https://places.googleapis.com/v1/places:searchText"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.types"
    }
    
    # O corpo do pedido com a localização fornecida pelo utilizador
    payload = {
        "textQuery": localizacao
    }

    # Fazemos a chamada assíncrona usando httpx
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        
        # Se algo correr mal na Google, lançamos uma exceção
        if response.status_code != 200:
            raise Exception(f"Erro na API externa: {response.status_code}")
            
        data = response.json()

    # Transformamos o JSON "sujo" do Google no nosso Schema limpo
    raw_places = data.get("places", [])
    processed_places = []

    for item in raw_places:
        # Mapeamos os campos do Google para os nossos campos do PlaceRecommendation
        place = PlaceRecommendation(
            name=item.get("displayName", {}).get("text", "Nome indisponível"),
            address=item.get("formattedAddress", "Endereço não encontrado"),
            rating=item.get("rating", 0.0),
            types=item.get("types", [])
        )
        processed_places.append(place)

    # Retornamos o objeto final formatado
    return RecommendationResponse(
        count=len(processed_places),
        results=processed_places
    )