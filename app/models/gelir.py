from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Gelir(Base):
    __tablename__ = "gelirler"
    id = Column(Integer, primary_key=True, index=True)
    sira_no = Column(Integer, unique=True, nullable=False)
    tarih = Column(Date, nullable=False, index=True)
    daire_no = Column(Integer, ForeignKey("daireler.daire_no"), nullable=False, index=True)
    sakin_adi = Column(String(100), nullable=False)
    gelir_turu = Column(String(60), nullable=False, default="Aidat")
    tutar = Column(Numeric(10,2), nullable=False)
    odeme_sekli = Column(String(40), nullable=False)
    makbuz_no = Column(String(30), unique=True, nullable=False, index=True)
    donem_yil = Column(Integer)
    donem_ay = Column(Integer)
    notlar = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    daire = relationship("Daire", back_populates="gelirler")
    makbuz = relationship("Makbuz", back_populates="gelir", uselist=False)
