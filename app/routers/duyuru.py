from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from datetime import date, datetime
from ..database import get_db
from ..models.duyuru import Duyuru
from ..auth.jwt import get_current_user, require_admin

router = APIRouter(prefix="/duyurular", tags=["duyurular"])

class DuyuruIn(BaseModel):
    tarih: date; konu: str; icerik: str; hedef_kitle: str = "Tum Sakinler"
    yayin_sekli: str = "Pano"; gecerlilik_tarihi: date | None = None
    durum: str = "Aktif"; olusturan: str | None = None

class DuyuruOut(DuyuruIn):
    id: int; duyuru_no: str; created_at: datetime
    class Config: from_attributes = True

@router.get("/", response_model=list[DuyuruOut])
async def list_duyurular(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Duyuru).order_by(Duyuru.tarih.desc())); return result.scalars().all()

@router.post("/", response_model=DuyuruOut, status_code=201)
async def create_duyuru(data: DuyuruIn, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(func.count()).select_from(Duyuru)); count = result.scalar() or 0
    dno = f"DUY-{data.tarih.year}-{count+1:04d}"
    d = Duyuru(**data.model_dump(), duyuru_no=dno); db.add(d); await db.commit(); await db.refresh(d); return d

@router.delete("/{duyuru_id}", status_code=204)
async def delete_duyuru(duyuru_id: int, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(Duyuru).where(Duyuru.id == duyuru_id))
    d = result.scalar_one_or_none()
    if not d: raise HTTPException(404, "Duyuru bulunamadı")
    await db.delete(d); await db.commit()
