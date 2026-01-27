from sqlalchemy import Column, String, JSON, DateTime, Integer
from datetime import datetime, UTC
from app.database.database import Base

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    search_query = Column(String, unique=True, index=True)
    response_data = Column(JSON)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC).replace(tzinfo=None))
