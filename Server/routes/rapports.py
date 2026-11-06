#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/rapports.py — 3 rapports agrégés + Rapport Z.
=====================================================
Réutilise Database/rapport_engine et Database/rapport_z.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Request, HTTPException, Query
from pydantic import BaseModel

from Database import rapport_engine as engine, rapport_z

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════
# UN SEUL router pour toutes les routes /api/rapports/*
# ══════════════════════════════════════════════════════════════════
router = APIRouter(prefix="/api/rapports", tags=["rapports"])


# ══════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════
def _resolve(periode: str, date_debut: str, date_fin: str):
    """Résout les bornes de période."""
    cs = None
    ce = None
    if periode == "Personnalisé" and date_debut and date_fin:
        try:
            cs = datetime.fromisoformat(date_debut)
            ce = datetime.fromisoformat(date_fin)
        except Exception:
            raise HTTPException(400, "Dates invalides (YYYY-MM-DD)")
    return engine.resolve_period(periode, cs, ce)


# ══════════════════════════════════════════════════════════════════
# 1. Rapport Ventes
# ══════════════════════════════════════════════════════════════════
@router.get("/ventes")
def rapport_ventes(
    request: Request,
    periode: str = Query("Ce mois"),
    date_debut: str = Query(""),
    date_fin: str = Query(""),
    topn: int = Query(10, ge=1, le=100),
):
    """Rapport Ventes : KPIs + top produits + catégories + N-1."""
    try:
        d, f, dn1, fn1 = _resolve(periode, date_debut, date_fin)
        kpi = engine.compute_kpis(d, f)
        kpi_n1 = engine.compute_kpis(dn1, fn1)
        var = engine.compare_n1(kpi, kpi_n1)

        return {
            "periode": {"debut": d, "fin": f,
                        "debut_n1": dn1, "fin_n1": fn1},
            "kpi": kpi,
            "kpi_n1": kpi_n1,
            "variation": var,
            "serie_ca": engine.serie_ca_journalier(d, f),
            "top_produits": engine.top_produits(d, f, topn),
            "categories": engine.repartition_categories(d, f),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur rapport_ventes")
        raise HTTPException(500, f"Erreur : {e}")


# ══════════════════════════════════════════════════════════════════
# 2. Rapport Équipe
# ══════════════════════════════════════════════════════════════════
@router.get("/equipe")
def rapport_equipe(
    request: Request,
    periode: str = Query("Ce mois"),
    date_debut: str = Query(""),
    date_fin: str = Query(""),
):
    """Rapport Équipe : vendeurs + annulations."""
    try:
        d, f, _, _ = _resolve(periode, date_debut, date_fin)
        return {
            "periode": {"debut": d, "fin": f},
            "vendeurs": engine.equipe_vendeurs(d, f),
            "annulations": engine.equipe_annulations(d, f),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur rapport_equipe")
        raise HTTPException(500, f"Erreur : {e}")


# ══════════════════════════════════════════════════════════════════
# 3. Rapport Opérations
# ══════════════════════════════════════════════════════════════════
@router.get("/operations")
def rapport_operations(
    request: Request,
    periode: str = Query("Ce mois"),
    date_debut: str = Query(""),
    date_fin: str = Query(""),
):
    """Rapport Opérations : marges + stock + clients + résumé."""
    try:
        d, f, _, _ = _resolve(periode, date_debut, date_fin)
        return {
            "periode": {"debut": d, "fin": f},
            "marges": engine.marges(d, f),
            "stock": engine.stock_et_blf(d, f),
            "clients": engine.clients_stats(d, f),
            "operations": engine.operations_resume(d, f),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur rapport_operations")
        raise HTTPException(500, f"Erreur : {e}")


# ══════════════════════════════════════════════════════════════════
# 4. Rapport Z (clôture de caisse)
# ══════════════════════════════════════════════════════════════════
class RapportZRequest(BaseModel):
    caisse: str
    periode: str = "Aujourd'hui"
    date_debut: str = ""   # ISO si personnalisé
    date_fin: str = ""
    montant_compte: float = 0
    format_pdf: str = "ticket"

# ══════════════════════════════════════════════════════════════════
# GET — Preview Rapport Z (calcul sans génération)
# ══════════════════════════════════════════════════════════════════
@router.get("/z/preview")
def preview_rapport_z(
    request: Request,
    caisse: str = Query("A"),
    periode: str = Query("Aujourd'hui"),
    date_debut: str = Query(""),
    date_fin: str = Query(""),
):
    """Calcule un Rapport Z sans générer le PDF (pour prévisualisation)."""
    user = request.state.user
    if not user:
        raise HTTPException(401, "Non authentifié")

    try:
        # Normalise "*" / "TOUTES"
        if caisse in ("TOUTES", "Toutes", "toutes", "*"):
            caisse_norm = "*"
        else:
            caisse_norm = caisse

        d_debut = None
        d_fin = None
        if date_debut:
            d_debut = datetime.fromisoformat(date_debut)
        if date_fin:
            d_fin = datetime.fromisoformat(date_fin)

        debut, fin = rapport_z.resolve_period(
            periode, date_debut=d_debut, date_fin=d_fin,
            caisse=caisse_norm)

        data = rapport_z.compute_rapport_z(caisse_norm, debut, fin)
        return data

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur preview rapport Z")
        raise HTTPException(500, str(e))


@router.post("/z")
async def create_rapport_z(payload: RapportZRequest, request: Request):
    user = request.state.user
    if not user:
        raise HTTPException(401, "Non authentifié")

    try:
        # ═══ NOUVEAU : normalise "*" / "TOUTES" ═══
        caisse = payload.caisse
        if caisse in ("TOUTES", "Toutes", "toutes", "*"):
            caisse = "*"

        # Résolution de la période
        d_debut = None
        d_fin = None
        if payload.date_debut:
            d_debut = datetime.fromisoformat(payload.date_debut)
        if payload.date_fin:
            d_fin = datetime.fromisoformat(payload.date_fin)

        debut, fin = rapport_z.resolve_period(
            payload.periode,
            date_debut=d_debut,
            date_fin=d_fin,
            caisse=caisse)              # ← utilise caisse normalisée

        data = rapport_z.compute_rapport_z(caisse, debut, fin)

        # numéro + PDF
        numero_caisse = caisse if caisse != "*" else "TOUTES"
        numero_z = rapport_z.next_numero_z(numero_caisse)
        chemin = f"Rapports/RapportZ/{numero_z}.pdf"
        rapport_z.generate_pdf(
            data, payload.montant_compte, numero_z,
            chemin, format_pdf=payload.format_pdf)

        rid = rapport_z.save_rapport_z(
            data,
            user_id=user.get("uid"),
            user_name=user.get("ident"),
            montant_compte=payload.montant_compte,
            format_pdf=payload.format_pdf,
            chemin_pdf=chemin)

        return {
            "id": rid,
            "numero_z": numero_z,
            "chemin_pdf": chemin,
            "ca_total": data["ca_total"],
            "ecart": payload.montant_compte - data["ca_total"],
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur création Rapport Z")
        raise HTTPException(500, str(e))