#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""routes/retours.py — Gestion des retours."""

import logging
from fastapi import APIRouter, Request, HTTPException, Query
from pydantic import BaseModel

from Database import retour_engine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/retours", tags=["retours"])


class LigneRetourInput(BaseModel):
    code_reference: str
    article: str
    quantite: int
    prix_unitaire: float
    total: float
    reconditionne: bool = True


class RetourCreate(BaseModel):
    num_fact_origine: str
    motif: str
    notes: str = None
    lignes: list[LigneRetourInput]
    montant_total: float
    nb_articles: int


@router.get("")
def list_retours(request: Request,
                 page: int = Query(1, ge=1),
                 per_page: int = Query(30, ge=1, le=100),
                 search: str = Query(""),
                 statut: str = Query("")):
    try:
        return retour_engine.list_retours(page, per_page, search, statut)
    except Exception as e:
        logger.exception("Erreur list_retours")
        raise HTTPException(500, str(e))


@router.get("/{retour_id}")
def get_retour(retour_id: str, request: Request):
    r = retour_engine.get_retour(retour_id)
    if not r:
        raise HTTPException(404, "Retour introuvable")
    return r


@router.post("")
async def create_retour(payload: RetourCreate, request: Request):
    user = request.state.user
    if not user:
        raise HTTPException(401, "Non authentifié")

    try:
        data = payload.model_dump()
        # Convertit les lignes Pydantic en dicts
        data["lignes"] = [l if isinstance(l, dict) else l.model_dump()
                          for l in payload.lignes]

        rid = retour_engine.save_retour(
            data, user.get("uid"), user.get("ident"))

        # Récupère le numéro généré
        rv = retour_engine.get_retour(rid)

        return {
            "id": rid,
            "numero_retour": rv["numero_retour"] if rv else "",
            "status": "ok",
        }
    except Exception as e:
        logger.exception("Erreur create_retour")
        raise HTTPException(500, str(e))