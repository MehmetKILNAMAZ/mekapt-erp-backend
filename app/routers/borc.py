from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime
from ..database import get_db
from ..models.borclu import Borclu
from ..auth.jwt import get_current_user, require_admin

router = APIRouter(prefix="/borclar", tags=["borclar"])

class BorcIn(BaseModel):
    daire_no: int; sakin_adi: str | None = None; telefon: str | None = None
    donem: str; borc_tutari: Decimal = Decimal("0"); devreden_borc: Decimal = Decimal("0")
    odenen: Decimal = Decimal("0"); kalan: Decimal = Decimal("0")
    vade_tarihi: date | None = None; durum: str = "Ödenmedi"; notlar: str | None = None

class BorcOut(BorcIn):
    id: int; created_at: datetime
    class Config: from_attributes = True

@router.get("/", response_model=list[BorcOut])
async def list_borclar(sadece_odenmemis: bool = Query(False), db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    q = select(Borclu)
    if sadece_odenmemis: q = q.where(Borclu.durum != "Ödendi")
    result = await db.execute(q.order_by(Borclu.daire_no)); return result.scalars().all()

@router.get("/ozet")
async def borc_ozet(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(func.sum(Borclu.kalan), func.count()).select_from(Borclu).where(Borclu.durum != "Ödendi"))
    row = result.one()
    return {"toplam_borc": float(row[0] or 0), "borclu_daire_sayisi": row[1]}

@router.post("/", response_model=BorcOut, status_code=201)
async def create_borc(data: BorcIn, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    b = Borclu(**data.model_dump()); db.add(b); await db.commit(); await db.refresh(b); return b

@router.put("/{borc_id}", response_model=BorcOut)
async def update_borc(borc_id: int, data: BorcIn, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(Borclu).where(Borclu.id == borc_id))
    b = result.scalar_one_or_none()
    if not b: raise HTTPException(404, "Borç kaydı bulunamadı")
    for k, v in data.model_dump().items(): setattr(b, k, v)
    await db.commit(); await db.refresh(b); return b
