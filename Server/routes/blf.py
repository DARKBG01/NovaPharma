#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/blf.py — Bons de Livraison Fournisseur.
================================================
CRUD + validation + annulation (rollback stock).
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Request, HTTPException, Query
from Database import db, audit

from Server.server_models import (
    BLFCreate, BLFAnnulationRequest, BLFResponse,
    BLFDetailResponse, BLFListResponse, SimpleResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/blf", tags=["blf"])


# ══════════════════════════════════════════════════════════════════
def _row_to_dict(row) -> dict:
    return {k: row[k] for k in row.keys()}


def _next_numero_blf() -> tuple[str, int]:
    try:
        compteur = int(db.get_config("blf_compteur", 1))
    except Exception:
        compteur = 1
    num = f"BLF-{datetime.now().year}-{compteur:09d}"
    return num, compteur


# ══════════════════════════════════════════════════════════════════
# GET — Liste paginée
# ══════════════════════════════════════════════════════════════════
@router.get("", response_model=BLFListResponse)
def list_blf(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=200),
    search: str = Query(""),
    statut: str = Query(""),   # BROUILLON|VALIDEE|ANNULEE|""
):
    """Liste paginée des BLF."""
    try:
        where, params = ["1=1"], []
        if search:
            where.append("(numero_blf LIKE ? OR fournisseur_nom LIKE ?)")
            like = f"%{search}%"
            params.extend([like, like])
        if statut:
            where.append("statut = ?")
            params.append(statut)

        wc = " AND ".join(where)

        row = db.query_one(
            f"SELECT COUNT(*) AS n FROM BonLivraison WHERE {wc}",
            tuple(params))
        total = int(row["n"] or 0) if row else 0
        pages = max(1, (total + per_page - 1) // per_page)

        offset = (page - 1) * per_page
        rows = db.query(
            f"""SELECT * FROM BonLivraison
                WHERE {wc}
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?""",
            tuple(params + [per_page, offset]))

        return {
            "total": total, "page": page,
            "per_page": per_page, "pages": pages,
            "items": [_row_to_dict(r) for r in rows],
        }
    except Exception as e:
        logger.exception("Erreur list_blf")
        raise HTTPException(500, f"Erreur : {e}")


# ══════════════════════════════════════════════════════════════════
# GET — Détail
# ══════════════════════════════════════════════════════════════════
@router.get("/{blf_id}", response_model=BLFDetailResponse)
def get_blf(blf_id: str):
    """Détail complet d'un BLF."""
    try:
        row = db.query_one(
            "SELECT * FROM BonLivraison WHERE id = ? LIMIT 1", (blf_id,))
        if not row:
            raise HTTPException(404, "BLF introuvable")

        blf = _row_to_dict(row)
        lignes = db.query(
            "SELECT * FROM LigneBonLivraison WHERE blf_id = ? ORDER BY rowid",
            (blf_id,))
        blf["lignes"] = [_row_to_dict(l) for l in lignes]
        return blf
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur get_blf")
        raise HTTPException(500, f"Erreur : {e}")


# ══════════════════════════════════════════════════════════════════
# POST — Création (brouillon ou validation directe)
# ══════════════════════════════════════════════════════════════════
@router.post("", response_model=BLFResponse, status_code=201)
def create_blf(b: BLFCreate, request: Request):
    """Crée un BLF. Si valider_immediatement=True → impact stock immédiat."""
    user = request.state.user

    # ─── 1. Résoudre les produits ───
    panier = []
    total_achat = 0.0
    nb_unites = 0

    try:
        for l in b.lignes:
            prod = db.query_one(
                """SELECT Code_reference, Nom, Quantite, Prix_achat, Prix_vente
                   FROM produits WHERE Code_reference = ? LIMIT 1""",
                (l.code_ref,))
            if not prod:
                raise HTTPException(404, f"Produit '{l.code_ref}' introuvable")

            pa = (l.prix_achat if l.prix_achat is not None
                  else float(prod["Prix_achat"] or 0))
            pv = (l.prix_vente if l.prix_vente is not None
                  else float(prod["Prix_vente"] or 0))

            ligne_total = round(pa * l.quantite, 2)
            total_achat += ligne_total
            nb_unites += l.quantite

            panier.append({
                "code_ref": prod["Code_reference"],
                "nom": prod["Nom"],
                "qte": l.quantite,
                "pa": pa,
                "pv": pv,
                "total": ligne_total,
                "stock_avant": int(prod["Quantite"] or 0),
            })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Erreur préparation : {e}")

    # ─── 2. Fournisseur ───
    fournisseur_nom = "Sans fournisseur"
    if b.fournisseur_id:
        try:
            f = db.query_one(
                "SELECT Entreprise FROM Fournisseur "
                "WHERE Id_fournisseur = ? LIMIT 1",
                (b.fournisseur_id,))
            if f:
                fournisseur_nom = f["Entreprise"]
        except Exception:
            pass

    # ─── 3. Numéro BLF ───
    numero_blf, compteur = _next_numero_blf()

    statut = "VALIDEE" if b.valider_immediatement else "BROUILLON"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    blf_id = db.new_id()

    # ─── 4. TRANSACTION ───
    try:
        with db.transaction():
            db.execute(
                """INSERT INTO BonLivraison
                   (id, numero_blf, fournisseur_id, fournisseur_nom,
                    statut, total_achat, nb_articles, nb_unites,
                    notes, reference_externe,
                    created_by, created_by_name, created_at,
                    validated_by, validated_by_name, validated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (blf_id, numero_blf, b.fournisseur_id, fournisseur_nom,
                 statut, total_achat, len(panier), nb_unites,
                 b.notes, b.reference_externe,
                 user["uid"], user["ident"], now,
                 user["uid"] if b.valider_immediatement else None,
                 user["ident"] if b.valider_immediatement else None,
                 now if b.valider_immediatement else None))

            for item in panier:
                stock_avant = item["stock_avant"]
                stock_apres = (stock_avant + item["qte"]
                               if b.valider_immediatement else stock_avant)

                db.execute(
                    """INSERT INTO LigneBonLivraison
                       (id, blf_id, produit_id, produit_nom,
                        quantite, prix_achat_unitaire, prix_vente_unitaire,
                        total_ligne, stock_avant, stock_apres)
                       VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (db.new_id(), blf_id, item["code_ref"], item["nom"],
                     item["qte"], item["pa"], item["pv"], item["total"],
                     stock_avant if b.valider_immediatement else None,
                     stock_apres if b.valider_immediatement else None))

                if b.valider_immediatement:
                    db.execute(
                        """UPDATE produits
                           SET Quantite = ?, Prix_achat = ?,
                               Prix_vente = ?, Prix_unitaire = ?
                           WHERE Code_reference = ?""",
                        (stock_apres, item["pa"], item["pv"],
                         item["pv"], item["code_ref"]))

                    db.execute(
                        """INSERT INTO MouvementStock
                           (id, produit_id, type, quantite,
                            stock_avant, stock_apres, motif, utilisateur_id)
                           VALUES (?,?,?,?,?,?,?,?)""",
                        (db.new_id(), item["code_ref"], "ENTREE",
                         item["qte"], stock_avant, stock_apres,
                         f"BLF {numero_blf} — {fournisseur_nom}",
                         user["uid"]))

            db.set_config("blf_compteur", compteur + 1, type_="int")

            audit.log(
                audit.ACTION_CREATION_BLF,
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="BonLivraison",
                cible_id=blf_id,
                cible_nom=numero_blf,
                details={
                    "statut": statut,
                    "total": total_achat,
                    "nb_articles": len(panier),
                    "nb_unites": nb_unites,
                    "fournisseur_nom": fournisseur_nom,
                    "source": "server",
                },
                apres={
                    "numero_blf": numero_blf,
                    "statut": statut,
                    "total_achat": total_achat,
                    "nb_articles": len(panier),
                    "nb_unites": nb_unites,
                })

            if b.valider_immediatement:
                audit.log(
                    "VALIDATION_BLF",
                    utilisateur_id=user["uid"],
                    utilisateur_name=user["ident"],
                    cible_type="blf", cible_id=blf_id, cible_nom=numero_blf)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Échec création BLF")
        raise HTTPException(500, f"Erreur création : {e}")

    logger.info("BLF créé : %s (%s)", numero_blf, statut)

    row = db.query_one(
        "SELECT * FROM BonLivraison WHERE id = ? LIMIT 1", (blf_id,))
    return _row_to_dict(row)


# ══════════════════════════════════════════════════════════════════
# POST — Valider un BLF brouillon
# ══════════════════════════════════════════════════════════════════
@router.post("/{blf_id}/valider", response_model=SimpleResponse)
def valider_blf(blf_id: str, request: Request):
    """Valide un BLF brouillon : impact stock + prix."""
    user = request.state.user

    blf = db.query_one(
        "SELECT * FROM BonLivraison WHERE id = ? LIMIT 1", (blf_id,))
    if not blf:
        raise HTTPException(404, "BLF introuvable")
    if blf["statut"] != "BROUILLON":
        raise HTTPException(400, f"BLF non modifiable (statut : {blf['statut']})")

    lignes = db.query(
        "SELECT * FROM LigneBonLivraison WHERE blf_id = ?", (blf_id,))
    if not lignes:
        raise HTTPException(400, "BLF sans ligne")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with db.transaction():
            db.execute(
                """UPDATE BonLivraison
                   SET statut = 'VALIDEE',
                       validated_by = ?, validated_by_name = ?,
                       validated_at = ?
                   WHERE id = ?""",
                (user["uid"], user["ident"], now, blf_id))

            for l in lignes:
                code_ref = l["produit_id"]
                if not code_ref:
                    continue

                row_p = db.query_one(
                    "SELECT Quantite FROM produits "
                    "WHERE Code_reference = ? LIMIT 1", (code_ref,))
                if not row_p:
                    continue

                avant = int(row_p["Quantite"] or 0)
                apres = avant + int(l["quantite"])

                db.execute(
                    """UPDATE LigneBonLivraison
                       SET stock_avant = ?, stock_apres = ?
                       WHERE id = ?""",
                    (avant, apres, l["id"]))

                db.execute(
                    """UPDATE produits
                       SET Quantite = ?, Prix_achat = ?,
                           Prix_vente = ?, Prix_unitaire = ?
                       WHERE Code_reference = ?""",
                    (apres, l["prix_achat_unitaire"],
                     l["prix_vente_unitaire"], l["prix_vente_unitaire"],
                     code_ref))

                db.execute(
                    """INSERT INTO MouvementStock
                       (id, produit_id, type, quantite,
                        stock_avant, stock_apres, motif, utilisateur_id)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (db.new_id(), code_ref, "ENTREE", l["quantite"],
                     avant, apres,
                     f"BLF {blf['numero_blf']} (validation)",
                     user["uid"]))

            audit.log(
                audit.ACTION_VALIDATION_BLF,
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="BonLivraison",
                cible_id=blf_id,
                cible_nom=blf["numero_blf"],
                details={
                    "nb_articles": blf["nb_articles"],
                    "nb_unites": blf["nb_unites"],
                    "source": "server",
                },
                avant={
                    "statut": "BROUILLON",
                    "total_achat": blf["total_achat"],
                },
                apres={
                    "statut": "VALIDEE",
                    "validated_by_name": user["ident"],
                })

        return {"status": "ok", "message": "BLF validé"}

    except Exception as e:
        logger.exception("Échec validation BLF")
        raise HTTPException(500, f"Erreur validation : {e}")


# ══════════════════════════════════════════════════════════════════
# POST — Annuler un BLF validé (rollback stock)
# ══════════════════════════════════════════════════════════════════
@router.post("/{blf_id}/annuler", response_model=SimpleResponse)
def annuler_blf(blf_id: str, req: BLFAnnulationRequest, request: Request):
    """Annule un BLF validé → retire le stock ajouté."""
    user = request.state.user

    blf = db.query_one(
        "SELECT * FROM BonLivraison WHERE id = ? LIMIT 1", (blf_id,))
    if not blf:
        raise HTTPException(404, "BLF introuvable")
    if blf["statut"] != "VALIDEE":
        raise HTTPException(400, "Seul un BLF validé peut être annulé")

    lignes = db.query(
        "SELECT * FROM LigneBonLivraison WHERE blf_id = ?", (blf_id,))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with db.transaction():
            db.execute(
                """UPDATE BonLivraison
                   SET statut = 'ANNULEE',
                       cancelled_by = ?, cancelled_by_name = ?,
                       cancelled_at = ?, motif_annulation = ?
                   WHERE id = ?""",
                (user["uid"], user["ident"], now, req.motif, blf_id))

            for l in lignes:
                code_ref = l["produit_id"]
                if not code_ref:
                    continue

                row_p = db.query_one(
                    "SELECT Quantite FROM produits "
                    "WHERE Code_reference = ? LIMIT 1", (code_ref,))
                if not row_p:
                    continue

                qte = int(l["quantite"])
                avant = int(row_p["Quantite"] or 0)
                apres = max(0, avant - qte)

                db.execute(
                    "UPDATE produits SET Quantite = ? "
                    "WHERE Code_reference = ?", (apres, code_ref))

                db.execute(
                    """INSERT INTO MouvementStock
                       (id, produit_id, type, quantite,
                        stock_avant, stock_apres, motif, utilisateur_id)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (db.new_id(), code_ref, "ANNULATION", -qte,
                     avant, apres,
                     f"Annulation BLF {blf['numero_blf']} — {req.motif}",
                     user["uid"]))

                db.execute(
                    """INSERT INTO AjustementStock
                       (id, Code_reference, Nom_produit,
                        stock_avant, stock_apres, difference,
                        motif, utilisateur_id)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (db.new_id(), code_ref, l["produit_nom"],
                     avant, apres, -qte,
                     f"Annulation BLF {blf['numero_blf']}",
                     user["uid"]))

            audit.log(
                audit.ACTION_ANNULATION_BLF,
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="BonLivraison",
                cible_id=blf_id,
                cible_nom=blf["numero_blf"],
                details={
                    "motif": req.motif,
                    "stock_retire": blf["nb_unites"],
                    "source": "server",
                },
                avant={
                    "statut": "VALIDEE",
                    "total_achat": blf["total_achat"],
                },
                apres={
                    "statut": "ANNULEE",
                    "motif_annulation": req.motif,
                    "cancelled_by_name": user["ident"],
                })

        return {"status": "ok", "message": "BLF annulé, stock restitué"}

    except Exception as e:
        logger.exception("Échec annulation BLF")
        raise HTTPException(500, f"Erreur annulation : {e}")


# ══════════════════════════════════════════════════════════════════
# DELETE — Supprimer un BROUILLON uniquement
# ══════════════════════════════════════════════════════════════════
@router.delete("/{blf_id}", response_model=SimpleResponse)
def delete_brouillon(blf_id: str, request: Request):
    """Supprime un BLF en brouillon (hard delete)."""
    user = request.state.user

    blf = db.query_one(
        "SELECT numero_blf, statut FROM BonLivraison WHERE id = ? LIMIT 1",
        (blf_id,))
    if not blf:
        raise HTTPException(404, "BLF introuvable")
    if blf["statut"] != "BROUILLON":
        raise HTTPException(400, "Seuls les brouillons peuvent être supprimés")

    try:
        with db.transaction():
            db.execute(
                "DELETE FROM BonLivraison WHERE id = ?", (blf_id,))

            audit.log(
                "SUPPRESSION_BLF_BROUILLON",
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="blf", cible_id=blf_id,
                cible_nom=blf["numero_blf"])

        return {"status": "ok", "message": "Brouillon supprimé"}

    except Exception as e:
        logger.exception("Échec suppression BLF")
        raise HTTPException(500, f"Erreur : {e}")