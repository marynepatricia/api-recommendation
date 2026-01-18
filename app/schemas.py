from pydantic import BaseModel
from typing import List, Optional

# Este modelo representa um único lugar recomendado
class PlaceRecommendation(BaseModel):
    name: str
    address: str
    rating: Optional[float] = 0.0
    types: List[str]

# Este modelo representa a resposta completa da tua API
class RecommendationResponse(BaseModel):
    count: int
    results: List[PlaceRecommendation]