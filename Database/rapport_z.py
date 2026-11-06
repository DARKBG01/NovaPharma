#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rapport_z.py — Moteur du Rapport Z (clôture de caisse).
========================================================
Fonctions :
  • compute_rapport_z() : agrège les ventes pour la période
  • next_numero_z()     : génère Z-CAISSE-YYYYMMDD-NNN
  • save_rapport_z()    : INSERT + audit
  • generate_pdf_ticket() : ticket thermique 80mm
  • generate_pdf_a4()     : rapport A4 complet
"""

import json
import logging
import os
from datetime import datetime, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from Database import db, audit

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Palette
# ══════════════════════════════════════════════════════════════════
PRIMARY  = colors.HexColor("#023E8A")
BLUE     = colors.HexColor("#0077B6")
CYAN     = colors.HexColor("#00B4D8")
DANGER   = colors.HexColor("#DC2626")
SUCCESS  = colors.HexColor("#16A34A")
WARNING  = colors.HexColor("#F4A261")
GREY     = colors.HexColor("#64748B")
LIGHT    = colors.HexColor("#F8FAFC")
BORDER   = colors.HexColor("#E2E8F0")


# ══════════════════════════════════════════════════════════════════
# Helpers dates (Historique stocke en DD/MM/YYYY HH:MM:SS)
# ══════════════════════════════════════════════════════════════════
def _iso_expr(col: str) -> str:
    return (
        f"(substr({col}, 7, 4) || '-' || "
        f"substr({col}, 4, 2) || '-' || "
        f"substr({col}, 1, 2) || "
        f"substr({col}, 11))"
    )


def _fr(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# ══════════════════════════════════════════════════════════════════
# Moteur — calcul
# ══════════════════════════════════════════════════════════════════
def resolve_period(periode: str, date_debut=None, date_fin=None,
                   caisse: str = None) -> tuple:
    """
    Retourne (debut, fin) en datetime.
    Accepte date OU datetime en entrée.
    """
    from datetime import datetime as _dt, date as _date

    # ─── Normalise date → datetime ───
    def _to_datetime(x):
        if x is None:
            return None
        if isinstance(x, _dt):
            return x
        if isinstance(x, _date):
            return _dt(x.year, x.month, x.day)
        return None

    date_debut = _to_datetime(date_debut)
    date_fin = _to_datetime(date_fin)

    now = datetime.now()

    if periode == "Aujourd'hui":
        debut = now.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = now

    elif periode == "Hier":
        hier = now - timedelta(days=1)
        debut = hier.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = hier.replace(hour=23, minute=59, second=59)

    elif periode == "7 derniers jours":
        debut = (now - timedelta(days=7)).replace(
            hour=0, minute=0, second=0, microsecond=0)
        fin = now

    elif periode == "Shift en cours":
        debut = _last_shift_end(caisse) or now.replace(
            hour=0, minute=0, second=0, microsecond=0)
        fin = now

    elif periode == "Personnalisé" and date_debut and date_fin:
        debut = date_debut.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = date_fin.replace(hour=23, minute=59, second=59)

    else:
        debut = now.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = now

    return debut, fin


def _last_shift_end(caisse: str = None):
    """Retourne la date_fin du dernier Z de cette caisse, ou None."""
    try:
        q = ("SELECT date_fin FROM RapportZ "
             "WHERE 1=1")
        p = []
        if caisse:
            q += " AND caisse = ?"
            p.append(caisse)
        q += " ORDER BY date_fin DESC LIMIT 1"
        row = db.query_one(q, tuple(p))
        if row and row["date_fin"]:
            return datetime.fromisoformat(row["date_fin"])
    except Exception:
        logger.exception("Erreur _last_shift_end")
    return None


def compute_rapport_z(caisse: str, debut: datetime, fin: datetime) -> dict:
    """
    Agrège toutes les données du rapport Z pour la période.
    """
    debut_iso = _fr(debut)
    fin_iso = _fr(fin)

    date_iso = _iso_expr("Date_vent")
    where_base = f"{date_iso} >= ? AND {date_iso} <= ?"
    params_base = [debut_iso, fin_iso]

    # Filtre caisse si précisé
    if caisse and caisse != "*":
        where_base += " AND Caisse = ?"
        params_base.append(caisse)

    # ─── Totaux ventes ───
    row = db.query_one(
        f"""SELECT
             COALESCE(SUM(Total), 0)     AS ca,
             COUNT(DISTINCT Num_fact)    AS nb_fact,
             COALESCE(SUM(Quantite), 0)  AS nb_art
           FROM Historique
           WHERE {where_base} AND annule = 0""",
        tuple(params_base))
    ca = float(row["ca"] or 0) if row else 0
    nb_fact = int(row["nb_fact"] or 0) if row else 0
    nb_art = int(row["nb_art"] or 0) if row else 0
    panier = (ca / nb_fact) if nb_fact else 0

    # ─── Clients identifiés / anonymes ───
    row = db.query_one(
        f"""SELECT
             COUNT(DISTINCT CASE
                 WHEN Client_name IS NOT NULL
                  AND Client_name != ''
                  AND Client_name NOT LIKE '%anonyme%'
                 THEN Client_name END) AS nb_ident,
             COUNT(DISTINCT CASE
                 WHEN Client_name IS NULL
                   OR Client_name = ''
                   OR Client_name LIKE '%anonyme%'
                 THEN Num_fact END) AS nb_anon
           FROM Historique
           WHERE {where_base} AND annule = 0""",
        tuple(params_base))
    nb_ident = int(row["nb_ident"] or 0) if row else 0
    nb_anon = int(row["nb_anon"] or 0) if row else 0

    # ─── Annulations ───
    row = db.query_one(
        f"""SELECT
             COUNT(DISTINCT Num_fact) AS nb,
             COALESCE(SUM(Total), 0)  AS montant
           FROM Historique
           WHERE {where_base} AND annule = 1""",
        tuple(params_base))
    nb_annul = int(row["nb"] or 0) if row else 0
    montant_annul = float(row["montant"] or 0) if row else 0

    # ─── Top 5 produits ───
    rows = db.query(
        f"""SELECT Article AS nom,
                  COALESCE(SUM(Quantite), 0) AS qte,
                  COALESCE(SUM(Total), 0)    AS ca
           FROM Historique
           WHERE {where_base} AND annule = 0
           GROUP BY Article
           ORDER BY ca DESC LIMIT 5""",
        tuple(params_base))
    top_produits = [
        {"nom": r["nom"], "qte": int(r["qte"]), "ca": float(r["ca"])}
        for r in rows
    ]

    # ─── Détail par heure ───
    rows = db.query(
        f"""SELECT substr(Date_vent, 12, 2) AS hh,
                  COUNT(DISTINCT Num_fact) AS n
           FROM Historique
           WHERE {where_base} AND annule = 0
           GROUP BY hh ORDER BY hh ASC""",
        tuple(params_base))
    detail_heure = [
        {"heure": int(r["hh"]), "n_ventes": int(r["n"])}
        for r in rows if r["hh"]
    ]

    # ─── Infos pharmacie ───
    ph = db.query_one(
        "SELECT nom, adresse, numero FROM Pharmacie "
        "WHERE id = 1 LIMIT 1")
    nom_pharmacie = ph["nom"] if ph else "NOVA PHARMA"
    adresse_pharmacie = ph["adresse"] if ph else ""
    telephone_pharmacie = ph["numero"] if ph else ""

    devise = db.get_config("devise", "FC")

    return {
        "caisse": caisse,
        "debut": debut_iso,
        "fin": fin_iso,
        "ca_total": ca,
        "nb_factures": nb_fact,
        "nb_articles": nb_art,
        "panier_moyen": panier,
        "nb_clients_ident": nb_ident,
        "nb_clients_anon": nb_anon,
        "nb_annulations": nb_annul,
        "montant_annule": montant_annul,
        "top_produits": top_produits,
        "detail_heure": detail_heure,
        "nom_pharmacie": nom_pharmacie,
        "adresse_pharmacie": adresse_pharmacie,
        "telephone_pharmacie": telephone_pharmacie,
        "devise": devise,
    }


# ══════════════════════════════════════════════════════════════════
# Numérotation
# ══════════════════════════════════════════════════════════════════
def next_numero_z(caisse: str) -> str:
    """Génère Z-{caisse}-{YYYYMMDD}-{NNN}."""
    today = datetime.now().strftime("%Y%m%d")
    prefix = f"Z-{caisse}-{today}-"

    try:
        row = db.query_one(
            "SELECT numero_z FROM RapportZ "
            "WHERE numero_z LIKE ? "
            "ORDER BY numero_z DESC LIMIT 1",
            (f"{prefix}%",))
        if row and row["numero_z"]:
            try:
                n = int(row["numero_z"].split("-")[-1]) + 1
            except (ValueError, IndexError):
                n = 1
        else:
            n = 1
    except Exception:
        n = 1

    return f"{prefix}{n:03d}"


# ══════════════════════════════════════════════════════════════════
# Persistance
# ══════════════════════════════════════════════════════════════════
def save_rapport_z(data: dict, user_id: str,
                   user_name: str,
                   montant_compte: float,
                   format_pdf: str = "ticket",
                   chemin_pdf: str = "") -> str:
    """
    Enregistre le Rapport Z et log dans l'audit.
    Retourne l'ID.
    """
    numero_z = next_numero_z(data["caisse"])
    rid = db.new_id()
    ecart = float(montant_compte) - float(data["ca_total"])

    with db.transaction():
        db.execute("""
            INSERT INTO RapportZ (
                id, numero_z, caisse, date_debut, date_fin,
                utilisateur_id, utilisateur_name,
                nb_factures, nb_articles, ca_total, panier_moyen,
                nb_clients_ident, nb_clients_anon,
                nb_annulations, montant_annule,
                montant_compte, ecart,
                top_produits, detail_heure,
                format_pdf, chemin_pdf
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            rid, numero_z, data["caisse"],
            data["debut"], data["fin"],
            user_id, user_name,
            data["nb_factures"], data["nb_articles"],
            data["ca_total"], data["panier_moyen"],
            data["nb_clients_ident"], data["nb_clients_anon"],
            data["nb_annulations"], data["montant_annule"],
            float(montant_compte), ecart,
            json.dumps(data["top_produits"], ensure_ascii=False),
            json.dumps(data["detail_heure"], ensure_ascii=False),
            format_pdf, chemin_pdf,
        ))

    # Audit
    try:
        audit.log(
            "RAPPORT_Z_GENERE",
            utilisateur_id=user_id,
            utilisateur_name=user_name,
            cible_type="rapport_z",
            cible_id=rid,
            cible_nom=numero_z,
            details={
                "caisse": data["caisse"],
                "ca_total": data["ca_total"],
                "montant_compte": float(montant_compte),
                "ecart": ecart,
                "nb_factures": data["nb_factures"],
                "format_pdf": format_pdf,
            },
            severite="info")
    except Exception:
        logger.exception("Erreur audit Rapport Z")

    return rid


# ══════════════════════════════════════════════════════════════════
# PDF — Format TICKET 80mm
# ══════════════════════════════════════════════════════════════════
def generate_pdf_ticket(data: dict, montant_compte: float,
                        numero_z: str, output_path: str) -> str:
    """Génère un ticket thermique 80mm."""
    # 80mm ≈ 226 points
    ticket_width = 76 * mm
    ticket_height = 200 * mm

    styles = getSampleStyleSheet()

    def P(text, size=8, bold=False, center=True, color=colors.black):
        style = ParagraphStyle(
            f"p_{size}_{bold}_{center}",
            parent=styles["Normal"],
            fontSize=size,
            leading=size + 2,
            fontName="Helvetica-Bold" if bold else "Helvetica",
            textColor=color,
            alignment=TA_CENTER if center else TA_LEFT)
        return Paragraph(text, style)

    def line():
        return P("─" * 42, size=7, center=True, color=GREY)

    story = []

    # Header
    story.append(P(data["nom_pharmacie"][:30], size=11, bold=True))
    if data["adresse_pharmacie"]:
        story.append(P(data["adresse_pharmacie"][:36], size=7))
    if data["telephone_pharmacie"]:
        story.append(P(f"Tel: {data['telephone_pharmacie']}", size=7))
    story.append(Spacer(1, 4))
    story.append(line())

    story.append(P("RAPPORT Z", size=12, bold=True))
    story.append(P(f"Caisse {data['caisse']}", size=9, bold=True))
    story.append(P(numero_z, size=7, color=GREY))
    story.append(line())

    # Période
    debut = data["debut"][:16].replace("-", "/")
    fin = data["fin"][:16].replace("-", "/")
    story.append(P(f"Du {debut}", size=7, center=False))
    story.append(P(f"Au {fin}", size=7, center=False))
    story.append(line())

    devise = data["devise"]

    # Ventes
    story.append(P("VENTES", size=8, bold=True, center=False))
    story.append(P(f"Factures .......... {data['nb_factures']}",
                   size=8, center=False))
    story.append(P(f"Articles .......... {data['nb_articles']}",
                   size=8, center=False))
    story.append(P(f"CA total .......... {data['ca_total']:,.0f} {devise}"
                   .replace(",", " "), size=9, bold=True, center=False))
    story.append(P(f"Panier moyen ...... {data['panier_moyen']:,.0f} {devise}"
                   .replace(",", " "), size=8, center=False))
    story.append(line())

    # Clients
    story.append(P("CLIENTS", size=8, bold=True, center=False))
    story.append(P(f"Identifies ........ {data['nb_clients_ident']}",
                   size=8, center=False))
    story.append(P(f"Anonymes .......... {data['nb_clients_anon']}",
                   size=8, center=False))
    story.append(line())

    # Annulations
    story.append(P("ANNULATIONS", size=8, bold=True, center=False))
    story.append(P(f"Nombre ............ {data['nb_annulations']}",
                   size=8, center=False))
    story.append(P(f"Montant ........... {data['montant_annule']:,.0f} {devise}"
                   .replace(",", " "), size=8, center=False))
    story.append(line())

    # Top 5
    if data["top_produits"]:
        story.append(P("TOP 5 PRODUITS", size=8, bold=True, center=False))
        for i, p in enumerate(data["top_produits"][:5], 1):
            nom = p["nom"][:22]
            story.append(P(f"{i}. {nom:<22} {p['qte']:>3} u",
                           size=7, center=False))
        story.append(line())

    # Contrôle caisse
    story.append(P("CONTROLE CAISSE", size=9, bold=True, center=False))
    story.append(P(f"Attendu ........... {data['ca_total']:,.0f} {devise}"
                   .replace(",", " "), size=8, center=False))
    story.append(P(f"Compte ............ {montant_compte:,.0f} {devise}"
                   .replace(",", " "), size=8, center=False))

    ecart = montant_compte - data["ca_total"]
    if abs(ecart) < 1:
        ecart_color = SUCCESS
        ecart_txt = "OK"
    elif ecart < 0:
        ecart_color = DANGER
        ecart_txt = "MANQUE"
    else:
        ecart_color = WARNING
        ecart_txt = "EXCEDENT"

    story.append(P(f"ECART ............. {ecart:+,.0f} {devise} ({ecart_txt})"
                   .replace(",", " "),
                   size=9, bold=True, center=False, color=ecart_color))
    story.append(line())

    story.append(Spacer(1, 8))
    story.append(P("Signature :", size=8, center=False))
    story.append(Spacer(1, 24))
    story.append(P("_" * 30, size=8))

    story.append(Spacer(1, 8))
    story.append(line())
    story.append(P(
        f"Imprime le {datetime.now().strftime('%d/%m/%Y a %H:%M')}",
        size=7, color=GREY))

    # Build
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=(ticket_width, ticket_height),
        leftMargin=4 * mm, rightMargin=4 * mm,
        topMargin=4 * mm, bottomMargin=4 * mm,
        title=f"Rapport Z {numero_z}")
    doc.build(story)

    return output_path


# ══════════════════════════════════════════════════════════════════
# PDF — Format A4
# ══════════════════════════════════════════════════════════════════
def generate_pdf_a4(data: dict, montant_compte: float,
                    numero_z: str, output_path: str) -> str:
    """Génère un rapport A4 détaillé."""
    styles = getSampleStyleSheet()

    def H1(t):
        return Paragraph(t, ParagraphStyle(
            "h1", parent=styles["Heading1"],
            fontSize=20, leading=26, textColor=PRIMARY,
            fontName="Helvetica-Bold", spaceAfter=10))

    def H2(t):
        return Paragraph(t, ParagraphStyle(
            "h2", parent=styles["Heading2"],
            fontSize=13, leading=18, textColor=BLUE,
            fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=8))

    def P(t, size=10, center=False, color=colors.black, bold=False):
        return Paragraph(t, ParagraphStyle(
            f"p_{size}", parent=styles["Normal"],
            fontSize=size, leading=size + 4,
            fontName="Helvetica-Bold" if bold else "Helvetica",
            textColor=color,
            alignment=TA_CENTER if center else TA_LEFT))

    def table(data_rows, col_widths=None):
        t = Table(data_rows, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, LIGHT]),
        ]))
        return t

    story = []

    # En-tête
    story.append(H1(f"Rapport Z — Caisse {data['caisse']}"))
    story.append(P(
        f"{data['nom_pharmacie']}  •  {numero_z}",
        size=11, color=GREY))
    story.append(Spacer(1, 6))

    debut = data["debut"][:16]
    fin = data["fin"][:16]
    story.append(P(f"Période : {debut} → {fin}", size=10))
    story.append(Spacer(1, 14))

    devise = data["devise"]

    # ─── KPIs globaux ───
    story.append(H2("Synthèse"))

    kpi_data = [
        ["Indicateur", "Valeur"],
        ["Nombre de factures", f"{data['nb_factures']}"],
        ["Nombre d'articles vendus", f"{data['nb_articles']}"],
        ["Chiffre d'affaires",
         f"{data['ca_total']:,.0f} {devise}".replace(",", " ")],
        ["Panier moyen",
         f"{data['panier_moyen']:,.0f} {devise}".replace(",", " ")],
        ["Clients identifiés", f"{data['nb_clients_ident']}"],
        ["Clients anonymes", f"{data['nb_clients_anon']}"],
        ["Annulations", f"{data['nb_annulations']}"],
        ["Montant annulé",
         f"{data['montant_annule']:,.0f} {devise}".replace(",", " ")],
    ]
    story.append(table(kpi_data, col_widths=[9 * cm, 6 * cm]))
    story.append(Spacer(1, 12))

    # ─── Contrôle caisse ───
    story.append(H2("Contrôle de caisse"))

    ecart = montant_compte - data["ca_total"]
    if abs(ecart) < 1:
        ecart_txt = "OK — Aucun écart"
        ecart_color = SUCCESS
    elif ecart < 0:
        ecart_txt = f"MANQUE {abs(ecart):,.0f} {devise}".replace(",", " ")
        ecart_color = DANGER
    else:
        ecart_txt = f"EXCÉDENT {ecart:,.0f} {devise}".replace(",", " ")
        ecart_color = WARNING

    ctrl_data = [
        ["Poste", "Montant"],
        ["CA système",
         f"{data['ca_total']:,.0f} {devise}".replace(",", " ")],
        ["Montant compté",
         f"{montant_compte:,.0f} {devise}".replace(",", " ")],
    ]
    story.append(table(ctrl_data, col_widths=[9 * cm, 6 * cm]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"<b>ÉCART : {ecart_txt}</b>",
        ParagraphStyle("ecart", parent=styles["Normal"],
                       fontSize=13, fontName="Helvetica-Bold",
                       textColor=ecart_color, alignment=TA_CENTER)))
    story.append(Spacer(1, 12))

    # ─── Top 5 produits ───
    if data["top_produits"]:
        story.append(H2("Top 5 produits"))
        prod_data = [["#", "Produit", "Qté", "CA"]]
        for i, p in enumerate(data["top_produits"][:5], 1):
            prod_data.append([
                str(i),
                p["nom"][:40],
                str(p["qte"]),
                f"{p['ca']:,.0f} {devise}".replace(",", " "),
            ])
        story.append(table(
            prod_data,
            col_widths=[1 * cm, 8 * cm, 2 * cm, 4 * cm]))
        story.append(Spacer(1, 12))

    # ─── Détail par heure ───
    if data["detail_heure"]:
        story.append(H2("Répartition horaire"))
        h_data = [["Heure", "Nb ventes"]]
        for h in data["detail_heure"]:
            h_data.append([f"{h['heure']:02d}h", str(h["n_ventes"])])
        story.append(table(h_data, col_widths=[3 * cm, 3 * cm]))

    # ─── Pied ───
    story.append(Spacer(1, 24))
    story.append(P(
        f"Document généré le "
        f"{datetime.now().strftime('%d/%m/%Y à %H:%M')}",
        size=8, color=GREY))
    story.append(Spacer(1, 4))
    story.append(P("Signature : _________________", size=9))

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=f"Rapport Z {numero_z}")
    doc.build(story)

    return output_path


# ══════════════════════════════════════════════════════════════════
# API unifiée
# ══════════════════════════════════════════════════════════════════
def generate_pdf(data: dict, montant_compte: float,
                 numero_z: str, output_path: str,
                 format_pdf: str = "ticket") -> str:
    """Route vers le bon template PDF."""
    if format_pdf == "a4":
        return generate_pdf_a4(data, montant_compte, numero_z, output_path)
    return generate_pdf_ticket(data, montant_compte, numero_z, output_path)


def list_caisses_disponibles() -> list:
    """Retourne la liste des caisses distinctes (table Caisse + Historique)."""
    caisses = set()
    try:
        for r in db.query("SELECT code FROM Caisse WHERE active = 1"):
            caisses.add(r["code"])
    except Exception:
        pass
    try:
        for r in db.query(
            "SELECT DISTINCT Caisse FROM Historique "
            "WHERE Caisse IS NOT NULL AND Caisse != ''"):
            caisses.add(r["Caisse"])
    except Exception:
        pass
    return sorted(caisses) or ["A"]