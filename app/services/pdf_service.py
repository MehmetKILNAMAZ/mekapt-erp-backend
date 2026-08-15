import os
from datetime import datetime
from decimal import Decimal
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle

MAKBUZ_DIR = "/tmp/makbuzlar"
os.makedirs(MAKBUZ_DIR, exist_ok=True)

APART_ADI   = "PAŞA APARTMANI"
APART_ADRES = "Yayla Mah. 1396 Sok. No:4, Keçiören/ANKARA"
APART_TEL   = "0530 233 29 64"

def _para(tutar: Decimal) -> str:
    return f"₺{tutar:,.2f}"

def _nushaci(c: canvas, x0, y0, w, h, nsha: str, data: dict, renk):
    """Tek nüsha (A veya B) çizer."""
    c.setFillColor(renk)
    c.rect(x0, y0+h-1.2*cm, w, 1.2*cm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x0 + w/2, y0+h-0.85*cm, f"{APART_ADI}   |   {nsha}")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8)
    c.drawCentredString(x0 + w/2, y0+h-1.5*cm, APART_ADRES)

    rows = [
        ["Makbuz No", data["makbuz_no"]],
        ["Tarih",     data["tarih"]],
        ["Daire No",  str(data["daire_no"])],
        ["Sakin",     data["sakin_adi"]],
        ["Dönem",     data.get("donem","")],
        ["Tür",       data.get("gelir_turu","Aidat")],
        ["Tutar",     _para(data["tutar"])],
        ["Ödeme",     data.get("odeme_sekli","Nakit")],
    ]
    ts = TableStyle([
        ("FONTNAME",  (0,0),(-1,-1), "Helvetica"),
        ("FONTSIZE",  (0,0),(-1,-1), 8),
        ("FONTNAME",  (0,0),(0,-1), "Helvetica-Bold"),
        ("GRID",      (0,0),(-1,-1), 0.3, colors.grey),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.white, colors.HexColor("#F7F9FC")]),
        ("LEFTPADDING",(0,0),(-1,-1),4),
    ])
    t = Table(rows, colWidths=[2.8*cm, w-3.2*cm])
    t.setStyle(ts)
    t.wrapOn(c, w-0.4*cm, 6*cm)
    t.drawOn(c, x0+0.2*cm, y0+h-5.8*cm)

    c.setFont("Helvetica-Oblique", 7)
    c.drawString(x0+0.2*cm, y0+0.5*cm, "İmza / Kaşe: _________________________")
    c.setStrokeColor(renk); c.rect(x0, y0, w, h, fill=0, stroke=1)

def generate_otokopi_pdf(data: dict) -> str:
    fname = f"{data['makbuz_no'].replace('-','_')}.pdf"
    path  = os.path.join(MAKBUZ_DIR, fname)
    W, H  = A4
    c     = canvas.Canvas(path, pagesize=A4)

    # Ayırıcı kesik çizgi
    mid = H / 2
    c.setDash(4, 3); c.setStrokeColor(colors.grey)
    c.line(1*cm, mid, W-1*cm, mid)
    c.setDash(); c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(W/2, mid+2, "✂ Sakin Nüshası")
    c.drawCentredString(W/2, mid-8, "✂ Yönetim Nüshası")

    nw = W - 2*cm; nh = mid - 1.5*cm
    _nushaci(c, 1*cm, mid+0.5*cm, nw, nh, "Sakin Nüshası (B Kopyası)", data, colors.HexColor("#1D4ED8"))
    _nushaci(c, 1*cm, 1*cm,       nw, nh, "Yönetim Nüshası (A Kopyası)", data, colors.HexColor("#059669"))

    c.save()
    return path
