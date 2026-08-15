from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from ..database import Base

class Borclu(Base):
    __tablename__ = "borclu"
    id = Column(Integer, primary_key=True, index=True)
    daire_no = Column(Integer, nullable=False, index=True)
    sakin_adi = Column(String(100))
    telefon = Column(String(20))
    donem = Column(String(7))  # "2026/08"
    borc_tutari = Column(Numeric(10,2), default=0)
    devreden_borc = Column(Numeric(10,2), default=0)
    odenen = Column(Numeric(10,2), default=0)
    kalan = Column(Numeric(10,2), default=0)
    vade_tarihi = Column(Date)
    durum = Column(String(20), default="Ödenmedi")
    notlar = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
