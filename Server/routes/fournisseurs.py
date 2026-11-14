#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/fournisseurs.py — CRUD fournisseurs (Phase 2).
======================================================
Réservé ADMIN / OWNER / DEVELOPER.
"""

import logging

from fastapi import APIRouter, Request, HTTPException, Query
from Database import db, audit

from Server.server_models import (
    FournisseurCreate, FournisseurUpdate,
    FournisseurResponse, FournisseurListResponse, SimpleResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/fournisseurs", tags=["fournisseurs"])


def _require_admin(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401, "Non authentifié")
    is_privileged = (user.get("own") or user.get("dev")
                     or user.get("role", "").upper() == "ADMIN")
    if not is_privileged:
        raise HTTPException(403, "Réservé aux administrateurs")


def _row_to_dict(row) -> dict:
    return {k: row[k] for k in row.keys()}


def _next_id() -> str:
    try:
        row = db.query_one(
            """SELECT Id_fournisseur FROM Fournisseur
               WHERE Id_fournisseur LIKE 'FOU-%'
               ORDER BY Id_fournisseur DESC LIMIT 1""")
        if row and row["Id_fournisseur"]:
            try:
                n = int(row["Id_fournisseur"].split("-")[1]) + 1
            except (ValueError, IndexError):
                n = 1
        else:
            n = 1
        return f"FOU-{n:04d}"
    except Exception:
        import time
        return f"FOU-{int(time.time()) % 10000:04d}"


# ══════════════════════════════════════════════════════════════════
@router.get("", response_model=FournisseurListResponse)
def list_fournisseurs(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    search: str = Query(""),
    actif: int = Query(-1),
):
    """Liste paginée des fournisseurs."""
    _require_admin(request)

    try:
        where, params = ["1=1"], []
        if search:
            where.append(
                "(Entreprise LIKE ? OR Responsable LIKE ? OR Email LIKE ?)")
            like = f"%{search}%"
            params.extend([like, like, like])
        if actif in (0, 1):
            where.append("actif = ?")
            params.append(actif)

        wc = " AND ".join(where)
        row = db.query_one(
            f"SELECT COUNT(*) AS n FROM Fournisseur WHERE {wc}",
            tuple(params))
        total = int(row["n"] or 0) if row else 0
        pages = max(1, (total + per_page - 1) // per_page)

        offset = (page - 1) * per_page
        rows = db.query(
            f"""SELECT * FROM Fournisseur WHERE {wc}
                ORDER BY Entreprise ASC LIMIT ? OFFSET ?""",
            tuple(params + [per_page, offset]))

        return {
            "total": total, "page": page,
            "per_page": per_page, "pages": pages,
            "items": [_row_to_dict(r) for r in rows],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur list_fournisseurs")
        raise HTTPException(500, f"Erreur : {e}")


@router.get("/{fournisseur_id}", response_model=FournisseurResponse)
def get_fournisseur(fournisseur_id: str, request: Request):
    _require_admin(request)
    row = db.query_one(
        "SELECT * FROM Fournisseur WHERE Id_fournisseur = ? LIMIT 1",
        (fournisseur_id,))
    if not row:
        raise HTTPException(404, "Fournisseur introuvable")
    return _row_to_dict(row)


@router.post("", response_model=FournisseurResponse, status_code=201)
def create_fournisseur(payload: FournisseurCreate, request: Request):
    _require_admin(request)
    user = request.state.user

    existing = db.query_one(
        "SELECT 1 FROM Fournisseur "
        "WHERE LOWER(Entreprise) = LOWER(?) LIMIT 1",
        (payload.Entreprise,))
    if existing:
        raise HTTPException(
            409, f"Fournisseur '{payload.Entreprise}' existe déjà")

    new_id = _next_id()

    try:
        with db.transaction():
            db.execute(
                """INSERT INTO Fournisseur
                   (Id_fournisseur, Entreprise, Categorie, Responsable,
                    Numero, Email, Adresse, actif, created_at)
                   VALUES (?,?,?,?,?,?,?,1, datetime('now'))""",
                (new_id, payload.Entreprise.upper(),
                 payload.Categorie, payload.Responsable,
                 payload.Numero, payload.Email, payload.Adresse))

            audit.log(
                "CREATION_FOURNISSEUR",
                utilisateur_id=user.get("uid"),
                utilisateur_name=user.get("ident"),
                cible_type="Fournisseur",
                cible_id=new_id,
                cible_nom=payload.Entreprise,
                details={"source": "api_client"})

        row = db.query_one(
            "SELECT * FROM Fournisseur WHERE Id_fournisseur = ? LIMIT 1",
            (new_id,))
        return _row_to_dict(row)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur create_fournisseur")
        raise HTTPException(500, f"Erreur : {e}")


@router.put("/{fournisseur_id}", response_model=FournisseurResponse)
def update_fournisseur(fournisseur_id: str,
                       payload: FournisseurUpdate, request: Request):
    _require_admin(request)
    user = request.state.user

    existing = db.query_one(
        "SELECT * FROM Fournisseur WHERE Id_fournisseur = ? LIMIT 1",
        (fournisseur_id,))
    if not existing:
        raise HTTPException(404, "Fournisseur introuvable")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(400, "Aucun champ à modifier")

    try:
        champs, params = [], []
        for k, v in updates.items():
            champs.append(f"{k} = ?")
            params.append(v)
        params.append(fournisseur_id)

        with db.transaction():
            db.execute(
                f"UPDATE Fournisseur SET {', '.join(champs)} "
                f"WHERE Id_fournisseur = ?",
                tuple(params))

            audit.log(
                "MODIF_FOURNISSEUR",
                utilisateur_id=user.get("uid"),
                utilisateur_name=user.get("ident"),
                cible_type="Fournisseur",
                cible_id=fournisseur_id,
                cible_nom=existing["Entreprise"],
                details={"champs_modifies": list(updates.keys())})

        row = db.query_one(
            "SELECT * FROM Fournisseur WHERE Id_fournisseur = ? LIMIT 1",
            (fournisseur_id,))
        return _row_to_dict(row)
    except Exception as e:
        logger.exception("Erreur update_fournisseur")
        raise HTTPException(500, f"Erreur : {e}")