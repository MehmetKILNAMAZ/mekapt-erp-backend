from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime
from ..database import get_db
from ..models.ariza import BakimAriza
from ..auth.jwt import get_current_user, require_admin

router = APIRouter(prefix="/arizalar", tags=["arizalar"])

class ArizaIn(BaseModel):
    bildirim_tarihi: date; bildiren: str; daire_konum: str | None = None
    ariza_turu: str; aciklama: str | None = None; oncelik: str = "Orta"
    atanan: str | None = None; durum: str = "Yeni"; cozum_tarihi: date | None = None
    maliyet: Decimal = Decimal("0"); notlar: str | None = None

class ArizaOut(ArizaIn):
    id: int; ariza_no: str; created_at: datetime
    class Config: from_attributes = True

@router.get("/", response_model=list[ArizaOut])
async def list_arizalar(durum: str | None = Query(None), db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    q = select(BakimAriza)
    if durum: q = q.where(BakimAriza.durum == durum)
    result = await db.execute(q.order_by(BakimAriza.bildirim_tarihi.desc())); return result.scalars().all()

@router.post("/", response_model=ArizaOut, status_code=201)
async def create_ariza(data: ArizaIn, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(func.count()).select_from(BakimAriza)); count = result.scalar() or 0
    ariza_no = f"ARZ-{data.bildirim_tarihi.year}-{count+1:04d}"
    a = BakimAriza(**data.model_dump(), ariza_no=ariza_no)
    db.add(a); await db.commit(); await db.refresh(a); return a

@router.put("/{ariza_id}", response_model=ArizaOut)
async def update_ariza(ariza_id: int, data: ArizaIn, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(BakimAriza).where(BakimAriza.id == ariza_id))
    a = result.scalar_one_or_none()
    if not a: raise HTTPException(404, "Arıza bulunamadı")
    for k, v in data.model_dump().items(): setattr(a, k, v)
    await db.commit(); await db.refresh(a); return a

@router.delete("/{ariza_id}", status_code=204)
async def delete_ariza(ariza_id: int, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(BakimAriza).where(BakimAriza.id == ariza_id))
    a = result.scalar_one_or_none()
    if not a: raise HTTPException(404, "Arıza bulunamadı")
    await db.delete(a); await db.commit()
