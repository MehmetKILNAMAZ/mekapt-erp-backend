from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime
from ..database import get_db
from ..models.gider import Gider
from ..auth.jwt import get_current_user, require_admin

router = APIRouter(prefix="/giderler", tags=["giderler"])

class GiderIn(BaseModel):
    tarih: date; gider_turu: str; kategori: str; aciklama: str | None = None
    firma_kisi: str | None = None; tutar: Decimal; odeme_sekli: str = "Nakit"
    donem_yil: int | None = None; donem_ay: int | None = None

class GiderOut(GiderIn):
    id: int; sira_no: int; fatura_makbuz_no: str; created_at: datetime
    class Config: from_attributes = True

@router.get("/", response_model=list[GiderOut])
async def list_giderler(yil: int | None = Query(None), ay: int | None = Query(None),
                        kategori: str | None = Query(None), db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    q = select(Gider)
    if yil: q = q.where(extract("year", Gider.tarih) == yil)
    if ay: q = q.where(extract("month", Gider.tarih) == ay)
    if kategori: q = q.where(Gider.kategori == kategori)
    result = await db.execute(q.order_by(Gider.tarih.desc())); return result.scalars().all()

@router.post("/", response_model=GiderOut, status_code=201)
async def create_gider(data: GiderIn, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(func.max(Gider.sira_no))); sira = (result.scalar() or 0) + 1
    result2 = await db.execute(select(func.count()).select_from(Gider).where(extract("year", Gider.tarih)==data.tarih.year))
    count = result2.scalar() or 0; mkno = f"GDR-{data.tarih.year}-{count+1:04d}"
    g = Gider(**data.model_dump(), sira_no=sira, fatura_makbuz_no=mkno)
    db.add(g); await db.commit(); await db.refresh(g); return g

@router.get("/ozet")
async def ozet(yil: int | None = Query(None), ay: int | None = Query(None), db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    q = select(Gider.kategori, func.sum(Gider.tutar).label("toplam"), func.count().label("adet"))
    if yil: q = q.where(extract("year", Gider.tarih) == yil)
    if ay: q = q.where(extract("month", Gider.tarih) == ay)
    result = await db.execute(q.group_by(Gider.kategori)); rows = result.all()
    return {"detay": [{"kategori": r[0], "toplam": float(r[1]), "adet": r[2]} for r in rows],
            "genel_toplam": sum(float(r[1]) for r in rows)}

@router.delete("/{gider_id}", status_code=204)
async def delete_gider(gider_id: int, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(Gider).where(Gider.id == gider_id))
    g = result.scalar_one_or_none()
    if not g: raise HTTPException(404, "Gider bulunamadı")
    await db.delete(g); await db.commit()
