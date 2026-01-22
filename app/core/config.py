import os
from dotenv import load_dotenv

# carrega as variáveis do .env para o sistema
load_dotenv()

# captura a chave específica e guarda numa variável
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# uma pequena verificação de segurança
if not GOOGLE_API_KEY:
    raise ValueError("ERRO: A variável GOOGLE_API_KEY não foi encontrada no ficheiro .env")