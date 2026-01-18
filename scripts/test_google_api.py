import httpx
from app.config import GOOGLE_API_KEY

def test_google_search():
    # O endereço (URL) da API do Google
    url = "https://places.googleapis.com/v1/places:searchText"
    
    # O que queremos perguntar (neste caso, restaurantes em SP)
    payload = {
        "textQuery": "restaurantes em Recife"
    }
    
    # as "credenciais" e permissões que enviamos no cabeçalho (Header)
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating"
    }

    print("Enviando pedido ao Google...")
    
    # Fazemos a "ligação" (POST)
    response = httpx.post(url, json=payload, headers=headers)
    
    # Mostramos o resultado
    if response.status_code == 200:
        print("Sucesso!")
        print(response.json())
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_google_search()