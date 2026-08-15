from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..auth.jwt import get_current_user
from ..config import get_settings

router = APIRouter(prefix="/ai", tags=["ai"])
settings = get_settings()

class ChatIn(BaseModel):
    mesaj: str
    baglam: str | None = None

class ChatOut(BaseModel):
    yanit: str
    kullanim: dict | None = None

@router.post("/chat", response_model=ChatOut)
async def ai_chat(data: ChatIn, _=Depends(get_current_user)):
    if not settings.OPENAI_API_KEY:
        raise HTTPException(503, "OpenAI API anahtarı yapılandırılmamış")
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        system_msg = f"""Sen {settings.APARTMAN_ADI} apartman yönetim sisteminin yapay zeka asistanısın.
Apartman: {settings.APARTMAN_ADRES}. Sakinlere ve yöneticiye Türkçe, samimi ve profesyonel yanıtlar ver.
Aidat takibi, borç hatırlatma, bakım-arıza yönetimi, duyuru hazırlama konularında uzmanlaşmışsın."""
        messages = [{"role": "system", "content": system_msg}]
        if data.baglam:
            messages.append({"role": "system", "content": f"Bağlam: {data.baglam}"})
        messages.append({"role": "user", "content": data.mesaj})
        response = await client.chat.completions.create(model=settings.OPENAI_MODEL, messages=messages, max_tokens=1000, temperature=0.7)
        return {"yanit": response.choices[0].message.content, "kullanim": {"prompt_tokens": response.usage.prompt_tokens, "completion_tokens": response.usage.completion_tokens}}
    except Exception as e:
        raise HTTPException(500, f"AI hatası: {str(e)}")

@router.post("/hatirlat")
async def generate_hatirlatma(data: ChatIn, _=Depends(get_current_user)):
    if not settings.OPENAI_API_KEY:
        return {"yanit": "OpenAI API anahtarı gerekli"}
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        prompt = f"{settings.APARTMAN_ADI} için şu konuda kısa, nazik bir WhatsApp hatırlatma mesajı yaz: {data.mesaj}"
        response = await client.chat.completions.create(model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}], max_tokens=200)
        return {"yanit": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(500, f"AI hatası: {str(e)}")
