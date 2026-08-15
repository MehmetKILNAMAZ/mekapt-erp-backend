from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Daire(Base):
    __tablename__ = "daireler"
    id = Column(Integer, primary_key=True, index=True)
    daire_no = Column(Integer, unique=True, nullable=False, index=True)
    kat = Column(String(50), nullable=False)
    daire_sahibi = Column(String(100), nullable=False)
    kiraci = Column(String(100))
    telefon = Column(String(15))
    eposta = Column(String(100))
    aylik_aidat = Column(Numeric(10,2), nullable=False, default=300)
    notlar = Column(Text)
    durum = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    gelirler = relationship("Gelir", back_populates="daire", lazy="dynamic")
    makbuzlar = relationship("Makbuz", back_populates="daire", lazy="dynamic")
