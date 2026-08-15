from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..models.makbuz import Makbuz
from ..auth.jwt import get_current_user
import os

router = APIRouter(prefix="/makbuzlar", tags=["makbuzlar"])

@router.get("/")
async def list_makbuzlar(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Makbuz).order_by(Makbuz.tarih.desc()))
    makbuzlar = result.scalars().all()
    return [{"id": m.id, "makbuz_no": m.makbuz_no, "tarih": str(m.tarih), "daire_no": m.daire_no,
             "sakin_adi": m.sakin_adi, "tutar": float(m.tutar), "odeme_sekli": m.odeme_sekli,
             "donem": m.donem, "durum": m.durum, "whatsapp_gonderildi": m.whatsapp_gonderildi} for m in makbuzlar]

@router.get("/daire/{daire_no}")
async def makbuzlar_by_daire(daire_no: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Makbuz).where(Makbuz.daire_no == daire_no).order_by(Makbuz.tarih.desc()))
    makbuzlar = result.scalars().all()
    return [{"id": m.id, "makbuz_no": m.makbuz_no, "tarih": str(m.tarih), "tutar": float(m.tutar),
             "odeme_sekli": m.odeme_sekli, "donem": m.donem, "durum": m.durum} for m in makbuzlar]
