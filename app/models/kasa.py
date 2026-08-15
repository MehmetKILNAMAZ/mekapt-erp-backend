from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from ..database import Base

class Kasa(Base):
    __tablename__ = "kasa"
    id = Column(Integer, primary_key=True, index=True)
    tarih = Column(Date, nullable=False)
    belge_no = Column(String(30), unique=True)
    aciklama = Column(String(255), nullable=False)
    kategori = Column(String(50))
    giren = Column(Numeric(10,2), default=0)
    cikan = Column(Numeric(10,2), default=0)
    bakiye = Column(Numeric(10,2), default=0)
    odeme_sekli = Column(String(30), default="Nakit")
    ilgili_belge = Column(String(50))
    olusturan = Column(String(50))
    created_at = Column(DateTime, default=func.now())
