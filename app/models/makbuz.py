from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Makbuz(Base):
    __tablename__ = "makbuzlar"
    id = Column(Integer, primary_key=True, index=True)
    makbuz_no = Column(String(30), unique=True, nullable=False, index=True)
    tarih = Column(Date, nullable=False)
    daire_no = Column(Integer, ForeignKey("daireler.daire_no"), nullable=False)
    sakin_adi = Column(String(100), nullable=False)
    aciklama = Column(Text)
    tutar = Column(Numeric(10,2), nullable=False)
    odeme_sekli = Column(String(40), nullable=False)
    donem = Column(String(30))
    gelir_id = Column(Integer, ForeignKey("gelirler.id"))
    durum = Column(String(20), default="Kesildi")
    pdf_path = Column(String(255))
    whatsapp_gonderildi = Column(Boolean, default=False)
    whatsapp_tarih = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    daire = relationship("Daire", back_populates="makbuzlar")
    gelir = relationship("Gelir", back_populates="makbuz")
