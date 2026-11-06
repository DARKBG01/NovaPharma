#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/ventes.py — Ventes (création, liste, détail, annulation).
=================================================================
Toutes les routes nécessitent un token valide.

La création d'une vente est ATOMIQUE :
  - INSERT Historique (1 ligne par article)
  - UPDATE stock (produits.Quantite)
  - INSERT MouvementStock (SORTIE)
  - UPDATE Client.Montant_total (si client identifié)
  - Incrément Compteur facture
Tout est fait dans une seule transaction SQLite.
"""

import logging
import os
import time
from datetime import datetime

from fastapi import APIRouter, Request, HTTPException, Query
from Database import db, audit

from Server.server_models import (
    VenteCreate, AnnulationRequest, VenteResponse,
    VenteListResponse, VenteCreateResponse, SimpleResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/ventes", tags=["ventes"])


# ══════════════════════════════════════════════════════════════════
def _row_to_dict(row) -> dict:
    return {k: row[k] for k in row.keys()}


def _fmt_date_fr() -> str:
    """Date FR conforme à Historique.Date_vent."""
    return time.strftime("%d/%m/%Y %H:%M:%S")


def _numero_facture() -> tuple[str, str, int]:
    """Génère (numero_facture, caisse, temoin_suivant)."""
    try:
        caisse = db.get_config("facture_numero_caisse", "01") or "01"
    except Exception:
        caisse = "01"
    try:
        temoin = int(db.get_config("facture_numero_temoin", 1))
    except Exception:
        temoin = 1

    num = f"F{caisse}-{time.strftime('%Y-%m-%d')}-{temoin:09d}"
    return num, caisse, temoin


# ══════════════════════════════════════════════════════════════════
# GET — Liste paginée des factures (groupées)
# ══════════════════════════════════════════════════════════════════
@router.get("", response_model=VenteListResponse)
def list_ventes(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    search: str = Query(""),
    date_debut: str = Query(""),   # YYYY-MM-DD
    date_fin: str = Query(""),
    annule: int = Query(-1),        # -1=tous, 0=valides, 1=annulées
):
    """Liste paginée des factures."""
    try:
        where, params = ["1=1"], []

        if search:
            where.append("(Num_fact LIKE ? OR Article LIKE ? "
                         "OR Client_name LIKE ? OR Code_reference LIKE ?)")
            like = f"%{search}%"
            params.extend([like, like, like, like])

        # Historique est en FR, on utilise _iso_expr pour comparer
        date_iso = (
            "(substr(Date_vent, 7, 4) || '-' || substr(Date_vent, 4, 2) || "
            "'-' || substr(Date_vent, 1, 2) || substr(Date_vent, 11))"
        )

        if date_debut:
            where.append(f"({date_iso}) >= ?")
            params.append(f"{date_debut} 00:00:00")
        if date_fin:
            where.append(f"({date_iso}) <= ?")
            params.append(f"{date_fin} 23:59:59")

        if annule == 0:
            where.append("COALESCE(annule, 0) = 0")
        elif annule == 1:
            where.append("COALESCE(annule, 0) = 1")

        wc = " AND ".join(where)

        # Compte les factures distinctes
        row = db.query_one(
            f"SELECT COUNT(DISTINCT Num_fact) AS n FROM Historique WHERE {wc}",
            tuple(params))
        total = int(row["n"] or 0) if row else 0
        pages = max(1, (total + per_page - 1) // per_page)

        offset = (page - 1) * per_page

        # Récupère les Num_fact de la page, puis agrège
        factures = db.query(
            f"""SELECT Num_fact, MAX(Date_vent) AS Date_vent,
                       MAX(Client_name) AS Client_name,
                       MAX(Caisse) AS Caisse,
                       MAX(utilisateur_id) AS utilisateur_id,
                       MAX(COALESCE(annule, 0)) AS annule,
                       MAX(motif_annulation) AS motif_annulation,
                       SUM(Total) AS total,
                       SUM(Quantite) AS nb_articles
                FROM Historique
                WHERE {wc}
                GROUP BY Num_fact
                ORDER BY MAX(Id) DESC
                LIMIT ? OFFSET ?""",
            tuple(params + [per_page, offset]))

        items = [_row_to_dict(f) for f in factures]

        # Enrichit avec le nom du caissier
        uids = list({it["utilisateur_id"] for it in items
                     if it.get("utilisateur_id")})
        caissiers = {}
        if uids:
            placeholders = ",".join("?" * len(uids))
            try:
                rows = db.query(
                    f"""SELECT id, COALESCE(prenom,'') || ' ' ||
                              COALESCE(nom,'') AS nom
                        FROM Utilisateur
                        WHERE id IN ({placeholders})""",
                    tuple(uids))
                for r in rows:
                    caissiers[r["id"]] = (r["nom"].strip() or "—")
            except Exception:
                pass

        for it in items:
            it["utilisateur_name"] = caissiers.get(
                it.get("utilisateur_id"), "—")

        return {
            "total": total, "page": page,
            "per_page": per_page, "pages": pages,
            "items": items,
        }
    except Exception as e:
        logger.exception("Erreur list_ventes")
        raise HTTPException(500, f"Erreur : {e}")


# ══════════════════════════════════════════════════════════════════
# GET — Détail d'une facture
# ══════════════════════════════════════════════════════════════════
@router.get("/{num_fact}", response_model=VenteResponse)
def get_vente(num_fact: str):
    """Détail complet d'une facture."""
    try:
        rows = db.query(
            """SELECT Article, Code_reference, Quantite, Prix_uni, Total,
                      Client_name, Caisse, Date_vent, utilisateur_id,
                      COALESCE(annule, 0) AS annule, motif_annulation
               FROM Historique
               WHERE Num_fact = ?
               ORDER BY Id ASC""",
            (num_fact,))

        if not rows:
            raise HTTPException(404, f"Facture '{num_fact}' introuvable")

        lignes = [_row_to_dict(r) for r in rows]
        first = lignes[0]

        # Nom du caissier
        cname = "—"
        if first.get("utilisateur_id"):
            try:
                u = db.query_one(
                    "SELECT COALESCE(prenom,'') || ' ' || COALESCE(nom,'') "
                    "AS nom FROM Utilisateur WHERE id = ? LIMIT 1",
                    (first["utilisateur_id"],))
                if u:
                    cname = u["nom"].strip() or "—"
            except Exception:
                pass

        return {
            "Num_fact": num_fact,
            "Date_vent": first.get("Date_vent") or "",
            "Client_name": first.get("Client_name") or "",
            "Caisse": first.get("Caisse") or "A",
            "utilisateur_id": first.get("utilisateur_id"),
            "utilisateur_name": cname,
            "annule": int(first.get("annule") or 0),
            "motif_annulation": first.get("motif_annulation"),
            "total": sum(float(l["Total"] or 0) for l in lignes),
            "nb_articles": sum(int(l["Quantite"] or 0) for l in lignes),
            "lignes": lignes,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur get_vente")
        raise HTTPException(500, f"Erreur : {e}")


# ══════════════════════════════════════════════════════════════════
# POST — Créer une vente
# ══════════════════════════════════════════════════════════════════
@router.post("", response_model=VenteCreateResponse, status_code=201)
def create_vente(v: VenteCreate, request: Request):
    """Crée une vente (transaction atomique)."""
    user = request.state.user

    # ─── 1. Résoudre le client ───
    client_name_full = "Client anonyme"
    client_numero = ""
    client_id_final = None

    if v.client_id:
        try:
            row = db.query_one(
                "SELECT id, COALESCE(C_name, nom) AS nom, numero "
                "FROM Client WHERE id = ? AND actif = 1 LIMIT 1",
                (v.client_id,))
            if not row:
                raise HTTPException(404, "Client introuvable ou inactif")
            client_name_full = row["nom"]
            client_numero = row["numero"] or ""
            client_id_final = row["id"]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(500, f"Erreur résolution client : {e}")

    elif v.client_numero:
        num = v.client_numero.replace(" ", "").replace("-", "").replace(".", "")
        try:
            row = db.query_one(
                "SELECT id, COALESCE(C_name, nom) AS nom, numero "
                "FROM Client WHERE numero = ? AND actif = 1 LIMIT 1",
                (num,))
            # Variantes
            if not row:
                variantes = []
                if num.startswith("+243") and len(num) == 13:
                    variantes.append("0" + num[4:])
                elif num.startswith("0") and len(num) == 10:
                    variantes.append("+243" + num[1:])
                for var in variantes:
                    row = db.query_one(
                        "SELECT id, COALESCE(C_name, nom) AS nom, numero "
                        "FROM Client WHERE numero = ? AND actif = 1 LIMIT 1",
                        (var,))
                    if row:
                        break
            if row:
                client_name_full = row["nom"]
                client_numero = row["numero"] or ""
                client_id_final = row["id"]
        except Exception:
            logger.exception("Erreur recherche client par numéro")

    # ─── 2. Résoudre les produits + vérifier stock ───
    panier = []
    total_general = 0.0
    nb_articles = 0

    try:
        for l in v.lignes:
            prod = db.query_one(
                """SELECT Code_reference, Nom, Quantite, Prix_unitaire
                   FROM produits WHERE Code_reference = ? AND actif = 1
                   LIMIT 1""",
                (l.code_ref,))
            if not prod:
                raise HTTPException(404, f"Produit '{l.code_ref}' introuvable")

            stock = int(prod["Quantite"] or 0)
            if stock < l.quantite:
                raise HTTPException(
                    400, f"Stock insuffisant pour '{prod['Nom']}' "
                         f"(demandé : {l.quantite}, dispo : {stock})")

            pu = (l.prix_unitaire
                  if l.prix_unitaire is not None
                  else float(prod["Prix_unitaire"] or 0))
            if pu <= 0:
                raise HTTPException(
                    400, f"Prix unitaire invalide pour '{prod['Nom']}'")

            ligne_total = round(pu * l.quantite, 2)
            total_general += ligne_total
            nb_articles += l.quantite

            panier.append({
                "code_ref": prod["Code_reference"],
                "nom": prod["Nom"],
                "qte": l.quantite,
                "pu": pu,
                "total": ligne_total,
                "stock_avant": stock,
            })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Erreur préparation panier : {e}")

    # Applique la remise si présente
    if v.remise > 0:
        total_general = max(0, round(total_general - v.remise, 2))



    # ─── 4. TRANSACTION atomique ───
    try:
        with db.transaction():

            # ─── 3. Génère numéro facture ───
            num_fact, caisse, temoin = _numero_facture()
            if v.caisse:
                caisse = v.caisse

            date_facture = _fmt_date_fr()
            # a) Insère les lignes Historique + décrémente stock
            for item in panier:
                db.execute(
                    """INSERT INTO Historique
                       (Num_fact, Code_reference, Article, Prix_uni,
                        Quantite, Total, Client_name,
                        Caisse, Date_vent, utilisateur_id)
                       VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (num_fact,
                     item["code_ref"], item["nom"],
                     item["pu"], item["qte"], item["total"],
                     f"{client_name_full} {client_numero}".strip(),
                     caisse, date_facture, user["uid"]))

                stock_avant = item["stock_avant"]
                stock_apres = stock_avant - item["qte"]

                db.execute(
                    "UPDATE produits SET Quantite = ? "
                    "WHERE Code_reference = ?",
                    (stock_apres, item["code_ref"]))

                # Vérifie que l'utilisateur existe (FK)
                uid_valide = None
                if user.get("uid"):
                    try:
                        if db.query_one(
                            "SELECT 1 FROM Utilisateur WHERE id = ? LIMIT 1",
                            (user["uid"],)
                        ):
                            uid_valide = user["uid"]
                    except Exception:
                        pass

                db.execute(
                    """INSERT INTO MouvementStock
                       (id, produit_id, type, quantite,
                        stock_avant, stock_apres, motif, utilisateur_id)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (db.new_id(), item["code_ref"], "SORTIE", item["qte"],
                     stock_avant, stock_apres,
                     f"Vente {num_fact}", uid_valide))

            # b) Met à jour Montant_total client si identifié
            if client_id_final:
                row_c = db.query_one(
                    "SELECT Montant_total FROM Client WHERE id = ? LIMIT 1",
                    (client_id_final,))
                ancien = float(row_c["Montant_total"] or 0) if row_c else 0
                db.execute(
                    "UPDATE Client SET Montant_total = ? WHERE id = ?",
                    (ancien + total_general, client_id_final))

            # c) Incrémente le compteur facture
            db.set_config("facture_numero_temoin",
                          temoin + 1, type_="int")

            # d) Audit
            audit.log(
                "CREATION_VENTE",
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="vente", cible_id=num_fact,
                cible_nom=num_fact,
                details={
                    "total": total_general,
                    "nb_articles": nb_articles,
                    "client": client_name_full,
                    "source": "server",
                })

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Échec création vente")
        raise HTTPException(500, f"Impossible d'enregistrer la vente : {e}")

    # ─── Encaissement (si montant_recu fourni) ───
    montant_rendu = 0.0
    devise_rendu = "FC"

    if v.montant_recu is not None and v.montant_recu >= 0:
        try:
            from Database import encaissement
            result = encaissement.compute_rendu(
                montant_facture_fc=total_general,
                devise_paiement=v.devise_paiement or "FC",
                montant_recu=v.montant_recu)

            encaissement.save_encaissement(
                num_fact=num_fact,
                result=result,
                user_id=user.get("uid"),
                user_name=user.get("ident"))

            montant_rendu = result["montant_rendu"]
            devise_rendu = result["devise_rendu"]

            logger.info(
                "Encaissement enregistré : %s → reçu %.2f %s, rendu %.0f %s",
                num_fact, v.montant_recu, v.devise_paiement or "FC",
                montant_rendu, devise_rendu)

        except Exception:
            logger.exception("Erreur encaissement serveur")

    logger.info(
        "Vente créée : %s — %d article(s), total %.0f",
        num_fact, nb_articles, total_general)

    return {
        "status": "ok",
        "Num_fact": num_fact,
        "total": total_general,
        "nb_articles": nb_articles,
        "chemin_pdf": None,
        "montant_rendu": montant_rendu,
        "devise_rendu": devise_rendu,
    }


# ══════════════════════════════════════════════════════════════════
# POST — Annuler une vente
# ══════════════════════════════════════════════════════════════════
@router.post("/{num_fact}/annuler", response_model=SimpleResponse)
def annuler_vente(num_fact: str, req: AnnulationRequest, request: Request):
    """Annule une vente et restitue le stock."""
    user = request.state.user

    # ─── 1. Vérifie que la vente existe et n'est pas déjà annulée ───
    lignes = db.query(
        """SELECT Id, Article, Code_reference, Quantite, Total,
                  Client_name, COALESCE(annule,0) AS annule
           FROM Historique
           WHERE Num_fact = ?""",
        (num_fact,))
    if not lignes:
        raise HTTPException(404, f"Facture '{num_fact}' introuvable")

    if any(int(l["annule"] or 0) == 1 for l in lignes):
        raise HTTPException(400, "Cette vente est déjà annulée")

    total_general = sum(float(l["Total"] or 0) for l in lignes)
    nb_articles = len(lignes)
    first = lignes[0]

    # ─── 2. TRANSACTION ───
    try:
        with db.transaction():
            # a) Marque comme annulée
            db.execute(
                """UPDATE Historique
                   SET annule = 1, motif_annulation = ?
                   WHERE Num_fact = ?""",
                (req.motif, num_fact))

            # b) Restitue le stock
            for l in lignes:
                code_ref = l["Code_reference"]
                if not code_ref:
                    continue

                row_p = db.query_one(
                    "SELECT Quantite FROM produits "
                    "WHERE Code_reference = ? LIMIT 1",
                    (code_ref,))
                if not row_p:
                    continue

                qte = int(l["Quantite"] or 0)
                avant = int(row_p["Quantite"] or 0)
                apres = avant + qte

                db.execute(
                    "UPDATE produits SET Quantite = ? "
                    "WHERE Code_reference = ?",
                    (apres, code_ref))

                uid_valide = None
                if user.get("uid"):
                    try:
                        if db.query_one(
                            "SELECT 1 FROM Utilisateur WHERE id = ? LIMIT 1",
                            (user["uid"],)
                        ):
                            uid_valide = user["uid"]
                    except Exception:
                        pass

                db.execute(
                    """INSERT INTO MouvementStock
                       (id, produit_id, type, quantite,
                        stock_avant, stock_apres, motif, utilisateur_id)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (db.new_id(), code_ref, "ANNULATION", qte,
                     avant, apres,
                     f"Annulation {num_fact} — {req.motif}",
                     uid_valide))

                db.execute(
                    """INSERT INTO AjustementStock
                       (id, Code_reference, Nom_produit,
                        stock_avant, stock_apres, difference,
                        motif, utilisateur_id)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (db.new_id(), code_ref, l["Article"],
                     avant, apres, qte,
                     f"Annulation vente {num_fact}",
                     uid_valide))

            # c) Réduit Montant_total du client si identifié
            client_name = first["Client_name"] or ""
            if client_name and "anonyme" not in client_name.lower():
                parts = client_name.strip().rsplit(" ", 1)
                if len(parts) == 2:
                    num_client = parts[1]
                    try:
                        row_c = db.query_one(
                            "SELECT id, Montant_total FROM Client "
                            "WHERE numero = ? LIMIT 1", (num_client,))
                        if row_c:
                            ancien = float(row_c["Montant_total"] or 0)
                            nouveau = max(0.0, ancien - total_general)
                            db.execute(
                                "UPDATE Client SET Montant_total = ? "
                                "WHERE id = ?",
                                (nouveau, row_c["id"]))
                    except Exception:
                        logger.exception("Erreur maj Montant_total client")

            # d) Audit
            audit.log(
                "ANNULATION_VENTE",
                utilisateur_id=user["uid"],
                utilisateur_name=user["ident"],
                cible_type="vente", cible_id=num_fact,
                cible_nom=num_fact,
                details={
                    "motif": req.motif,
                    "total": total_general,
                    "nb_articles": nb_articles,
                    "source": "server",
                })

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Échec annulation vente")
        raise HTTPException(500, f"Impossible d'annuler : {e}")

    logger.info("Vente annulée : %s — motif : %s", num_fact, req.motif)

    return {
        "status": "ok",
        "message": f"Vente {num_fact} annulée. Stock restitué."
    }


# ══════════════════════════════════════════════════════════════════
# GET — Ventes du jour (raccourci pour le dashboard)
# ══════════════════════════════════════════════════════════════════
@router.get("/stats/jour")
def stats_jour(request: Request):
    """Stats simples des ventes du jour."""
    try:
        today_fr = time.strftime("%d/%m/%Y")
        row = db.query_one(
            """SELECT COUNT(DISTINCT Num_fact) AS n_fact,
                      COALESCE(SUM(Total), 0) AS ca,
                      COALESCE(SUM(Quantite), 0) AS nb_art
               FROM Historique
               WHERE substr(Date_vent, 1, 10) = ?
                 AND COALESCE(annule, 0) = 0""",
            (today_fr,))
        return {
            "date": today_fr,
            "nb_factures": int(row["n_fact"] or 0) if row else 0,
            "ca": float(row["ca"] or 0) if row else 0,
            "nb_articles": int(row["nb_art"] or 0) if row else 0,
        }
    except Exception as e:
        logger.exception("Erreur stats_jour")
        raise HTTPException(500, f"Erreur : {e}")

@router.get("/{num_fact}/encaissement")
def get_encaissement_vente(num_fact: str, request: Request):
    from Database import encaissement
    e = encaissement.get_encaissement(num_fact)
    if not e:
        raise HTTPException(404, "Aucun encaissement pour cette facture")
    return e