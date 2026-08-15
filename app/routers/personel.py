from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime
from ..database import get_db
from ..models.personel import Personel
from ..auth.jwt import require_admin

router = APIRouter(prefix="/personel", tags=["personel"])

class PersonelIn(BaseModel):
    ad_soyad: str; tc_no: str | None = None; gorevi: str | None = None
    ise_giris: date | None = None; iban: str | None = None; banka: str | None = None
    brut_maas: Decimal | None = None; net_maas: Decimal | None = None
    telefon: str | None = None; aktif: bool = True; notlar: str | None = None

class PersonelOut(PersonelIn):
    id: int; sicil_no: str; created_at: datetime
    class Config: from_attributes = True

@router.get("/", response_model=list[PersonelOut])
async def list_personel(db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(Personel).order_by(Personel.ad_soyad)); return result.scalars().all()

@router.post("/", response_model=PersonelOut, status_code=201)
async def create_personel(data: PersonelIn, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    r = await db.execute(select(func.count()).select_from(Personel)); count = r.scalar() or 0
    sicil_no = f"PRS-{count+1:04d}"
    p = Personel(**data.model_dump(), sicil_no=sicil_no); db.add(p); await db.commit(); await db.refresh(p); return p

@router.put("/{pid}", response_model=PersonelOut)
async def update_personel(pid: int, data: PersonelIn, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(Personel).where(Personel.id == pid))
    p = result.scalar_one_or_none()
    if not p: raise HTTPException(404, "Personel bulunamadı")
    for k, v in data.model_dump().items(): setattr(p, k, v)
    await db.commit(); await db.refresh(p); return p
