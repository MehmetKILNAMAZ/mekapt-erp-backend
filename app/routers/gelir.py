from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime
from ..database import get_db
from ..models.gelir import Gelir
from ..models.makbuz import Makbuz
from ..auth.jwt import get_current_user, require_admin

router = APIRouter(prefix="/gelirler", tags=["gelirler"])

class GelirIn(BaseModel):
    tarih: date
    daire_no: int
    sakin_adi: str
    gelir_turu: str = "Aidat"
    tutar: Decimal
    odeme_sekli: str = "Nakit"
    donem_yil: int | None = None
    donem_ay: int | None = None
    notlar: str | None = None

class GelirOut(GelirIn):
    id: int; sira_no: int; makbuz_no: str; created_at: datetime
    class Config: from_attributes = True

async def _next_sira(db) -> int:
    result = await db.execute(select(func.max(Gelir.sira_no)))
    val = result.scalar() or 0; return val + 1

async def _make_makbuz_no(db, tarih: date) -> str:
    result = await db.execute(select(func.count()).select_from(Gelir).where(extract("year", Gelir.tarih)==tarih.year))
    count = result.scalar() or 0
    return f"G-{tarih.year}-{count+1:04d}"

@router.get("/", response_model=list[GelirOut])
async def list_gelirler(yil: int | None = Query(None), ay: int | None = Query(None),
                        daire_no: int | None = Query(None), db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    q = select(Gelir)
    if yil: q = q.where(extract("year", Gelir.tarih) == yil)
    if ay: q = q.where(extract("month", Gelir.tarih) == ay)
    if daire_no: q = q.where(Gelir.daire_no == daire_no)
    result = await db.execute(q.order_by(Gelir.tarih.desc())); return result.scalars().all()

@router.post("/", response_model=GelirOut, status_code=201)
async def create_gelir(data: GelirIn, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    sira = await _next_sira(db); mkno = await _make_makbuz_no(db, data.tarih)
    g = Gelir(**data.model_dump(), sira_no=sira, makbuz_no=mkno)
    db.add(g); await db.flush()
    m = Makbuz(makbuz_no=mkno, tarih=data.tarih, daire_no=data.daire_no, sakin_adi=data.sakin_adi,
               tutar=data.tutar, odeme_sekli=data.odeme_sekli, gelir_id=g.id,
               donem=f"{data.donem_yil}/{data.donem_ay:02d}" if data.donem_yil and data.donem_ay else None)
    db.add(m); await db.commit(); await db.refresh(g); return g

@router.get("/ozet")
async def ozet(yil: int | None = Query(None), ay: int | None = Query(None), db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    q = select(Gelir.gelir_turu, func.sum(Gelir.tutar).label("toplam"), func.count().label("adet"))
    if yil: q = q.where(extract("year", Gelir.tarih) == yil)
    if ay: q = q.where(extract("month", Gelir.tarih) == ay)
    result = await db.execute(q.group_by(Gelir.gelir_turu))
    rows = result.all()
    return {"detay": [{"tur": r[0], "toplam": float(r[1]), "adet": r[2]} for r in rows],
            "genel_toplam": sum(float(r[1]) for r in rows)}

@router.delete("/{gelir_id}", status_code=204)
async def delete_gelir(gelir_id: int, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(Gelir).where(Gelir.id == gelir_id))
    g = result.scalar_one_or_none()
    if not g: raise HTTPException(404, "Gelir bulunamadı")
    await db.delete(g); await db.commit()
