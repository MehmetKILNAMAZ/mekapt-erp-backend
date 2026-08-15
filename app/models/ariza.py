from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Numeric
from sqlalchemy.sql import func
from ..database import Base

class BakimAriza(Base):
    __tablename__ = "bakim_ariza"
    id = Column(Integer, primary_key=True)
    ariza_no = Column(String(20), unique=True, nullable=False, index=True)
    bildirim_tarihi = Column(Date, nullable=False)
    bildiren = Column(String(100), nullable=False)
    daire_konum = Column(String(80))
    ariza_turu = Column(String(60), nullable=False)
    aciklama = Column(Text)
    oncelik = Column(String(20), default="Orta")
    atanan = Column(String(100))
    durum = Column(String(30), default="Yeni")
    cozum_tarihi = Column(Date)
    maliyet = Column(Numeric(10,2), default=0)
    notlar = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
