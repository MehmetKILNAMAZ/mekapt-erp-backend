from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, DateTime, func
from ..database import Base

class Personel(Base):
    __tablename__ = "personel"
    id = Column(Integer, primary_key=True, index=True)
    sicil_no = Column(String(20), unique=True)
    ad_soyad = Column(String(100), nullable=False)
    tc_no = Column(String(11))
    gorevi = Column(String(50))
    ise_giris = Column(Date)
    isten_cikis = Column(Date)
    sgk_no = Column(String(20))
    iban = Column(String(34))
    banka = Column(String(50))
    brut_maas = Column(Numeric(10,2))
    net_maas = Column(Numeric(10,2))
    telefon = Column(String(20))
    adres = Column(String(255))
    aktif = Column(Boolean, default=True)
    notlar = Column(String(500))
    created_at = Column(DateTime, default=func.now())
