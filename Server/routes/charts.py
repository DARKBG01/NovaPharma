#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/charts.py — Données des graphiques dashboard (Phase 2+).
================================================================
Retourne en 1 appel toutes les données nécessaires aux 4 cartes
du tableau de bord (mode client).
"""

import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Request, HTTPException
from Database import db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/charts", tags=["charts"])

MOIS_FR = {
    1: "Jan", 2: "Fév", 3: "Mar", 4: "Avr", 5: "Mai", 6: "Juin",
    7: "Juil", 8: "Août", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Déc",
}


def _iso_expr(col: str) -> str:
    return (
        f"(substr({col}, 7, 4) || '-' || "
        f"substr({col}, 4, 2) || '-' || "
        f"substr({col}, 1, 2) || substr({col}, 11))"
    )


@router.get("/dashboard")
def get_dashboard_charts(request: Request):
    """Retourne toutes les données des 4 graphiques dashboard."""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401, "Non authentifié")

    try:
        date_iso = _iso_expr("Date_vent")

        # ═══ 1. Revenus 7 derniers jours ═══
        today = datetime.now().date()
        start7 = today - timedelta(days=6)

        rows = db.query(
            f"""SELECT substr(Date_vent, 1, 10) AS jour,
                       SUM(Total) AS ca
                FROM Historique
                WHERE annule = 0
                  AND {date_iso} >= ?
                  AND {date_iso} <= ?
                GROUP BY jour""",
            (start7.strftime("%Y-%m-%d") + " 00:00:00",
             today.strftime("%Y-%m-%d") + " 23:59:59"))

        daily = {r["jour"]: float(r["ca"] or 0) for r in rows}

        labels7, ca7 = [], []
        for i in range(7):
            d = start7 + timedelta(days=i)
            key = d.strftime("%d/%m/%Y")
            labels7.append(d.strftime("%d/%m"))
            ca7.append(daily.get(key, 0.0))

        # ═══ 2. CA mensuel (12 derniers mois) ═══
        now = datetime.now()
        start12 = (now.replace(day=1) - timedelta(days=30 * 11)).replace(day=1)

        rows = db.query(
            f"""SELECT substr(Date_vent, 4, 7) AS mois,
                       SUM(Total) AS ca
                FROM Historique
                WHERE annule = 0
                  AND {date_iso} >= ?
                GROUP BY mois""",
            (start12.strftime("%Y-%m-%d") + " 00:00:00",))

        monthly = {}
        for r in rows:
            try:
                mm, yyyy = (r["mois"] or "").split("/")
                monthly[f"{yyyy}-{mm}"] = float(r["ca"] or 0)
            except Exception:
                pass

        labels12, ca12 = [], []
        cur = start12
        for _ in range(12):
            key = f"{cur.year}-{cur.month:02d}"
            labels12.append(f"{MOIS_FR[cur.month]} {cur.year % 100:02d}")
            ca12.append(monthly.get(key, 0.0))
            if cur.month == 12:
                cur = cur.replace(year=cur.year + 1, month=1)
            else:
                cur = cur.replace(month=cur.month + 1)

        # ═══ 3. Top 10 médicaments ═══
        rows = db.query(
            """SELECT Article AS nom,
                      SUM(Quantite) AS qte,
                      SUM(Total) AS ca
               FROM Historique
               WHERE annule = 0
               GROUP BY Article
               ORDER BY qte DESC
               LIMIT 10""")
        top = [
            {"nom": r["nom"] or "—",
             "qte": int(r["qte"] or 0),
             "ca": float(r["ca"] or 0)}
            for r in rows
        ]

        # ═══ 4. Répartition par catégorie ═══
        rows = db.query(
            """SELECT COALESCE(p.Categorie, 'Non classé') AS cat,
                      SUM(h.Total) AS ca
               FROM Historique h
               LEFT JOIN produits p ON p.Code_reference = h.Code_reference
               WHERE COALESCE(h.annule, 0) = 0
               GROUP BY cat
               ORDER BY ca DESC""")
        categories = [
            {"cat": r["cat"], "ca": float(r["ca"] or 0)}
            for r in rows
        ]

        return {
            "revenue_7days": {"labels": labels7, "ca": ca7},
            "revenue_12months": {"labels": labels12, "ca": ca12},
            "top_products": top,
            "categories": categories,
        }

    except Exception as e:
        logger.exception("Erreur dashboard charts")
        raise HTTPException(500, f"Erreur : {e}")