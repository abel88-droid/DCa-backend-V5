# app/models.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Warning(Base):
    __tablename__ = "warnings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    guild_id = Column(String, nullable=False, index=True)
    reason = Column(String, nullable=True)
