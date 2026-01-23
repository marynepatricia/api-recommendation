from sqlalchemy import Column, String, JSON, DateTime, Integer
from datetime import datetime
from app.database.database import Base
from datetime import datetime

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, unique=True, index=True)
    response_data = Column(JSON)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))
