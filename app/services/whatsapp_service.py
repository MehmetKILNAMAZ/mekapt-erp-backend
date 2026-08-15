import os
from twilio.rest import Client
from ..config import get_settings

settings = get_settings()

def _client():
    return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def _from_number():
    return f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}"

def send_makbuz_bilgi(to_phone: str, makbuz_no: str, sakin_adi: str,
                      tutar: float, donem: str, daire_no: int) -> str:
    msg_body = (
        f"🏢 *PAŞA APARTMANI*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ Makbuz Bilgisi\n"
        f"Makbuz No : {makbuz_no}\n"
        f"Daire No  : {daire_no}\n"
        f"Sakin     : {sakin_adi}\n"
        f"Dönem     : {donem}\n"
        f"Tutar     : ₺{tutar:,.2f}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Ödemeniz alınmıştır. İyi günler 🙏"
    )
    to = f"whatsapp:+90{to_phone.lstrip('0')}" if not to_phone.startswith("+") else f"whatsapp:{to_phone}"
    msg = _client().messages.create(body=msg_body, from_=_from_number(), to=to)
    return msg.sid

def send_borc_hatirlatma(to_phone: str, sakin_adi: str, daire_no: int,
                          tutar: float, donem: str, vade: str = "") -> str:
    msg_body = (
        f"🏢 *PAŞA APARTMANI* — Hatırlatma\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Sayın {sakin_adi},\n"
        f"Daire No : {daire_no}\n"
        f"Dönem    : {donem}\n"
        f"Borç     : ₺{tutar:,.2f}\n"
        + (f"Vade     : {vade}\n" if vade else "")
        + f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Ödemenizi en kısa sürede yapmanızı rica ederiz.\n"
        f"İletişim: {settings.APARTMAN_TELEFON}"
    )
    to = f"whatsapp:+90{to_phone.lstrip('0')}" if not to_phone.startswith("+") else f"whatsapp:{to_phone}"
    msg = _client().messages.create(body=msg_body, from_=_from_number(), to=to)
    return msg.sid

def send_duyuru(to_phone: str, konu: str, icerik: str) -> str:
    msg_body = (
        f"📢 *PAŞA APARTMANI* — Duyuru\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 {konu}\n\n"
        f"{icerik}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Paşa Apartmanı Yönetimi"
    )
    to = f"whatsapp:+90{to_phone.lstrip('0')}" if not to_phone.startswith("+") else f"whatsapp:{to_phone}"
    msg = _client().messages.create(body=msg_body, from_=_from_number(), to=to)
    return msg.sid
