from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base

class Duyuru(Base):
    __tablename__ = "duyurular"
    id = Column(Integer, primary_key=True)
    duyuru_no = Column(String(20), unique=True, nullable=False, index=True)
    tarih = Column(Date, nullable=False)
    konu = Column(String(200), nullable=False)
    icerik = Column(Text, nullable=False)
    hedef_kitle = Column(String(50), default="Tum Sakinler")
    yayin_sekli = Column(String(50), default="Pano")
    gecerlilik_tarihi = Column(Date)
    durum = Column(String(20), default="Aktif")
    olusturan = Column(String(80))
    whatsapp_gonderildi = Column(String(5), default="hayir")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
