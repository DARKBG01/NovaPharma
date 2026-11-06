#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
encaissement.py — Gestion des encaissements (reçu / rendu).
=============================================================
Enregistre et lit les paiements clients.
"""

import logging

from Database import db

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Calcul
# ══════════════════════════════════════════════════════════════════
def compute_rendu(montant_facture_fc: float,
                  devise_paiement: str,
                  montant_recu: float,
                  taux_change: float = None) -> dict:
    """
    Calcule le rendu à donner.

    - Si paiement en FC : rendu en FC
    - Si paiement en USD : rendu en FC (cas le plus courant en RDC)
    """
    try:
        if taux_change is None:
            taux_change = float(db.get_config("taux_change", 2800.0))
        if taux_change <= 0:
            taux_change = 2800.0

        montant_facture_fc = float(montant_facture_fc or 0)
        montant_recu = float(montant_recu or 0)

        if devise_paiement == "USD":
            montant_recu_fc = montant_recu * taux_change
            devise_rendu = "FC"
        else:
            montant_recu_fc = montant_recu
            devise_rendu = "FC"

        diff = montant_recu_fc - montant_facture_fc
        montant_rendu = max(0.0, diff)
        manque = max(0.0, -diff)
        suffisant = diff >= 0

        return {
            "montant_facture_fc": montant_facture_fc,
            "devise_paiement": devise_paiement,
            "taux_change": taux_change,
            "montant_recu": montant_recu,
            "montant_recu_fc": montant_recu_fc,
            "montant_rendu": montant_rendu,
            "devise_rendu": devise_rendu,
            "manque": manque,
            "suffisant": suffisant,
        }
    except Exception:
        logger.exception("Erreur compute_rendu")
        return {
            "montant_facture_fc": 0,
            "devise_paiement": "FC",
            "taux_change": 2800.0,
            "montant_recu": 0,
            "montant_recu_fc": 0,
            "montant_rendu": 0,
            "devise_rendu": "FC",
            "manque": 0,
            "suffisant": False,
        }


# ══════════════════════════════════════════════════════════════════
# Persistance
# ══════════════════════════════════════════════════════════════════
def save_encaissement(num_fact: str, result: dict,
                      user_id: str = None, user_name: str = None,
                      notes: str = None) -> str:
    """Enregistre un encaissement en DB. Retourne l'ID."""
    try:
        eid = db.new_id()
        db.execute("""
            INSERT INTO Encaissement (
                id, num_fact, montant_facture,
                devise_paiement, taux_change,
                montant_recu, montant_recu_fc,
                montant_rendu, devise_rendu,
                utilisateur_id, utilisateur_name, notes
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            eid, num_fact,
            float(result["montant_facture_fc"]),
            result["devise_paiement"],
            float(result["taux_change"]),
            float(result["montant_recu"]),
            float(result["montant_recu_fc"]),
            float(result["montant_rendu"]),
            result["devise_rendu"],
            user_id, user_name, notes))

        # Audit
        try:
            from Database import audit
            audit.log(
                "ENCAISSEMENT",
                utilisateur_id=user_id,
                utilisateur_name=user_name,
                cible_type="vente",
                cible_id=num_fact,
                cible_nom=num_fact,
                details={
                    "montant_facture": result["montant_facture_fc"],
                    "devise_paiement": result["devise_paiement"],
                    "montant_recu": result["montant_recu"],
                    "montant_rendu": result["montant_rendu"],
                    "taux_change": result["taux_change"],
                })
        except Exception:
            logger.exception("Erreur audit encaissement")

        return eid
    except Exception:
        logger.exception("Erreur save_encaissement")
        return None


# ══════════════════════════════════════════════════════════════════
# Lecture
# ══════════════════════════════════════════════════════════════════
def get_encaissement(num_fact: str) -> dict:
    """Retourne l'encaissement d'une facture, ou None."""
    try:
        row = db.query_one(
            "SELECT * FROM Encaissement WHERE num_fact = ? LIMIT 1",
            (num_fact,))
        return dict(row) if row else None
    except Exception:
        logger.exception("Erreur get_encaissement")
        return None


def get_stats_periode(debut: str, fin: str,
                      caisse: str = None) -> dict:
    """
    Retourne les totaux encaissés sur la période.
    Format debut/fin : "YYYY-MM-DD HH:MM:SS"
    """
    try:
        where = ["e.date_encaissement >= ?", "e.date_encaissement <= ?"]
        params = [debut, fin]

        if caisse and caisse != "*":
            where.append("h.Caisse = ?")
            params.append(caisse)

        wc = " AND ".join(where)

        row = db.query_one(
            f"""SELECT
                  COUNT(*) AS nb_encaissements,
                  COALESCE(SUM(e.montant_recu_fc), 0) AS total_recu_fc,
                  COALESCE(SUM(e.montant_rendu), 0) AS total_rendu,
                  COALESCE(SUM(CASE WHEN e.devise_paiement = 'FC'
                                    THEN 1 ELSE 0 END), 0) AS nb_paiements_fc,
                  COALESCE(SUM(CASE WHEN e.devise_paiement = 'USD'
                                    THEN 1 ELSE 0 END), 0) AS nb_paiements_usd,
                  COALESCE(SUM(CASE WHEN e.devise_paiement = 'USD'
                                    THEN e.montant_recu ELSE 0 END), 0)
                                    AS total_recu_usd
                FROM Encaissement e
                LEFT JOIN Historique h ON h.Num_fact = e.num_fact
                WHERE {wc}""",
            tuple(params))

        if not row:
            return _empty_stats()

        return {
            "nb_encaissements": int(row["nb_encaissements"] or 0),
            "total_recu_fc": float(row["total_recu_fc"] or 0),
            "total_rendu": float(row["total_rendu"] or 0),
            "nb_paiements_fc": int(row["nb_paiements_fc"] or 0),
            "nb_paiements_usd": int(row["nb_paiements_usd"] or 0),
            "total_recu_usd": float(row["total_recu_usd"] or 0),
        }
    except Exception:
        logger.exception("Erreur get_stats_periode")
        return _empty_stats()


def _empty_stats() -> dict:
    return {
        "nb_encaissements": 0,
        "total_recu_fc": 0.0,
        "total_rendu": 0.0,
        "nb_paiements_fc": 0,
        "nb_paiements_usd": 0,
        "total_recu_usd": 0.0,
    }