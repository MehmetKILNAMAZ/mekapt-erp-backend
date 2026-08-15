from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime
from ..database import get_db
from ..models.kasa import Kasa
from ..auth.jwt import get_current_user, require_admin

router = APIRouter(prefix="/kasa", tags=["kasa"])

class KasaIn(BaseModel):
    tarih: date; aciklama: str; kategori: str | None = None
    giren: Decimal = Decimal("0"); cikan: Decimal = Decimal("0")
    odeme_sekli: str = "Nakit"; ilgili_belge: str | None = None; olusturan: str | None = None

class KasaOut(KasaIn):
    id: int; belge_no: str; bakiye: Decimal; created_at: datetime
    class Config: from_attributes = True

async def _calc_bakiye(db) -> Decimal:
    r = await db.execute(select(func.sum(Kasa.giren) - func.sum(Kasa.cikan)).select_from(Kasa))
    return r.scalar() or Decimal("0")

@router.get("/", response_model=list[KasaOut])
async def list_kasa(yil: int | None = Query(None), ay: int | None = Query(None), db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    q = select(Kasa)
    if yil: q = q.where(extract("year", Kasa.tarih) == yil)
    if ay: q = q.where(extract("month", Kasa.tarih) == ay)
    result = await db.execute(q.order_by(Kasa.tarih.asc())); return result.scalars().all()

@router.post("/", response_model=KasaOut, status_code=201)
async def create_kasa(data: KasaIn, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    r = await db.execute(select(func.count()).select_from(Kasa)); count = r.scalar() or 0
    belge_no = f"KAS-{data.tarih.year}-{count+1:05d}"
    bakiye = await _calc_bakiye(db) + data.giren - data.cikan
    k = Kasa(**data.model_dump(), belge_no=belge_no, bakiye=bakiye)
    db.add(k); await db.commit(); await db.refresh(k); return k

@router.get("/ozet")
async def kasa_ozet(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    bakiye = await _calc_bakiye(db)
    r = await db.execute(select(func.sum(Kasa.giren), func.sum(Kasa.cikan)).select_from(Kasa))
    row = r.one()
    return {"bakiye": float(bakiye), "toplam_giren": float(row[0] or 0), "toplam_cikan": float(row[1] or 0)}
