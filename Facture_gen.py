#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facture_gen.py — Génération de tickets PDF Nova Pharma
========================================================
Génère un ticket de caisse au format imprimante thermique (80mm).

- Signature HMAC (Réf. sécurité) : TOUJOURS affichée
- QR Code : OPTIONNEL (config `qrcode_actif`)
- Formatage compact des nombres (M / Md) pour éviter le débordement
- Word-wrap automatique dans les cellules (Paragraph)
"""

import hmac
import hashlib
import io
import re

import qrcode
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, Image,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from Database import db


# ══════════════════════════════════════════════════════════════════
# Constantes
# ══════════════════════════════════════════════════════════════════
DEFAULT_HMAC_KEY = "NOVA_PHARMA_SECURE_KEY_FALLBACK"

DEFAULT_MENTIONS = [
    "Les médicaments vendus ne sont ni repris ni échangés",
    "À conserver hors de la portée des enfants",
    "Signature ou cachet de la pharmacie",
]


# ══════════════════════════════════════════════════════════════════
# Formatage des nombres
# ══════════════════════════════════════════════════════════════════
def _fmt_number(value, devise: str = "") -> str:
    """
    Formate un nombre de façon compacte pour éviter le débordement.
      < 1 000         → "123 FC"
      < 1 000 000     → "12 345 FC"
      < 1 000 000 000 → "12.3 M FC"
      ≥ 1 000 000 000 → "1.23 Md FC"
    """
    try:
        v = float(value or 0)
    except Exception:
        v = 0.0

    if abs(v) < 1_000_000:
        s = f"{v:,.0f}".replace(",", " ")
    elif abs(v) < 1_000_000_000:
        s = f"{v / 1_000_000:.2f}".rstrip("0").rstrip(".") + " M"
    else:
        s = f"{v / 1_000_000_000:.2f}".rstrip("0").rstrip(".") + " Md"

    return f"{s} {devise}".strip()


# ══════════════════════════════════════════════════════════════════
# Styles des cellules (avec word-wrap)
# ══════════════════════════════════════════════════════════════════
def _make_cell_styles():
    """
    Retourne (style_left, style_center, style_right) pour les cellules
    de tableau. Chaque style active le word-wrap automatique.
    """
    base = dict(fontSize=7, leading=9, wordWrap="CJK")

    style_left = ParagraphStyle("cellL", alignment=TA_LEFT, **base)
    style_center = ParagraphStyle("cellC", alignment=TA_CENTER, **base)
    style_right = ParagraphStyle("cellR", alignment=TA_RIGHT, **base)

    return style_left, style_center, style_right


def _safe_cell(text, style, allow_html: bool = False) -> Paragraph:
    """
    Retourne un Paragraph sécurisé (échappe XML).
      - allow_html=False (défaut) : échappe TOUT le HTML
      - allow_html=True : conserve les balises <b>, <i>, <br/>
    """
    s = str(text or "")

    if allow_html:
        # Échappe seulement les & qui ne sont pas déjà des entités
        s = re.sub(
            r"&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)",
            "&amp;", s)
    else:
        s = (s.replace("&", "&amp;")
              .replace("<", "&lt;")
              .replace(">", "&gt;"))

    return Paragraph(s, style)


# ══════════════════════════════════════════════════════════════════
# Helpers HMAC / QR / Mentions
# ══════════════════════════════════════════════════════════════════
def _get_secret_key() -> bytes:
    """Récupère la clé HMAC depuis la base (fallback si absente)."""
    try:
        key = db.get_config("unique_key", "")
        if not key:
            return DEFAULT_HMAC_KEY.encode("utf-8")
        return str(key).encode("utf-8")
    except Exception:
        return DEFAULT_HMAC_KEY.encode("utf-8")


def _is_qrcode_active() -> bool:
    """Vérifie si le QR code est activé dans la config."""
    try:
        return bool(db.get_config("qrcode_actif", False))
    except Exception:
        return False


def _get_mentions(data: dict) -> list:
    """Récupère les mentions (data > DB > défaut)."""
    mentions = data.get("Mention", None)
    if mentions and isinstance(mentions, list):
        return mentions

    try:
        mentions_db = db.get_config("mentions_ticket", None)
        if mentions_db and isinstance(mentions_db, list):
            return mentions_db
    except Exception:
        pass

    return DEFAULT_MENTIONS


def _generate_signature(numero_facture: str, caisse: str) -> str:
    """Génère la signature HMAC courte (16 caractères hex)."""
    secret_key = _get_secret_key()
    base = f"{numero_facture}-{caisse}".encode("utf-8")
    return hmac.new(
        secret_key, base, hashlib.sha256
    ).hexdigest()[:16].upper()


def _generate_qr_buffer(numero_facture: str, caisse: str,
                        signature: str) -> io.BytesIO:
    """Génère un QR code en mémoire (BytesIO)."""
    qr_data = f"NOVA-{numero_facture}-{caisse}-{signature}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img_buffer = io.BytesIO()
    img_qr = qr.make_image(fill_color="black", back_color="white")
    img_qr.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return img_buffer


# ══════════════════════════════════════════════════════════════════
# Génération du ticket
# ══════════════════════════════════════════════════════════════════
def Generer_ticket_final(data: dict,
                         nom_fichier: str = "ticket_nova.pdf") -> None:
    """
    Génère un ticket PDF.

    `data` doit contenir :
      - Numero facture        : str
      - Numero de la caisse   : str
      - Produit vendu         : list[list] → [nom, qte, pu, total]
      - Numero client         : str
      - Nom client            : str
      - date                  : str
      - Total general         : float
      - Nom entreprise        : str
      - Adresse entreprise    : str (optionnel)
      - Telephone entreprise  : str (optionnel)
      - Mention               : list (optionnel)
    """
    numero_facture = data.get("Numero facture", "")
    caisse = data.get("Numero de la caisse", "")

    # ─── A. SIGNATURE HMAC ───
    signature = _generate_signature(numero_facture, caisse)

    # ─── B. QR CODE (optionnel) ───
    qr_actif = _is_qrcode_active()
    img_buffer = None
    if qr_actif:
        try:
            img_buffer = _generate_qr_buffer(
                numero_facture, caisse, signature)
        except Exception:
            img_buffer = None

    # ─── C. STYLES ───
    style_center = ParagraphStyle(
        "Center", fontSize=8, alignment=TA_CENTER)
    style_header = ParagraphStyle(
        "Header", fontSize=12, alignment=TA_CENTER,
        fontName="Helvetica-Bold")
    style_small = ParagraphStyle(
        "Small", fontSize=7, leading=9)
    style_tot = ParagraphStyle(
        "Tot", alignment=TA_RIGHT, fontSize=10,
        fontName="Helvetica-Bold")

    cell_left, cell_center, cell_right = _make_cell_styles()

    # ─── D. DOCUMENT PDF ───
    doc = SimpleDocTemplate(
        nom_fichier,
        pagesize=(80 * mm, 300 * mm),
        rightMargin=2 * mm, leftMargin=2 * mm,
        topMargin=5 * mm, bottomMargin=5 * mm,
    )

    elements = []

    # ─── En-tête entreprise ───
    nom_entreprise = data.get("Nom entreprise", "NOVA PHARMA")
    adresse = data.get("Adresse entreprise", "")
    telephone = data.get("Telephone entreprise", "")

    elements.append(Paragraph(nom_entreprise, style_header))
    if adresse:
        elements.append(Paragraph(adresse, style_center))
    if telephone:
        elements.append(Paragraph(f"Tél : {telephone}", style_center))
    elements.append(Paragraph(
        "---------------------------------------", style_center))

    # ─── Métadonnées ───
    elements.append(Paragraph(f"Date: {data.get('date', '')}", style_small))
    elements.append(Paragraph(
        f"FAC N°: {numero_facture} | Caisse: {caisse}", style_small))
    elements.append(Paragraph(
        f"Client: {data.get('Nom client', '—')}", style_small))
    elements.append(Paragraph(
        f"Tél: {data.get('Numero client', '—')}", style_small))
    elements.append(Spacer(1, 2 * mm))

    # ═══════════════════════════════════════════════════════════════
    # TABLEAU DES PRODUITS
    #   Colonnes : 30 + 8 + 17 + 21 = 76 mm
    #   _fmt_number → montants compacts
    #   Paragraph   → word-wrap automatique
    # ═══════════════════════════════════════════════════════════════
    table_data = [[
        _safe_cell("Produit", cell_left),
        _safe_cell("Qté", cell_center),
        _safe_cell("P.U", cell_right),
        _safe_cell("Total", cell_right),
    ]]

    for p in data.get("Produit vendu", []):
        nom_produit = str(p[0])
        qte_str = str(p[1])
        pu_str = _fmt_number(p[2], "")
        tot_str = _fmt_number(p[3], "")

        table_data.append([
            _safe_cell(f"<b>{nom_produit}</b>", cell_left,
                       allow_html=True),
            _safe_cell(qte_str, cell_center),
            _safe_cell(pu_str, cell_right),
            _safe_cell(tot_str, cell_right),
        ])

    t = Table(
        table_data,
        colWidths=[30 * mm, 8 * mm, 17 * mm, 21 * mm],
        repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 1),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1),
    ]))
    elements.append(t)

    # ─── Total général ───
    elements.append(Spacer(1, 2 * mm))
    total_general = data.get("Total general", 0)
    total_txt = f"<b>TOTAL : {_fmt_number(total_general, 'FC')}</b>"
    elements.append(Paragraph(total_txt, style_tot))

    # ═══════════════════════════════════════════════════════════════
    # RÉF. SÉCURITÉ
    # ═══════════════════════════════════════════════════════════════
    elements.append(Spacer(1, 3 * mm))
    style_ref = ParagraphStyle(
        "Ref", fontSize=8, alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#023E8A"))
    elements.append(Paragraph(f"Réf. sécurité : {signature}", style_ref))
    elements.append(Spacer(1, 1 * mm))

    # ─── QR CODE ───
    if qr_actif and img_buffer is not None:
        elements.append(Spacer(1, 2 * mm))
        qr_img = Image(img_buffer, width=30 * mm, height=30 * mm)
        elements.append(qr_img)

    # ─── Mentions ───
    mentions = _get_mentions(data)
    elements.append(Spacer(1, 3 * mm))
    for m in mentions:
        elements.append(_safe_cell(m, style_center))
        elements.append(Spacer(1, 1 * mm))

    # ─── Build ───
    doc.build(elements)
    print(f"Ticket généré : {nom_fichier}")


# ══════════════════════════════════════════════════════════════════
# Test autonome
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    db.get_conn()

    print("→ Config actuelle :")
    print(f"   qrcode_actif        : {db.get_config('qrcode_actif', False)}")
    print(f"   unique_key définie  : {bool(db.get_config('unique_key', ''))}")
    print(f"   mentions définies   : "
          f"{bool(db.get_config('mentions_ticket', None))}")
    print()

    pharmacie = db.query_one(
        "SELECT nom, adresse, numero FROM Pharmacie WHERE id = 1 LIMIT 1")
    if pharmacie:
        nom_entreprise = pharmacie["nom"] or "NOVA PHARMA"
        adresse = pharmacie["adresse"] or ""
        telephone = pharmacie["numero"] or ""
    else:
        nom_entreprise = "NOVA PHARMA"
        adresse = ""
        telephone = ""

    # ─── Test avec montants courts ───
    donnees_test = {
        "Numero facture": "FA-2026-000001",
        "Numero de la caisse": "A",
        "Produit vendu": [
            ["Panadol Advance", 4, 4500, 18000],
            ["Aspirine", 2, 1000, 2000],
        ],
        "Numero client": "0861180044",
        "Nom client": "AARON STAM JOHN",
        "date": "31/01/2026 00:58:17",
        "Total general": 20000,
        "Nom entreprise": nom_entreprise,
        "Adresse entreprise": adresse,
        "Telephone entreprise": telephone,
    }
    Generer_ticket_final(donnees_test, "ticket_test.pdf")

    # ─── Test avec gros montants (milliards) ───
    donnees_big = {
        "Numero facture": "FA-2026-000999",
        "Numero de la caisse": "A",
        "Produit vendu": [
            ["Paracétamol 500mg — Boîte de 20 comprimés",
             1234, 12500, 15425000],
            ["Amoxicilline 1g — Boîte de 12",
             500, 45678, 22839000],
            ["Médicament Ultra Cher",
             1000, 1500000, 1500000000],
        ],
        "Numero client": "0861180044",
        "Nom client": "AARON STAM JOHN",
        "date": "31/01/2026 00:58:17",
        "Total general": 1536284000,
        "Nom entreprise": nom_entreprise,
        "Adresse entreprise": adresse,
        "Telephone entreprise": telephone,
    }
    Generer_ticket_final(donnees_big, "ticket_test_big.pdf")