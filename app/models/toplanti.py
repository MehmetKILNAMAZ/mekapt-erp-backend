from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, func
from ..database import Base

class Toplanti(Base):
    __tablename__ = "toplanti"
    id = Column(Integer, primary_key=True, index=True)
    toplanti_no = Column(String(20), unique=True)
    toplanti_turu = Column(String(50), default="Olağan")
    tarih = Column(Date, nullable=False)
    saat = Column(Time)
    yer = Column(String(150))
    baskan = Column(String(100))
    katilimcilar = Column(Text)
    gundem = Column(Text)
    kararlar = Column(Text)
    sonraki_toplanti = Column(Date)
    outlook_event_id = Column(String(200))
    durum = Column(String(20), default="Planlandı")
    created_at = Column(DateTime, default=func.now())
