#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/clients.py — CRUD clients + fiche détaillée.
=====================================================
Toutes les routes nécessitent un token valide.
"""

import logging
import re
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Query
from Database import db, audit

from Server.server_models import (
    ClientCreate, ClientUpdate, ClientResponse,
    ClientListResponse, ClientDetailResponse, SimpleResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/clients", tags=["clients"])


# ══════════════════════════════════════════════════════════════════
PHONE_REGEX = re.compile(r"^(?:\+243\d{9}|0\d{9})$")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
HISTORY_LIMIT = 200


def _row_to_dict(row) -> dict:
    return {k: row[k] for k in row.keys()}


def _normalize(row) -> dict:
    """Uniformise C_name/nom + Montant_total."""
    d = _row_to_dict(row)
    d["nom"] = d.get("C_name") or d.get("nom") or "—"
    try:
        d["Montant_total"] = float(d.get("Montant_total") or 0)
    except Exception:
        d["Montant_total"] = 0.0
    return d


def _generate_anonymous() -> tuple[str, str]:
    """Génère (nom_anonyme, numero_anonyme)."""
    today = datetime.now().strftime("%Y%m%d")
    for _ in range(20):
        suffix = db.new_id().replace("-", "")[:4].upper()
        numero = f"ANON-{today}-{suffix}"
        try:
            if not db.query_one(
                "SELECT 1 FROM Client WHERE numero = ? LIMIT 1",
                (numero,)
            ):
                return f"Anonyme #{suffix}", numero
        except Exception:
            continue
    # Fallback
    import time
    numero = f"ANON-{today}-{int(time.time()) % 10000:04d}"
    return f"Anonyme #{numero[-4:]}", numero


# ══════════════════════════════════════════════════════════════════
# GET — Liste paginée + recherche + filtre
# ══════════════════════════════════════════════════════════════════
@router.get("", response_model=ClientListResponse)
def list_clients(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    search: Optional[str] = Query(None),
    filtre: Optional[str] = Query("tous"),  # tous|actifs|anonymes|inactifs
    actif: Optional[int] = Query(1),
):
    """Liste paginée des clients."""
    try:
        where, params = ["1=1"], []

        if filtre == "actifs":
            where.append("actif = 1 AND numero NOT LIKE 'ANON-%'")
        elif filtre == "anonymes":
            where.append("numero LIKE 'ANON-%'")
        elif filtre == "inactifs":
            where.append("actif = 0")
        elif actif is not None:
            where.append("actif = ?")
            params.append(actif)

        if search:
            where.append("(nom LIKE ? OR C_name LIKE ? OR numero LIKE ?)")
            like = f"%{search}%"
            params.extend([like, like, like])

        wc = " AND ".join(where)

        row = db.query_one(
            f"SELECT COUNT(*) AS n FROM Client WHERE {wc}",
            tuple(params))
        total = int(row["n"] or 0) if row else 0
        pages = max(1, (total + per_page - 1) // per_page)

        offset = (page - 1) * per_page
        rows = db.query(
            f"""SELECT * FROM Client
                WHERE {wc}
                ORDER BY COALESCE(C_name, nom) COLLATE NOCASE ASC
                LIMIT ? OFFSET ?""",
            tuple(params + [per_page, offset]))

        items = [_normalize(r) for r in rows]

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
            "items": items,
        }
    except Exception as e:
        logger.exception("Erreur list_clients")
        raise HTTPException(500, f"Erreur interne : {e}")


# ══════════════════════════════════════════════════════════════════
# GET — Détail + stats + historique
# ══════════════════════════════════════════════════════════════════
@router.get("/{client_id}", response_model=ClientDetailResponse)
def get_client(client_id: str):
    """Fiche détaillée d'un client."""
    row = db.query_one(
        "SELECT * FROM Client WHERE id = ? LIMIT 1", (client_id,))
    if not row:
        raise HTTPException(404, "Client introuvable")

    client = _normalize(row)

    nom = client.get("nom") or ""
    numero = client.get("numero") or ""
    # Historique.Client_name est stocké exactement "{nom} {numero}"
    exact_name = f"{nom} {numero}".strip() if numero else nom

    # Stats
    try:
        stats = db.query_one(
            """SELECT COUNT(DISTINCT Num_fact) AS n,
                      MAX(Date_vent) AS last
               FROM Historique
               WHERE Client_name = ?""",
            (exact_name,))
        client["nb_visites"] = int(stats["n"] or 0) if stats else 0
        client["derniere_visite"] = stats["last"] if stats else None
    except Exception:
        client["nb_visites"] = 0
        client["derniere_visite"] = None

    # Historique des achats
    try:
        rows = db.query(
            """SELECT Date_vent, Num_fact, Article, Quantite, Total
               FROM Historique
               WHERE Client_name = ?
               ORDER BY Date_vent DESC
               LIMIT ?""",
            (exact_name, HISTORY_LIMIT))
        client["historique"] = [_row_to_dict(r) for r in rows]
    except Exception:
        client["historique"] = []

    return client


# ══════════════════════════════════════════════════════════════════
# GET — Recherche par numéro (utilisé par facturation live)
# ══════════════════════════════════════════════════════════════════
@router.get("/numero/{numero}")
def find_by_numero(numero: str):
    """Recherche un client par numéro (avec variantes +243↔0)."""
    num = numero.replace(" ", "").replace("-", "").replace(".", "")

    row = db.query_one(
        "SELECT id, COALESCE(C_name, nom) AS nom, numero, Montant_total, actif "
        "FROM Client WHERE numero = ? LIMIT 1",
        (num,))
    if row:
        return _row_to_dict(row)

    variantes = []
    if num.startswith("+243") and len(num) == 13:
        variantes.append("0" + num[4:])
    elif num.startswith("0") and len(num) == 10:
        variantes.append("+243" + num[1:])

    for var in variantes:
        row = db.query_one(
            "SELECT id, COALESCE(C_name, nom) AS nom, numero, "
            "Montant_total, actif FROM Client WHERE numero = ? LIMIT 1",
            (var,))
        if row:
            return _row_to_dict(row)

    raise HTTPException(404, f"Aucun client avec le numéro {num}")


# ══════════════════════════════════════════════════════════════════
# POST — Création
# ══════════════════════════════════════════════════════════════════
@router.post("", response_model=ClientResponse, status_code=201)
def create_client(c: ClientCreate, request: Request):
    """Crée un nouveau client (ou anonyme)."""
    user = request.state.user

    try:
        if c.anonyme:
            nom, numero = _generate_anonymous()
            email = None
            adresse = c.adresse
            notes = c.notes
        else:
            nom = (c.nom or "").strip()
            numero = (c.numero or "").strip().replace(" ", "")

            if len(nom) < 2:
                raise HTTPException(400, "Nom du client trop court")
            if not PHONE_REGEX.match(numero):
                raise HTTPException(400,
                    "Numéro invalide (format +243XXXXXXXXX ou 0XXXXXXXXX)")

            if c.email and not EMAIL_REGEX.match(c.email):
                raise HTTPException(400, "Email invalide")

            # Unicité
            if db.query_one(
                "SELECT 1 FROM Client WHERE numero = ? LIMIT 1",
                (numero,)
            ):
                raise HTTPException(409, f"Numéro déjà utilisé : {numero}")

            email = c.email.lower() if c.email else None
            adresse = c.adresse
            notes = c.notes

        new_id = db.new_id()

        with db.transaction():
            db.execute(
                """INSERT INTO Client
                   (id, nom, numero, adresse, Id_client, C_name,
                    Montant_total, email, notes, sexe, actif, created_at)
                   VALUES (?,?,?,?,?,?,0,?,?,?,1, datetime('now'))""",
                (new_id, nom, numero, adresse, new_id, nom,
                 email, notes, c.sexe or "M"))

            audit.log(
                "CREATION_CLIENT",
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="client", cible_id=new_id,
                cible_nom=nom,
                details={"anonyme": c.anonyme, "source": "server"})

        logger.info("Client créé : %s (%s)", nom, numero)

        row = db.query_one(
            "SELECT * FROM Client WHERE id = ? LIMIT 1", (new_id,))
        return _normalize(row)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur create_client")
        raise HTTPException(500, f"Erreur création : {e}")


# ══════════════════════════════════════════════════════════════════
# PUT — Modification
# ══════════════════════════════════════════════════════════════════
@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: str, c: ClientUpdate, request: Request):
    """Modifie un client existant."""
    user = request.state.user

    existing = db.query_one(
        "SELECT * FROM Client WHERE id = ? LIMIT 1", (client_id,))
    if not existing:
        raise HTTPException(404, "Client introuvable")

    # Si numero change, valider
    if c.numero:
        num_clean = c.numero.strip().replace(" ", "")
        if not PHONE_REGEX.match(num_clean):
            raise HTTPException(400, "Numéro invalide")
        if num_clean != existing["numero"]:
            dup = db.query_one(
                """SELECT 1 FROM Client
                   WHERE numero = ? AND id <> ? LIMIT 1""",
                (num_clean, client_id))
            if dup:
                raise HTTPException(409, f"Numéro déjà utilisé : {num_clean}")

    # Prépare UPDATE
    champs, params = [], []
    mapping = {
        "nom": c.nom, "numero": c.numero, "adresse": c.adresse,
        "email": c.email, "notes": c.notes, "sexe": c.sexe,
    }
    for field, val in mapping.items():
        if val is not None:
            champs.append(f"{field} = ?")
            params.append(val)
            # Sync C_name si nom
            if field == "nom":
                champs.append("C_name = ?")
                params.append(val)

    if not champs:
        raise HTTPException(400, "Aucun champ à modifier")

    params.append(client_id)

    try:
        with db.transaction():
            db.execute(
                f"UPDATE Client SET {', '.join(champs)} WHERE id = ?",
                tuple(params))

            audit.log(
                "MODIF_CLIENT",
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="client", cible_id=client_id,
                cible_nom=c.nom or existing["nom"],
                details={"source": "server"})

        logger.info("Client modifié : %s", client_id)

        row = db.query_one(
            "SELECT * FROM Client WHERE id = ? LIMIT 1", (client_id,))
        return _normalize(row)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur update_client")
        raise HTTPException(500, f"Erreur modification : {e}")


# ══════════════════════════════════════════════════════════════════
# DELETE — Soft delete (désactivation)
# ══════════════════════════════════════════════════════════════════
@router.delete("/{client_id}", response_model=SimpleResponse)
def delete_client(client_id: str, request: Request):
    """Soft delete : actif = 0."""
    user = request.state.user

    existing = db.query_one(
        "SELECT COALESCE(C_name, nom) AS nom, actif FROM Client "
        "WHERE id = ? LIMIT 1", (client_id,))
    if not existing:
        raise HTTPException(404, "Client introuvable")

    if not existing["actif"]:
        raise HTTPException(400, "Client déjà inactif")

    try:
        with db.transaction():
            db.execute(
                "UPDATE Client SET actif = 0 WHERE id = ?",
                (client_id,))

            audit.log(
                "SUPPRESSION_CLIENT",
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="client", cible_id=client_id,
                cible_nom=existing["nom"],
                details={"source": "server"})

        logger.info("Client désactivé : %s", client_id)
        return {"status": "ok",
                "message": f"Client '{existing['nom']}' désactivé"}

    except Exception as e:
        logger.exception("Erreur delete_client")
        raise HTTPException(500, f"Erreur suppression : {e}")


# ══════════════════════════════════════════════════════════════════
# POST — Réactivation
# ══════════════════════════════════════════════════════════════════
@router.post("/{client_id}/reactiver", response_model=SimpleResponse)
def reactiver_client(client_id: str, request: Request):
    """Réactive un client (actif = 1)."""
    user = request.state.user

    existing = db.query_one(
        "SELECT COALESCE(C_name, nom) AS nom, actif FROM Client "
        "WHERE id = ? LIMIT 1", (client_id,))
    if not existing:
        raise HTTPException(404, "Client introuvable")
    if existing["actif"]:
        raise HTTPException(400, "Client déjà actif")

    try:
        with db.transaction():
            db.execute(
                "UPDATE Client SET actif = 1 WHERE id = ?", (client_id,))

            audit.log(
                "ACTIVATION_CLIENT",
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="client", cible_id=client_id,
                cible_nom=existing["nom"])

        return {"status": "ok", "message": "Client réactivé"}

    except Exception as e:
        logger.exception("Erreur reactiver_client")
        raise HTTPException(500, f"Erreur : {e}")



