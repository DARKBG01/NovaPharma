#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/health.py — Endpoint de santé (ping) + config publique.
==============================================================
Accessible SANS token ni horaires.
"""

import logging
import traceback
from datetime import datetime

from fastapi import APIRouter, Request, HTTPException
from Database import db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["santé"])


# ══════════════════════════════════════════════════════════════════
@router.get("/sante")
def sante():
    """Ping du serveur — vérifie qu'il est vivant."""
    now = datetime.now()

    info = {
        "status": "ok",
        "version": "0.1.0",
        "timestamp": now.isoformat(),
        "serveur_actif": True,
        "utilisateurs_actifs": 0,           # ← valeur par défaut
        "server_time": now.isoformat(),     # ← AJOUT (point 18)
        "server_time_fr": now.strftime("%H:%M:%S"),  # ← AJOUT
    }

    # Info DB
    try:
        row = db.query_one(
            "SELECT COUNT(*) AS n FROM Utilisateur WHERE actif = 1")
        info["utilisateurs_actifs"] = int(row["n"] or 0) if row else 0
    except Exception as e:
        logger.error("Erreur requête Utilisateur : %s", e)
        logger.error(traceback.format_exc())
        info["utilisateurs_actifs"] = None
        info["db_error"] = str(e)
        info["db_path"] = str(db.DB_PATH)
        info["db_exists"] = db.DB_PATH.exists()

    return info


# ══════════════════════════════════════════════════════════════════
@router.get("/config/public")
def get_public_config(request: Request):
    """Retourne les paramètres publics (devise, mentions, pharmacie...)."""
    try:
        ph = db.query_one(
            "SELECT nom, adresse, numero FROM Pharmacie "
            "WHERE id = 1 AND actif = 1 LIMIT 1")

        return {
            "devise": db.get_config("devise", "FC"),
            "nom_entreprise": (ph["nom"] if ph else None) or "NOVA PHARMA",
            "adresse_entreprise": (ph["adresse"] if ph else "") or "",
            "telephone_entreprise": (ph["numero"] if ph else "") or "",
            "mentions_ticket": db.get_config("mentions_ticket", []) or [],
            "qrcode_actif": bool(db.get_config("qrcode_actif", True)),
            "impression_facture_auto": bool(db.get_config(
                "impression_facture_auto", True)),
            "printer_auto_print": bool(db.get_config(
                "printer_auto_print", False)),
            "printer_auto_open": bool(db.get_config(
                "printer_auto_open", True)),
            "seuil_stock": int(db.get_config("seuil_stock", 20)),
            "marge_benefice": float(db.get_config("marge_benefice", 30)),
            "taux_change": float(db.get_config("taux_change", 2800)),
        }
    except Exception as e:
        raise HTTPException(500, str(e))