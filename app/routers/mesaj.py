from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db, AsyncSessionLocal
from ..models.mesaj import Mesaj
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/mesajlar", tags=["mesajlar"])

class MesajIn(BaseModel):
    daire_no: int; gonderen: str; icerik: str

class MesajOut(MesajIn):
    id: int; okundu: bool; olusturulma: datetime
    class Config: from_attributes = True

class ConnectionManager:
    def __init__(self): self.active: dict[int, list[WebSocket]] = {}
    async def connect(self, daire_no: int, ws: WebSocket):
        await ws.accept(); self.active.setdefault(daire_no, []).append(ws)
    def disconnect(self, daire_no: int, ws: WebSocket):
        if daire_no in self.active: self.active[daire_no].discard(ws)
    async def broadcast(self, daire_no: int, data: dict):
        for ws in list(self.active.get(daire_no, [])):
            try: await ws.send_json(data)
            except: self.active[daire_no].discard(ws)

manager = ConnectionManager()

@router.get("/{daire_no}", response_model=list[MesajOut])
async def get_mesajlar(daire_no: int, limit: int = Query(50), db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Mesaj).where(Mesaj.daire_no == daire_no).order_by(Mesaj.olusturulma.asc()).limit(limit))
    return result.scalars().all()

@router.post("/", response_model=MesajOut, status_code=201)
async def send_mesaj(data: MesajIn, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    m = Mesaj(**data.model_dump()); db.add(m); await db.commit(); await db.refresh(m)
    await manager.broadcast(m.daire_no, {"id": m.id, "daire_no": m.daire_no, "gonderen": m.gonderen,
                                          "icerik": m.icerik, "okundu": m.okundu,
                                          "olusturulma": m.olusturulma.isoformat()})
    return m

@router.websocket("/ws/{daire_no}")
async def websocket_endpoint(websocket: WebSocket, daire_no: int):
    await manager.connect(daire_no, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            async with AsyncSessionLocal() as db:
                m = Mesaj(daire_no=daire_no, gonderen=data.get("gonderen","sakin"), icerik=data.get("icerik",""))
                db.add(m); await db.commit(); await db.refresh(m)
            await manager.broadcast(daire_no, {"id": m.id, "daire_no": daire_no, "gonderen": m.gonderen,
                                                "icerik": m.icerik, "okundu": False, "olusturulma": m.olusturulma.isoformat()})
    except WebSocketDisconnect:
        manager.disconnect(daire_no, websocket)
