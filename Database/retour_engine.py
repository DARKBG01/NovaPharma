#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
retour_engine.py — Moteur des retours/remboursements.
======================================================
Calcule, enregistre et génère le PDF d'un avoir.
"""

import json
import logging
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from Database import db, audit

logger = logging.getLogger(__name__)

PRIMARY = colors.HexColor("#023E8A")
DANGER  = colors.HexColor("#DC2626")
SUCCESS = colors.HexColor("#16A34A")
GREY    = colors.HexColor("#64748B")
BORDER  = colors.HexColor("#E2E8F0")


# ══════════════════════════════════════════════════════════════════
# Calcul
# ══════════════════════════════════════════════════════════════════
def get_lignes_facture(num_fact: str) -> list:
    """Retourne les lignes de la facture d'origine."""
    rows = db.query(
        """SELECT Id, Article, Code_reference, Quantite, Prix_uni,
                  Total, Client_name, Caisse, Date_vent
           FROM Historique
           WHERE Num_fact = ?
           ORDER BY Id ASC""",
        (num_fact,))
    return [dict(r) for r in rows]


def get_quantite_deja_retournee(num_fact: str, code_ref: str) -> int:
    """Somme des quantités déjà retournées pour un article."""
    row = db.query_one(
        """SELECT COALESCE(SUM(lr.quantite), 0) AS n
           FROM LigneRetour lr
           JOIN RetourVente rv ON rv.id = lr.retour_id
           WHERE rv.num_fact_origine = ?
             AND lr.code_reference = ?
             AND rv.statut = 'VALIDE'""",
        (num_fact, code_ref))
    return int(row["n"] or 0) if row else 0


def compute_totaux_retour(lignes_retour: list) -> dict:
    """Calcule le total du retour."""
    total = sum(l["quantite"] * l["prix_unitaire"]
                for l in lignes_retour)
    nb_art = sum(l["quantite"] for l in lignes_retour)
    return {
        "montant_total": total,
        "nb_articles": nb_art,
        "nb_lignes": len(lignes_retour),
    }


# ══════════════════════════════════════════════════════════════════
# Numérotation
# ══════════════════════════════════════════════════════════════════
def next_numero_retour() -> str:
    """Génère RET-YYYY-NNNNNN."""
    year = datetime.now().strftime("%Y")
    prefix = f"RET-{year}-"
    try:
        row = db.query_one(
            "SELECT numero_retour FROM RetourVente "
            "WHERE numero_retour LIKE ? "
            "ORDER BY numero_retour DESC LIMIT 1",
            (f"{prefix}%",))
        if row and row["numero_retour"]:
            n = int(row["numero_retour"].split("-")[-1]) + 1
        else:
            n = 1
    except Exception:
        n = 1
    return f"{prefix}{n:06d}"


# ══════════════════════════════════════════════════════════════════
# Persistance
# ══════════════════════════════════════════════════════════════════
def save_retour(data: dict,
                user_id: str,
                user_name: str) -> str:
    """
    Enregistre le retour + ajuste le stock + met à jour le client.
    Retourne l'ID du retour.
    """
    numero_retour = next_numero_retour()
    rid = db.new_id()

    with db.transaction():
        # 1. INSERT RetourVente
        db.execute("""
            INSERT INTO RetourVente (
                id, numero_retour, num_fact_origine,
                utilisateur_id, utilisateur_name,
                client_name, client_numero,
                motif, montant_total, statut, notes
            ) VALUES (?,?,?,?,?,?,?,?,?,'VALIDE',?)
        """, (
            rid, numero_retour, data["num_fact_origine"],
            user_id, user_name,
            data.get("client_name"), data.get("client_numero"),
            data["motif"], data["montant_total"], data.get("notes")))

        # 2. INSERT lignes + ajustement stock
        for l in data["lignes"]:
            db.execute("""
                INSERT INTO LigneRetour (
                    id, retour_id, code_reference, article,
                    quantite, prix_unitaire, total, reconditionne
                ) VALUES (?,?,?,?,?,?,?,?)
            """, (
                db.new_id(), rid, l["code_reference"], l["article"],
                l["quantite"], l["prix_unitaire"], l["total"],
                1 if l.get("reconditionne", True) else 0))

            # Réintégration stock si reconditionné
            if l.get("reconditionne", True) and l.get("code_reference"):
                _restore_stock(
                    l["code_reference"], l["article"],
                    l["quantite"], numero_retour, user_id)

        # 3. Décrémente le montant total du client
        if data.get("client_numero"):
            _decrement_client_montant(
                data["client_numero"], data["montant_total"])

    # 4. Audit
    try:
        audit.log(
            "RETOUR_VENTE",
            utilisateur_id=user_id,
            utilisateur_name=user_name,
            cible_type="retour",
            cible_id=rid,
            cible_nom=numero_retour,
            details={
                "num_fact_origine": data["num_fact_origine"],
                "montant_total": data["montant_total"],
                "nb_articles": data["nb_articles"],
                "motif": data["motif"],
                "lignes": [
                    {"article": l["article"],
                     "qte": l["quantite"],
                     "reconditionne": l.get("reconditionne", True)}
                    for l in data["lignes"]
                ],
            },
            severite="warning")
    except Exception:
        logger.exception("Erreur audit retour")

    return rid


def _restore_stock(code_ref: str, article: str, qte: int,
                   numero_retour: str, user_id: str) -> None:
    """Réintègre le stock et trace le mouvement."""
    try:
        row = db.query_one(
            "SELECT Quantite FROM produits "
            "WHERE Code_reference = ? LIMIT 1", (code_ref,))
        if not row:
            return
        avant = int(row["Quantite"] or 0)
        apres = avant + int(qte)

        db.execute(
            "UPDATE produits SET Quantite = ? "
            "WHERE Code_reference = ?", (apres, code_ref))

        db.execute("""
            INSERT INTO MouvementStock
            (id, produit_id, type, quantite,
             stock_avant, stock_apres, motif, utilisateur_id)
            VALUES (?,?,?,?,?,?,?,?)
        """, (db.new_id(), code_ref, "ENTREE", int(qte),
              avant, apres, f"Retour {numero_retour}", user_id))
    except Exception:
        logger.exception("Erreur restore stock retour")


def _decrement_client_montant(numero: str, montant: float) -> None:
    """Décrémente le montant total du client."""
    try:
        row = db.query_one(
            "SELECT Montant_total FROM Client "
            "WHERE numero = ? LIMIT 1", (numero,))
        if not row:
            return
        nouveau = max(0.0, float(row["Montant_total"] or 0) - float(montant))
        db.execute(
            "UPDATE Client SET Montant_total = ? WHERE numero = ?",
            (nouveau, numero))
    except Exception:
        logger.exception("Erreur decrement client montant")


# ══════════════════════════════════════════════════════════════════
# Lecture
# ══════════════════════════════════════════════════════════════════
def list_retours(page: int = 1, per_page: int = 30,
                 search: str = "", statut: str = "") -> dict:
    """Liste paginée des retours."""
    where, params = ["1=1"], []
    if search:
        where.append("(numero_retour LIKE ? OR num_fact_origine LIKE ? "
                     "OR client_name LIKE ? OR motif LIKE ?)")
        like = f"%{search}%"
        params.extend([like, like, like, like])
    if statut:
        where.append("statut = ?")
        params.append(statut)

    wc = " AND ".join(where)
    row = db.query_one(
        f"SELECT COUNT(*) AS n FROM RetourVente WHERE {wc}",
        tuple(params))
    total = int(row["n"] or 0) if row else 0
    pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, pages))
    offset = (page - 1) * per_page

    rows = db.query(
        f"""SELECT * FROM RetourVente
            WHERE {wc}
            ORDER BY date_retour DESC
            LIMIT ? OFFSET ?""",
        tuple(params + [per_page, offset]))

    return {
        "total": total, "page": page,
        "per_page": per_page, "pages": pages,
        "items": [dict(r) for r in rows],
    }


def get_retour(retour_id: str) -> dict:
    """Détail d'un retour + ses lignes."""
    rv = db.query_one(
        "SELECT * FROM RetourVente WHERE id = ? LIMIT 1", (retour_id,))
    if not rv:
        return None
    lignes = db.query(
        "SELECT * FROM LigneRetour WHERE retour_id = ? "
        "ORDER BY rowid ASC", (retour_id,))
    d = dict(rv)
    d["lignes"] = [dict(l) for l in lignes]
    return d


# ══════════════════════════════════════════════════════════════════
# PDF — Avoir
# ══════════════════════════════════════════════════════════════════
def generate_pdf_avoir(data: dict, output_path: str) -> str:
    """Génère le PDF de l'avoir (document de remboursement)."""
    styles = getSampleStyleSheet()

    def P(t, size=10, center=False, color=colors.black, bold=False):
        return Paragraph(t, ParagraphStyle(
            f"p_{size}_{center}_{bold}",
            parent=styles["Normal"],
            fontSize=size, leading=size + 4,
            fontName="Helvetica-Bold" if bold else "Helvetica",
            textColor=color,
            alignment=TA_CENTER if center else TA_LEFT))

    def R(t, size=10, bold=False):
        return Paragraph(t, ParagraphStyle(
            f"r_{size}", parent=styles["Normal"],
            fontSize=size, leading=size + 4,
            fontName="Helvetica-Bold" if bold else "Helvetica",
            alignment=TA_RIGHT))

    story = []

    # Header
    story.append(P(data.get("nom_pharmacie", "NOVA PHARMA"),
                   size=18, center=True, color=PRIMARY, bold=True))
    story.append(Spacer(1, 4))
    if data.get("adresse_pharmacie"):
        story.append(P(data["adresse_pharmacie"],
                       size=9, center=True, color=GREY))
    if data.get("telephone_pharmacie"):
        story.append(P(f"Tel : {data['telephone_pharmacie']}",
                       size=9, center=True, color=GREY))

    story.append(Spacer(1, 12))

    # Titre
    story.append(P("AVOIR — REMBOURSEMENT",
                   size=22, center=True, color=DANGER, bold=True))
    story.append(Spacer(1, 12))

    # Infos avoir
    info_data = [
        ["Numéro avoir", data.get("numero_retour", "—")],
        ["Facture d'origine", data.get("num_fact_origine", "—")],
        ["Date retour", data.get("date_retour", "—")[:19]],
        ["Client", data.get("client_name") or "Client anonyme"],
        ["Motif", data.get("motif", "—")],
    ]
    t = Table(info_data, colWidths=[5 * cm, 11 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F8FAFC")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t)
    story.append(Spacer(1, 16))

    # Lignes
    ligne_data = [["Article", "Qté", "P.U.", "Total"]]
    for l in data.get("lignes", []):
        ligne_data.append([
            l["article"][:40],
            str(l["quantite"]),
            f"{l['prix_unitaire']:,.0f}",
            f"{l['total']:,.0f}",
        ])
    # Total
    ligne_data.append([
        "", "", "TOTAL",
        f"{data.get('montant_total', 0):,.0f} FC",
    ])

    t2 = Table(ligne_data, colWidths=[9 * cm, 2 * cm, 2.5 * cm, 2.5 * cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DANGER),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#FEF2F2")),
        ("TEXTCOLOR", (-1, -1), (-1, -1), DANGER),
    ]))
    story.append(t2)
    story.append(Spacer(1, 24))

    # Mention
    story.append(P(
        "Ce document atteste du remboursement des articles listés "
        "ci-dessus. Le stock a été restauré pour les articles "
        "reconditionnés.",
        size=9, center=True, color=GREY))

    story.append(Spacer(1, 40))
    story.append(P("Signature du caissier : ____________________",
                   size=9))
    story.append(Spacer(1, 20))
    story.append(P("Signature du client : ____________________",
                   size=9))

    story.append(Spacer(1, 30))
    story.append(P(
        f"Document généré le "
        f"{datetime.now().strftime('%d/%m/%Y à %H:%M')}",
        size=8, center=True, color=GREY))

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=f"Avoir {data.get('numero_retour', '')}")
    doc.build(story)
    return output_path