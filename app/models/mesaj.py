from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base

class Mesaj(Base):
    __tablename__ = "mesajlar"
    id = Column(Integer, primary_key=True)
    daire_no = Column(Integer, nullable=False, index=True)
    gonderen = Column(String(20), nullable=False)
    icerik = Column(Text, nullable=False)
    okundu = Column(Boolean, default=False)
    olusturulma = Column(DateTime(timezone=True), server_default=func.now())
