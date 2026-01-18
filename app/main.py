from fastapi import FastAPI

app = FastAPI(title="API de Recomendação de Lugares")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

