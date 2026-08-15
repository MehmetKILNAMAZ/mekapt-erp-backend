from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import *  # noqa — register all models
from .routers import (auth, daire, gelir, gider, makbuz, borc,
                      ariza, duyuru, mesaj, kasa, personel, ai_asistan)
from .config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Mekapt AYS-ERP API",
    description="Paşa Apartmanı Yönetim Sistemi v2.0",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PREFIX = "/api/v1"
app.include_router(auth.router,        prefix=PREFIX)
app.include_router(daire.router,       prefix=PREFIX)
app.include_router(gelir.router,       prefix=PREFIX)
app.include_router(gider.router,       prefix=PREFIX)
app.include_router(makbuz.router,      prefix=PREFIX)
app.include_router(borc.router,        prefix=PREFIX)
app.include_router(ariza.router,       prefix=PREFIX)
app.include_router(duyuru.router,      prefix=PREFIX)
app.include_router(mesaj.router,       prefix=PREFIX)
app.include_router(kasa.router,        prefix=PREFIX)
app.include_router(personel.router,    prefix=PREFIX)
app.include_router(ai_asistan.router,  prefix=PREFIX)

@app.get("/health")
async def health():
    return {"status": "ok", "app": "Mekapt AYS-ERP", "version": "2.0.0"}

@app.get("/")
async def root():
    return {"message": "Paşa Apartmanı AYS-ERP API v2.0", "docs": "/docs"}
