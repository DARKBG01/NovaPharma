#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/audit.py — Journal d'audit.
====================================
Réservé OWNER / DEVELOPER.
"""

import logging

from fastapi import APIRouter, Request, HTTPException, Query
from Database import db

from Server.server_models import AuditListResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/audit", tags=["audit"])


def _require_owner_or_dev(request: Request):
    user = request.state.user
    if not (user.get("own") or user.get("dev")):
        raise HTTPException(403, "Réservé au propriétaire ou développeur")


def _row_to_dict(row) -> dict:
    return {k: row[k] for k in row.keys()}


# ══════════════════════════════════════════════════════════════════
@router.get("", response_model=AuditListResponse)
def list_audit(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    action: str = Query(""),
    utilisateur_id: str = Query(""),
    date_debut: str = Query(""),
    date_fin: str = Query(""),
):
    """Liste paginée du journal d'audit."""
    _require_owner_or_dev(request)

    try:
        where, params = ["1=1"], []
        if action:
            where.append("action = ?")
            params.append(action)
        if utilisateur_id:
            where.append("utilisateur_id = ?")
            params.append(utilisateur_id)
        if date_debut:
            where.append("date_action >= ?")
            params.append(f"{date_debut} 00:00:00")
        if date_fin:
            where.append("date_action <= ?")
            params.append(f"{date_fin} 23:59:59")

        wc = " AND ".join(where)
        row = db.query_one(
            f"SELECT COUNT(*) AS n FROM AuditLog WHERE {wc}",
            tuple(params))
        total = int(row["n"] or 0) if row else 0
        pages = max(1, (total + per_page - 1) // per_page)

        offset = (page - 1) * per_page
        rows = db.query(
            f"""SELECT * FROM AuditLog
                WHERE {wc}
                ORDER BY date_action DESC
                LIMIT ? OFFSET ?""",
            tuple(params + [per_page, offset]))

        return {
            "total": total, "page": page,
            "per_page": per_page, "pages": pages,
            "items": [_row_to_dict(r) for r in rows],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur list_audit")
        raise HTTPException(500, f"Erreur : {e}")


# ══════════════════════════════════════════════════════════════════
@router.get("/{entry_id}")
def get_audit(entry_id: str, request: Request):
    """Détail d'une entrée d'audit."""
    _require_owner_or_dev(request)

    row = db.query_one(
        "SELECT * FROM AuditLog WHERE id = ? LIMIT 1", (entry_id,))
    if not row:
        raise HTTPException(404, "Entrée introuvable")
    return _row_to_dict(row)


# ══════════════════════════════════════════════════════════════════
@router.get("/actions/liste")
def list_actions(request: Request):
    """Liste des actions connues (pour filtres UI)."""
    _require_owner_or_dev(request)

    try:
        rows = db.query(
            "SELECT DISTINCT action FROM AuditLog ORDER BY action ASC")
        return {"actions": [r["action"] for r in rows]}
    except Exception:
        return {"actions": []}