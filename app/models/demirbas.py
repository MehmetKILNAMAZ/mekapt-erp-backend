from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from ..database import Base

class Demirbas(Base):
    __tablename__ = "demirbas"
    id = Column(Integer, primary_key=True, index=True)
    demirbas_no = Column(String(20), unique=True)
    tanim = Column(String(150), nullable=False)
    marka = Column(String(50))
    model = Column(String(50))
    seri_no = Column(String(50))
    kategori = Column(String(50))
    konum = Column(String(100))
    alis_tarihi = Column(Date)
    alis_fiyati = Column(Numeric(10,2))
    garanti_bitis = Column(Date)
    durum = Column(String(30), default="Aktif")
    son_bakim = Column(Date)
    sonraki_bakim = Column(Date)
    notlar = Column(String(500))
    created_at = Column(DateTime, default=func.now())
