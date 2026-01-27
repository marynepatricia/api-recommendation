import pytest
from sqlalchemy.future import select
from app.services import get_places_from_google
from app.database.models import SearchHistory
from app.database import AsyncSessionLocal, engine, Base # Importamos o engine e Base

@pytest.mark.asyncio
async def test_database_recording_flow():
    """
    Testa se o serviço grava corretamente uma nova busca no banco de dados.
    """
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    localizacao = "Porto"
    
    # Criamos uma sessão real com o banco de dados
    async with AsyncSessionLocal() as db:
        # 1. Limpamos qualquer teste anterior para garantir um estado limpo
        from sqlalchemy import delete
        await db.execute(delete(SearchHistory).where(SearchHistory.search_query == localizacao.lower()))
        await db.commit() 

        # 2. Chamamos o serviço (ele vai tentar gravar no DB)
        try:
            await get_places_from_google(localizacao, db) 
        except Exception:
            pass

        # 3. Verificamos se o registro foi criado no banco de dados
        query = select(SearchHistory).where(SearchHistory.search_query == localizacao.lower())
        result = await db.execute(query) 
        record = result.scalars().first() 

        assert record is not None, f"O registro para {localizacao} deveria ter sido gravado na base de dados."
        assert record.search_query == localizacao.lower()