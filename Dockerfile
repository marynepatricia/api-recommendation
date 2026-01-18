# 1. Usar uma imagem oficial e leve do Python
FROM python:3.12-slim

# 2. Instalar o 'uv' para gestão de pacotes eficiente
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Definir o diretório de trabalho
WORKDIR /app

# 4. Copiar apenas os ficheiros de dependências primeiro (otimiza a cache)
COPY pyproject.toml ./

# 5. Instalar as dependências no sistema do contentor
RUN uv pip install --system .

# 6. Copiar o código da aplicação
COPY app/ ./app/

# 7. Informar qual porta a aplicação utiliza
EXPOSE 8000

# 8. Comando para iniciar o servidor Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]