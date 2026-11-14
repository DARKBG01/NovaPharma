#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/categories.py — CRUD catégories produits (Phase 2).
==========================================================
Lecture : tout le monde. Écriture : ADMIN / OWNER / DEVELOPER.
"""

import logging

from fastapi import APIRouter, Request, HTTPException, Query
from Database import db, audit

from Server.server_models import (
    CategorieCreate, CategorieUpdate,
    CategorieResponse, CategorieListResponse, SimpleResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/categories", tags=["categories"])


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


# ══════════════════════════════════════════════════════════════════
@router.get("", response_model=CategorieListResponse)
def list_categories(
    request: Request,
    actif: int = Query(1),
):
    """Liste des catégories (actives par défaut)."""
    try:
        where = "1=1"
        params = []
        if actif in (0, 1):
            where = "actif = ?"
            params.append(actif)

        rows = db.query(
            f"SELECT * FROM Categorie WHERE {where} ORDER BY nom ASC",
            tuple(params))

        items = [_row_to_dict(r) for r in rows]
        return {"total": len(items), "items": items}
    except Exception as e:
        logger.exception("Erreur list_categories")
        raise HTTPException(500, f"Erreur : {e}")


@router.post("", response_model=CategorieResponse, status_code=201)
def create_categorie(payload: CategorieCreate, request: Request):
    _require_admin(request)
    user = request.state.user

    nom = payload.nom.strip().upper()
    if not nom:
        raise HTTPException(400, "Nom obligatoire")

    existing = db.query_one(
        "SELECT 1 FROM Categorie WHERE LOWER(nom) = LOWER(?) LIMIT 1",
        (nom,))
    if existing:
        raise HTTPException(409, f"Catégorie '{nom}' existe déjà")

    new_id = db.new_id()
    try:
        with db.transaction():
            db.execute(
                """INSERT INTO Categorie
                   (id, nom, description, actif, created_at)
                   VALUES (?,?,?,1, datetime('now'))""",
                (new_id, nom, payload.description))

            audit.log(
                "CREATION_CATEGORIE",
                utilisateur_id=user.get("uid"),
                utilisateur_name=user.get("ident"),
                cible_type="Categorie",
                cible_id=new_id,
                cible_nom=nom)

        row = db.query_one(
            "SELECT * FROM Categorie WHERE id = ? LIMIT 1", (new_id,))
        return _row_to_dict(row)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur create_categorie")
        raise HTTPException(500, f"Erreur : {e}")


@router.put("/{categorie_id}", response_model=CategorieResponse)
def update_categorie(categorie_id: str,
                     payload: CategorieUpdate, request: Request):
    _require_admin(request)
    user = request.state.user

    existing = db.query_one(
        "SELECT * FROM Categorie WHERE id = ? LIMIT 1",
        (categorie_id,))
    if not existing:
        raise HTTPException(404, "Catégorie introuvable")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(400, "Aucun champ à modifier")

    if "nom" in updates:
        updates["nom"] = (updates["nom"] or "").strip().upper()
        if not updates["nom"]:
            raise HTTPException(400, "Nom obligatoire")
        dup = db.query_one(
            """SELECT 1 FROM Categorie
               WHERE LOWER(nom) = LOWER(?) AND id <> ? LIMIT 1""",
            (updates["nom"], categorie_id))
        if dup:
            raise HTTPException(409, "Catégorie déjà existante")

    try:
        champs, params = [], []
        for k, v in updates.items():
            champs.append(f"{k} = ?")
            params.append(v)
        params.append(categorie_id)

        with db.transaction():
            db.execute(
                f"UPDATE Categorie SET {', '.join(champs)} "
                f"WHERE id = ?", tuple(params))

            audit.log(
                "MODIF_CATEGORIE",
                utilisateur_id=user.get("uid"),
                utilisateur_name=user.get("ident"),
                cible_type="Categorie",
                cible_id=categorie_id,
                cible_nom=existing["nom"],
                details={"champs_modifies": list(updates.keys())})

        row = db.query_one(
            "SELECT * FROM Categorie WHERE id = ? LIMIT 1",
            (categorie_id,))
        return _row_to_dict(row)
    except Exception as e:
        logger.exception("Erreur update_categorie")
        raise HTTPException(500, f"Erreur : {e}")


@router.delete("/{categorie_id}", response_model=SimpleResponse)
def delete_categorie(categorie_id: str, request: Request):
    """Soft delete (actif = 0)."""
    _require_admin(request)
    user = request.state.user

    existing = db.query_one(
        "SELECT nom, actif FROM Categorie WHERE id = ? LIMIT 1",
        (categorie_id,))
    if not existing:
        raise HTTPException(404, "Catégorie introuvable")

    try:
        with db.transaction():
            db.execute(
                "UPDATE Categorie SET actif = 0 WHERE id = ?",
                (categorie_id,))

            audit.log(
                "SUPPRESSION_CATEGORIE",
                utilisateur_id=user.get("uid"),
                utilisateur_name=user.get("ident"),
                cible_type="Categorie",
                cible_id=categorie_id,
                cible_nom=existing["nom"],
                severite="warning")

        return {"status": "ok",
                "message": f"Catégorie '{existing['nom']}' désactivée"}
    except Exception as e:
        logger.exception("Erreur delete_categorie")
        raise HTTPException(500, f"Erreur : {e}")