#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/monitoring.py — Whitelist PC monitoring (lecture seule).
================================================================
Gestion des machines autorisées à se connecter en ADMIN/OWNER/DEV.

⚠️ La whitelist est gérée UNIQUEMENT par NovaPharma Dev (outil externe).
L'application ne peut QUE consulter la liste (GET).
Aucune route POST/DELETE n'est exposée pour empêcher une auto-promotion.
"""

import logging

from fastapi import APIRouter, Request, HTTPException
from Database import db

from Server.server_models import (
    MachineResponse, MachinesListResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])

MAX_MACHINES = 3


# ══════════════════════════════════════════════════════════════════
def _row_to_dict(row) -> dict:
    return {k: row[k] for k in row.keys()}


def _require_owner_or_dev(request: Request):
    """Vérifie que l'utilisateur est OWNER ou DEVELOPER."""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401, "Non authentifié")
    if not (user.get("own") or user.get("dev")):
        raise HTTPException(
            403, "Réservé au propriétaire ou au développeur")


# ══════════════════════════════════════════════════════════════════
# GET — Liste des machines whitelistées (LECTURE SEULE)
# ══════════════════════════════════════════════════════════════════
@router.get("/machines", response_model=MachinesListResponse)
def list_machines(request: Request):
    """Liste toutes les machines whitelistées (actives + inactives)."""
    _require_owner_or_dev(request)

    try:
        rows = db.query(
            """SELECT * FROM MonitoringMachine
               ORDER BY actif DESC, ajoute_le DESC""")
        items = [_row_to_dict(r) for r in rows]

        return {
            "total": len(items),
            "max_allowed": MAX_MACHINES,
            "items": items,
        }
    except Exception as e:
        logger.exception("Erreur list_machines")
        raise HTTPException(500, f"Erreur : {e}")