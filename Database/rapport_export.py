#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rapport_export.py — Générateur PDF professionnel pour rapports.
"""

import logging
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

logger = logging.getLogger(__name__)

# Palette
PRIMARY  = colors.HexColor("#023E8A")
BLUE     = colors.HexColor("#0077B6")
CYAN     = colors.HexColor("#00B4D8")
DANGER   = colors.HexColor("#DC2626")
SUCCESS  = colors.HexColor("#16A34A")
WARNING  = colors.HexColor("#F4A261")
GREY     = colors.HexColor("#64748B")
LIGHT    = colors.HexColor("#F8FAFC")
BORDER   = colors.HexColor("#E2E8F0")


def _styles():
    base = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"],
            fontSize=20, leading=26, textColor=PRIMARY,
            fontName="Helvetica-Bold", spaceAfter=14),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"],
            fontSize=13, leading=18, textColor=BLUE,
            fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=8),
        "body": ParagraphStyle(
            "body", parent=base["BodyText"],
            fontSize=10, leading=14, textColor=colors.black),
        "kpi_label": ParagraphStyle(
            "kl", parent=base["Normal"],
            fontSize=9, textColor=GREY, alignment=TA_CENTER),
        "kpi_value": ParagraphStyle(
            "kv", parent=base["Normal"],
            fontSize=14, fontName="Helvetica-Bold",
            textColor=PRIMARY, alignment=TA_CENTER),
    }


def _table(data, col_widths=None, header_bg=PRIMARY):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
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


def export_pdf(path: str, titre: str, sous_titre: str,
               sections: list, nom_entreprise: str = "NOVA PHARMA") -> bool:
    """Génère un PDF professionnel."""
    try:
        styles = _styles()
        doc = SimpleDocTemplate(
            path, pagesize=A4,
            leftMargin=2 * cm, rightMargin=2 * cm,
            topMargin=2 * cm, bottomMargin=2 * cm,
            title=titre, author=nom_entreprise)

        elements = []

        # ─── Couverture ───
        elements.append(Paragraph(nom_entreprise, styles["h1"]))
        elements.append(Paragraph(titre, ParagraphStyle(
            "t", parent=styles["h2"],
            fontSize=16, textColor=colors.black)))
        elements.append(Paragraph(sous_titre, ParagraphStyle(
            "s", parent=styles["body"],
            textColor=GREY, fontSize=11)))
        elements.append(Spacer(1, 14))

        # ─── Sections ───
        for section in sections:
            elements.append(Paragraph(section["titre"], styles["h2"]))

            if section.get("type") == "kpis":
                data = []
                for label, value in section["data"]:
                    data.append([
                        Paragraph(label, styles["kpi_label"]),
                        Paragraph(str(value), styles["kpi_value"]),
                    ])
                t = Table(data, colWidths=[7 * cm, 8 * cm])
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                    ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                ]))
                elements.append(t)

            elif section.get("type") == "table":
                data = [section["headers"]] + section["rows"]
                elements.append(_table(
                    data,
                    col_widths=section.get("col_widths")))

            elements.append(Spacer(1, 14))

        # ─── Pied ───
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(
            f"Document généré le "
            f"{datetime.now().strftime('%d/%m/%Y à %H:%M')}",
            ParagraphStyle("f", parent=styles["body"],
                           fontSize=8, textColor=GREY,
                           alignment=TA_CENTER)))

        doc.build(elements)
        logger.info("PDF rapport généré : %s", path)
        return True

    except Exception:
        logger.exception("Erreur export PDF")
        return False

# ══════════════════════════════════════════════════════════════════
# Export CSV
# ══════════════════════════════════════════════════════════════════
def export_csv(path: str, headers: list, rows: list[list]) -> bool:
    """
    Exporte une liste de lignes vers un fichier CSV (UTF-8 BOM pour Excel).

    Args:
        path    : chemin de destination
        headers : liste des titres de colonnes
        rows    : liste de listes (une par ligne de données)

    Retourne True si succès, False sinon.
    """
    import csv
    try:
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(headers)
            w.writerows(rows)
        logger.info("CSV exporté : %s (%d lignes)", path, len(rows))
        return True
    except Exception:
        logger.exception("Erreur export CSV : %s", path)
        return False


# ══════════════════════════════════════════════════════════════════
# Export Excel
# ══════════════════════════════════════════════════════════════════
def export_excel(path: str, sheets: dict) -> bool:
    """
    Exporte plusieurs feuilles vers un classeur Excel.

    Args:
        path   : chemin de destination (.xlsx)
        sheets : dict {nom_feuille: {"headers": [...], "rows": [[...], ...]}}

    Retourne True si succès, False sinon.
    """
    try:
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment
        except ImportError:
            logger.error(
                "openpyxl non installé — pip install openpyxl")
            return False

        wb = Workbook()
        # Supprime la feuille par défaut
        wb.remove(wb.active)

        for sheet_name, data in sheets.items():
            # Excel limite le nom à 31 caractères
            safe_name = str(sheet_name)[:31] or "Sheet"
            ws = wb.create_sheet(safe_name)

            headers = data.get("headers", [])
            rows = data.get("rows", [])

            # ─── En-têtes stylés ───
            ws.append(headers)
            for cell in ws[1]:
                cell.font = Font(bold=True, color="FFFFFF", size=11)
                cell.fill = PatternFill(
                    "solid", fgColor="023E8A")  # bleu primaire
                cell.alignment = Alignment(
                    horizontal="center", vertical="center")

            # ─── Données ───
            for row in rows:
                ws.append(row)

            # ─── Ajustement auto des colonnes ───
            for col in ws.columns:
                max_len = 10
                for cell in col:
                    v = cell.value
                    if v is not None:
                        max_len = max(max_len, len(str(v)))
                col_letter = col[0].column_letter
                ws.column_dimensions[col_letter].width = min(
                    max_len + 2, 40)

            # ─── Figer la ligne d'en-tête ───
            ws.freeze_panes = "A2"

        wb.save(path)
        logger.info(
            "Excel exporté : %s (%d feuille(s))", path, len(sheets))
        return True

    except Exception:
        logger.exception("Erreur export Excel : %s", path)
        return False