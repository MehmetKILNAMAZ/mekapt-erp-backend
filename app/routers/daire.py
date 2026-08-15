from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from decimal import Decimal
from ..database import get_db
from ..models.daire import Daire
from ..auth.jwt import get_current_user, require_admin

router = APIRouter(prefix="/daireler", tags=["daireler"])

class DaireIn(BaseModel):
    daire_no: int
    kat: str
    daire_sahibi: str
    kiraci: str | None = None
    telefon: str | None = None
    eposta: str | None = None
    aylik_aidat: Decimal = Decimal("300.00")
    notlar: str | None = None
    durum: str = "active"

class DaireOut(DaireIn):
    id: int
    class Config: from_attributes = True

@router.get("/", response_model=list[DaireOut])
async def list_daireler(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Daire).order_by(Daire.daire_no))
    return result.scalars().all()

@router.get("/{daire_no}", response_model=DaireOut)
async def get_daire(daire_no: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Daire).where(Daire.daire_no == daire_no))
    d = result.scalar_one_or_none()
    if not d: raise HTTPException(404, "Daire bulunamadı")
    return d

@router.post("/", response_model=DaireOut, status_code=201)
async def create_daire(data: DaireIn, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    daire = Daire(**data.model_dump())
    db.add(daire); await db.commit(); await db.refresh(daire)
    return daire

@router.put("/{daire_no}", response_model=DaireOut)
async def update_daire(daire_no: int, data: DaireIn, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(Daire).where(Daire.daire_no == daire_no))
    d = result.scalar_one_or_none()
    if not d: raise HTTPException(404, "Daire bulunamadı")
    for k, v in data.model_dump().items(): setattr(d, k, v)
    await db.commit(); await db.refresh(d); return d

@router.delete("/{daire_no}", status_code=204)
async def delete_daire(daire_no: int, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(Daire).where(Daire.daire_no == daire_no))
    d = result.scalar_one_or_none()
    if not d: raise HTTPException(404, "Daire bulunamadı")
    await db.delete(d); await db.commit()
