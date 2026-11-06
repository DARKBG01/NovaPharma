#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""routes/sessions.py — Surveillance postes clients."""

import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from Database import db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sessions", tags=["sessions"])


class HeartbeatPayload(BaseModel):
    machine_id: str
    hostname: str = ""
    imprimante: str = ""
    version: str = ""


class BlockPayload(BaseModel):
    reason: str = "Bloqué par admin"


@router.post("/heartbeat")
def heartbeat(payload: HeartbeatPayload, request: Request):
    """Met à jour la session du poste client."""
    user = request.state.user
    if not user:
        raise HTTPException(401)

    try:
        # Vérifie si bloqué
        existing = db.query_one(
            "SELECT bloque, bloque_raison FROM ClientSession "
            "WHERE machine_id = ? LIMIT 1",
            (payload.machine_id,))

        # ─── Limite max_postes ───
        if not existing:
            row_count = db.query_one("""
                SELECT COUNT(*) AS n FROM ClientSession
                WHERE statut = 'CONNECTE'
                  AND derniere_vue >= datetime('now', '-2 minutes')
            """)
            nb_connectes = int(row_count["n"] or 0) if row_count else 0
            max_postes = int(db.get_config("max_postes", 100))

            if nb_connectes >= max_postes:
                logger.warning(
                    "Limite postes atteinte : %d / %d",
                    nb_connectes, max_postes)
                raise HTTPException(
                    429,
                    f"Limite de {max_postes} postes atteinte. "
                    f"Contactez l'administrateur.")

        if existing and int(existing["bloque"]) == 1:
            raise HTTPException(
                403,
                f"Ce poste est bloqué : {existing['bloque_raison'] or '—'}")

        ip = ""
        if request.client:
            ip = request.client.host or ""

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if existing:
            db.execute("""
                UPDATE ClientSession SET
                    hostname = ?, ip_address = ?, user_id = ?,
                    user_name = ?, role = ?, imprimante = ?,
                    version_app = ?, derniere_vue = ?,
                    statut = 'CONNECTE'
                WHERE machine_id = ?
            """, (payload.hostname, ip, user.get("uid"),
                  user.get("ident"), user.get("role"),
                  payload.imprimante, payload.version, now,
                  payload.machine_id))
        else:
            db.execute("""
                INSERT INTO ClientSession
                (id, machine_id, hostname, ip_address,
                 user_id, user_name, role, imprimante,
                 version_app, statut, derniere_vue)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'CONNECTE', ?)
            """, (db.new_id(), payload.machine_id,
                  payload.hostname, ip, user.get("uid"),
                  user.get("ident"), user.get("role"),
                  payload.imprimante, payload.version, now))

        return {"status": "ok"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur heartbeat")
        raise HTTPException(500, str(e))


@router.get("")
def list_sessions(request: Request):
    """Liste toutes les sessions (admin/owner/dev)."""
    user = request.state.user
    if not user:
        raise HTTPException(401)

    try:
        # Marque les sessions inactives (derniere_vue > 2 min)
        threshold = (datetime.now() - timedelta(minutes=2)
                     ).strftime("%Y-%m-%d %H:%M:%S")
        db.execute("""
            UPDATE ClientSession SET statut = 'DECONNECTE'
            WHERE derniere_vue < ? AND statut = 'CONNECTE'
              AND bloque = 0
        """, (threshold,))

        rows = db.query("""
            SELECT * FROM ClientSession
            ORDER BY bloque DESC, derniere_vue DESC
        """)

        return {
            "items": [dict(r) for r in rows],
            "total": len(rows),
        }
    except Exception as e:
        logger.exception("Erreur list_sessions")
        raise HTTPException(500, str(e))


@router.post("/{session_id}/block")
def block_session(session_id: str, payload: BlockPayload,
                  request: Request):
    """Bloque un poste."""
    try:
        db.execute("""
            UPDATE ClientSession SET
                bloque = 1, statut = 'BLOQUE',
                bloque_raison = ?
            WHERE id = ?
        """, (payload.reason, session_id))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/{session_id}/unblock")
def unblock_session(session_id: str, request: Request):
    """Débloque un poste."""
    try:
        db.execute("""
            UPDATE ClientSession SET
                bloque = 0, bloque_raison = NULL
            WHERE id = ?
        """, (session_id,))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.delete("/{session_id}")
def delete_session(session_id: str, request: Request):
    """Supprime la session (déconnexion forcée)."""
    try:
        db.execute(
            "DELETE FROM ClientSession WHERE id = ?",
            (session_id,))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(500, str(e))