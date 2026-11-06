#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/produits.py — CRUD produits + ajustement stock.
========================================================
Toutes les routes nécessitent un token valide.
"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Query
from Database import db, audit

from Server.server_models import (
    ProduitCreate, ProduitUpdate, ProduitResponse,
    ProduitListResponse, StockAdjustRequest, SimpleResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/produits", tags=["produits"])


# ══════════════════════════════════════════════════════════════════
def _row_to_dict(row) -> dict:
    return {k: row[k] for k in row.keys()}


def _next_code_reference() -> str:
    """Génère MED-XXXXX séquentiel."""
    try:
        row = db.query_one(
            "SELECT Code_reference FROM produits "
            "WHERE Code_reference LIKE 'MED-%' "
            "ORDER BY Code_reference DESC LIMIT 1")
        if row:
            try:
                n = int(row["Code_reference"].split("-")[1]) + 1
            except (ValueError, IndexError):
                n = 1
        else:
            n = 1
        return f"MED-{n:05d}"
    except Exception:
        return f"MED-{datetime.now().strftime('%H%M%S')}"


# ══════════════════════════════════════════════════════════════════
# GET — Liste paginée + recherche + filtre
# ══════════════════════════════════════════════════════════════════
@router.get("", response_model=ProduitListResponse)
def list_produits(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    search: Optional[str] = Query(None),
    categorie: Optional[str] = Query(None),
    actif: Optional[int] = Query(1),
    rupture: Optional[bool] = Query(False),
):
    """Liste paginée des produits."""
    try:
        where, params = ["1=1"], []

        if actif is not None:
            where.append("actif = ?")
            params.append(actif)

        if search:
            where.append("(Nom LIKE ? OR Code_reference LIKE ? OR "
                         "Code_barre LIKE ?)")
            like = f"%{search}%"
            params.extend([like, like, like])

        if categorie:
            where.append("Categorie = ?")
            params.append(categorie)

        if rupture:
            try:
                seuil = int(db.get_config("seuil_stock", 20))
            except Exception:
                seuil = 20
            where.append("Quantite <= ?")
            params.append(seuil)

        wc = " AND ".join(where)

        # Compte total
        row = db.query_one(
            f"SELECT COUNT(*) AS n FROM produits WHERE {wc}",
            tuple(params))
        total = int(row["n"] or 0) if row else 0
        pages = max(1, (total + per_page - 1) // per_page)

        # Page courante
        offset = (page - 1) * per_page
        rows = db.query(
            f"""SELECT * FROM produits
                WHERE {wc}
                ORDER BY Nom ASC
                LIMIT ? OFFSET ?""",
            tuple(params + [per_page, offset]))

        items = [_row_to_dict(r) for r in rows]

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
            "items": items,
        }
    except Exception as e:
        logger.exception("Erreur list_produits")
        raise HTTPException(500, f"Erreur interne : {e}")


# ══════════════════════════════════════════════════════════════════
# GET — Détail d'un produit
# ══════════════════════════════════════════════════════════════════
@router.get("/{code_ref}", response_model=ProduitResponse)
def get_produit(code_ref: str):
    """Détail d'un produit par son code référence."""
    row = db.query_one(
        "SELECT * FROM produits WHERE Code_reference = ? LIMIT 1",
        (code_ref,))
    if not row:
        raise HTTPException(404, f"Produit '{code_ref}' introuvable")
    return _row_to_dict(row)


# ══════════════════════════════════════════════════════════════════
# POST — Création
# ══════════════════════════════════════════════════════════════════
@router.post("", response_model=ProduitResponse, status_code=201)
def create_produit(p: ProduitCreate, request: Request):
    """Crée un nouveau produit."""
    user = request.state.user

    try:
        # Génère le code si absent
        code_ref = (p.Code_reference or "").strip().upper() \
            or _next_code_reference()

        # Vérif unicité
        if db.query_one(
            "SELECT 1 FROM produits WHERE Code_reference = ? LIMIT 1",
            (code_ref,)
        ):
            raise HTTPException(409, f"Le code '{code_ref}' existe déjà")

        if db.query_one(
            "SELECT 1 FROM produits WHERE LOWER(Nom) = LOWER(?) LIMIT 1",
            (p.Nom,)
        ):
            raise HTTPException(
                409, f"Un produit nommé '{p.Nom}' existe déjà")

        # Valeur par défaut Prix_unitaire
        prix_unitaire = p.Prix_unitaire if p.Prix_unitaire is not None \
            else p.Prix_vente

        with db.transaction():
            db.execute(
                """INSERT INTO produits
                   (Code_reference, Nom, Code_barre, Categorie,
                    Description, Unite, Quantite_initiale, Quantite,
                    Prix_achat, Prix_vente, Prix_unitaire,
                    Cree_par, Date_ajout, actif)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?, datetime('now'), 1)""",
                (code_ref, p.Nom, p.Code_barre, p.Categorie,
                 p.Description, p.Unite, p.Quantite, p.Quantite,
                 p.Prix_achat, p.Prix_vente, prix_unitaire,
                 user["ident"]))

            # Mouvement d'entrée initiale
            if p.Quantite > 0:
                db.execute(
                    """INSERT INTO MouvementStock
                       (id, produit_id, type, quantite,
                        stock_avant, stock_apres, motif, utilisateur_id)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (db.new_id(), code_ref, "ENTREE", p.Quantite,
                     0, p.Quantite, "Stock initial", user["uid"]))

            audit.log(
                "CREATION_PRODUIT",
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="produit", cible_id=code_ref,
                cible_nom=p.Nom,
                details={"source": "server"})

        logger.info("Produit créé : %s (%s)", p.Nom, code_ref)

        row = db.query_one(
            "SELECT * FROM produits WHERE Code_reference = ? LIMIT 1",
            (code_ref,))
        return _row_to_dict(row)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur create_produit")
        raise HTTPException(500, f"Erreur création : {e}")


# ══════════════════════════════════════════════════════════════════
# PUT — Modification
# ══════════════════════════════════════════════════════════════════
@router.put("/{code_ref}", response_model=ProduitResponse)
def update_produit(code_ref: str, p: ProduitUpdate, request: Request):
    """Modifie un produit existant."""
    user = request.state.user

    existing = db.query_one(
        "SELECT * FROM produits WHERE Code_reference = ? LIMIT 1",
        (code_ref,))
    if not existing:
        raise HTTPException(404, f"Produit '{code_ref}' introuvable")

    # Vérif unicité nom (si changé)
    if p.Nom and p.Nom.lower() != (existing["Nom"] or "").lower():
        dup = db.query_one(
            """SELECT 1 FROM produits
               WHERE LOWER(Nom) = LOWER(?) AND Code_reference <> ?
               LIMIT 1""",
            (p.Nom, code_ref))
        if dup:
            raise HTTPException(409, f"Un produit nommé '{p.Nom}' existe")

    # Prépare les champs modifiables
    champs = []
    params = []
    for field in ("Nom", "Code_barre", "Categorie", "Description",
                  "Unite", "Quantite", "Prix_achat", "Prix_vente",
                  "Prix_unitaire"):
        val = getattr(p, field, None)
        if val is not None:
            champs.append(f"{field} = ?")
            params.append(val)

    if not champs:
        raise HTTPException(400, "Aucun champ à modifier")

    params.append(code_ref)

    try:
        with db.transaction():
            db.execute(
                f"UPDATE produits SET {', '.join(champs)} "
                f"WHERE Code_reference = ?",
                tuple(params))

            # Trace ajustement stock si Quantite change
            if p.Quantite is not None:
                avant = int(existing["Quantite"] or 0)
                apres = int(p.Quantite)
                if avant != apres:
                    db.execute(
                        """INSERT INTO AjustementStock
                           (id, Code_reference, Nom_produit,
                            stock_avant, stock_apres, difference,
                            motif, utilisateur_id)
                           VALUES (?,?,?,?,?,?,?,?)""",
                        (db.new_id(), code_ref,
                         p.Nom or existing["Nom"],
                         avant, apres, apres - avant,
                         "Modification via API",
                         user["uid"]))

            audit.log(
                "MODIF_PRODUIT",
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="produit", cible_id=code_ref,
                cible_nom=p.Nom or existing["Nom"],
                details={"source": "server"})

        logger.info("Produit modifié : %s", code_ref)

        row = db.query_one(
            "SELECT * FROM produits WHERE Code_reference = ? LIMIT 1",
            (code_ref,))
        return _row_to_dict(row)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur update_produit")
        raise HTTPException(500, f"Erreur modification : {e}")


# ══════════════════════════════════════════════════════════════════
# DELETE — Soft delete
# ══════════════════════════════════════════════════════════════════
@router.delete("/{code_ref}", response_model=SimpleResponse)
def delete_produit(code_ref: str, request: Request):
    """Soft delete : passe actif = 0."""
    user = request.state.user

    existing = db.query_one(
        "SELECT Nom, actif FROM produits WHERE Code_reference = ? LIMIT 1",
        (code_ref,))
    if not existing:
        raise HTTPException(404, f"Produit '{code_ref}' introuvable")

    if not existing["actif"]:
        raise HTTPException(400, "Le produit est déjà supprimé")

    try:
        with db.transaction():
            db.execute(
                "UPDATE produits SET actif = 0 WHERE Code_reference = ?",
                (code_ref,))

            audit.log(
                "SUPPRESSION_PRODUIT",
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="produit", cible_id=code_ref,
                cible_nom=existing["Nom"],
                details={"source": "server"})

        logger.info("Produit désactivé : %s", code_ref)
        return {"status": "ok",
                "message": f"Produit '{existing['Nom']}' supprimé"}

    except Exception as e:
        logger.exception("Erreur delete_produit")
        raise HTTPException(500, f"Erreur suppression : {e}")


# ══════════════════════════════════════════════════════════════════
# POST — Ajustement manuel de stock
# ══════════════════════════════════════════════════════════════════
@router.post("/{code_ref}/stock", response_model=ProduitResponse)
def ajuster_stock(code_ref: str, req: StockAdjustRequest, request: Request):
    """Ajuste le stock d'un produit avec motif obligatoire."""
    user = request.state.user

    existing = db.query_one(
        "SELECT Nom, Quantite FROM produits "
        "WHERE Code_reference = ? LIMIT 1",
        (code_ref,))
    if not existing:
        raise HTTPException(404, f"Produit '{code_ref}' introuvable")

    avant = int(existing["Quantite"] or 0)
    apres = req.nouvelle_quantite
    diff = apres - avant

    if diff == 0:
        raise HTTPException(400, "Aucun changement de quantité")

    try:
        with db.transaction():
            db.execute(
                "UPDATE produits SET Quantite = ? WHERE Code_reference = ?",
                (apres, code_ref))

            db.execute(
                """INSERT INTO AjustementStock
                   (id, Code_reference, Nom_produit,
                    stock_avant, stock_apres, difference,
                    motif, utilisateur_id)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (db.new_id(), code_ref, existing["Nom"],
                 avant, apres, diff, req.motif, user["uid"]))

            db.execute(
                """INSERT INTO MouvementStock
                   (id, produit_id, type, quantite,
                    stock_avant, stock_apres, motif, utilisateur_id)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (db.new_id(), code_ref, "AJUSTEMENT", diff,
                 avant, apres, req.motif, user["uid"]))

            audit.log(
                "MODIF_STOCK_MANUEL",
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="produit", cible_id=code_ref,
                cible_nom=existing["Nom"],
                details={"motif": req.motif, "diff": diff,
                         "source": "server"})

        logger.info("Stock ajusté : %s (%+d)", code_ref, diff)

        row = db.query_one(
            "SELECT * FROM produits WHERE Code_reference = ? LIMIT 1",
            (code_ref,))
        return _row_to_dict(row)

    except Exception as e:
        logger.exception("Erreur ajuster_stock")
        raise HTTPException(500, f"Erreur ajustement : {e}")