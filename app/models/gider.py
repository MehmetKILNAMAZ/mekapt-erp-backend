from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base

class Gider(Base):
    __tablename__ = "giderler"
    id = Column(Integer, primary_key=True, index=True)
    sira_no = Column(Integer, unique=True, nullable=False)
    tarih = Column(Date, nullable=False, index=True)
    gider_turu = Column(String(60), nullable=False)
    kategori = Column(String(40), nullable=False)
    aciklama = Column(Text)
    firma_kisi = Column(String(100))
    tutar = Column(Numeric(10,2), nullable=False)
    odeme_sekli = Column(String(40), nullable=False)
    fatura_makbuz_no = Column(String(50), unique=True, nullable=False)
    donem_yil = Column(Integer)
    donem_ay = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
