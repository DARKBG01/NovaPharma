#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database/audit.py — Journal d'audit renforcé.
==============================================
- Snapshot avant/après automatique
- IP + hostname capturés
- Chaîne de hash anti-falsification
- Sévérité par action
- Helper `trace()` : enveloppe complète pour modifications
"""

import hashlib
import json
import logging
import socket
from typing import Any

from Database import db

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Constantes d'actions — Ventes
# ══════════════════════════════════════════════════════════════════
ACTION_CREATION_VENTE         = "CREATION_VENTE"
ACTION_ANNULATION_VENTE       = "ANNULATION_VENTE"
ACTION_REMISE_APPLIQUEE       = "REMISE_APPLIQUEE"
ACTION_REIMPRESSION_FACTURE   = "REIMPRESSION_FACTURE"
ACTION_IMPRESSION_FACTURE     = "IMPRESSION_FACTURE"

# ─── Produits ───
ACTION_CREATION_PRODUIT       = "CREATION_PRODUIT"
ACTION_MODIF_PRODUIT          = "MODIF_PRODUIT"
ACTION_MODIF_PRIX             = "MODIF_PRIX"
ACTION_MODIF_PRIX_ACHAT       = "MODIF_PRIX_ACHAT"
ACTION_SUPPRESSION_PRODUIT    = "SUPPRESSION_PRODUIT"
ACTION_MODIF_STOCK_MANUEL     = "MODIF_STOCK_MANUEL"
ACTION_MOUVEMENT_STOCK        = "MOUVEMENT_STOCK"

# ─── Clients ───
ACTION_CREATION_CLIENT        = "CREATION_CLIENT"
ACTION_MODIF_CLIENT           = "MODIF_CLIENT"
ACTION_MODIF_CLIENT_NUMERO    = "MODIF_CLIENT_NUMERO"
ACTION_SUPPRESSION_CLIENT     = "SUPPRESSION_CLIENT"
ACTION_ACTIVATION_CLIENT      = "ACTIVATION_CLIENT"

# ─── BLF ───
ACTION_CREATION_BLF           = "CREATION_BLF"
ACTION_VALIDATION_BLF         = "VALIDATION_BLF"
ACTION_ANNULATION_BLF         = "ANNULATION_BLF"

# ─── Fournisseurs ───
ACTION_CREATION_FOURNISSEUR   = "CREATION_FOURNISSEUR"
ACTION_MODIF_FOURNISSEUR      = "MODIF_FOURNISSEUR"
ACTION_SUPPRESSION_FOURNISSEUR = "SUPPRESSION_FOURNISSEUR"

# ─── Utilisateurs ───
ACTION_CREATION_USER          = "CREATION_USER"
ACTION_MODIF_INFO_USER        = "MODIF_INFO_USER"
ACTION_MODIF_ROLE_USER        = "MODIF_ROLE_USER"
ACTION_MODIF_PERMISSIONS      = "MODIF_PERMISSIONS"
ACTION_MODIF_MOT_DE_PASSE     = "MODIF_MOT_DE_PASSE"
ACTION_RESET_MOT_DE_PASSE     = "RESET_MOT_DE_PASSE"
ACTION_ACTIVATION_USER        = "ACTIVATION_USER"
ACTION_DESACTIVATION_USER     = "DESACTIVATION_USER"
ACTION_SUPPRESSION_USER       = "SUPPRESSION_USER"
ACTION_PROMOTION_OWNER        = "PROMOTION_OWNER"

# ─── Auth ───
ACTION_CONNEXION              = "CONNEXION"
ACTION_DECONNEXION            = "DECONNEXION"
ACTION_ECHEC_CONNEXION        = "ECHEC_CONNEXION"
ACTION_VERROUILLAGE_COMPTE    = "VERROUILLAGE_COMPTE"

# ─── Système / config ───
ACTION_MODIF_CONFIG           = "MODIF_CONFIG"
ACTION_CONNEXION_DEVELOPER    = "CONNEXION_DEVELOPER"
ACTION_ACCES_MODE_TECHNIQUE   = "ACCES_MODE_TECHNIQUE"
ACTION_BACKUP_CREATION        = "BACKUP_CREATION"
ACTION_BACKUP_SUPPRESSION     = "BACKUP_SUPPRESSION"
ACTION_RESTORE_DATABASE       = "RESTORE_DATABASE"
ACTION_EXPORT_DATABASE        = "EXPORT_DATABASE"

# ─── Consultations sensibles ───
ACTION_CONSULTATION_PRIX_ACHAT = "CONSULTATION_PRIX_ACHAT"
ACTION_CONSULTATION_MARGES    = "CONSULTATION_MARGES"
ACTION_CONSULTATION_AUDIT     = "CONSULTATION_AUDIT"
ACTION_CONSULTATION_CLIENT    = "CONSULTATION_CLIENT"

# ─── Rapports ───
ACTION_EXPORT_RAPPORT         = "EXPORT_RAPPORT"
ACTION_EXPORT_PDF             = "EXPORT_PDF"
ACTION_EXPORT_EXCEL           = "EXPORT_EXCEL"
ACTION_EXPORT_CSV             = "EXPORT_CSV"

# ─── Alertes de sécurité ───
ACTION_ALERTE_FRAUDE          = "ALERTE_FRAUDE"
ACTION_ALERTE_STOCK           = "ALERTE_STOCK"
ACTION_ALERTE_MODIF_SUSPECTE  = "ALERTE_MODIF_SUSPECTE"


# ══════════════════════════════════════════════════════════════════
# Sévérité par action
# ══════════════════════════════════════════════════════════════════
SEVERITE_MAP = {
    # Danger (rouge) — actions sensibles
    ACTION_ANNULATION_VENTE:       "danger",
    ACTION_ANNULATION_BLF:         "danger",
    ACTION_SUPPRESSION_USER:       "danger",
    ACTION_MODIF_PERMISSIONS:      "danger",
    ACTION_MODIF_ROLE_USER:        "danger",
    ACTION_RESET_MOT_DE_PASSE:     "danger",
    ACTION_RESTORE_DATABASE:       "danger",
    ACTION_EXPORT_DATABASE:        "danger",
    ACTION_ACCES_MODE_TECHNIQUE:   "danger",
    ACTION_ECHEC_CONNEXION:        "warning",
    ACTION_ALERTE_FRAUDE:          "danger",
    ACTION_PROMOTION_OWNER:        "danger",

    # Warning (orange) — à surveiller
    ACTION_MODIF_PRIX:             "warning",
    ACTION_MODIF_PRIX_ACHAT:       "warning",
    ACTION_MODIF_STOCK_MANUEL:     "warning",
    ACTION_SUPPRESSION_PRODUIT:    "warning",
    ACTION_SUPPRESSION_CLIENT:     "warning",
    ACTION_MODIF_CONFIG:           "warning",
    ACTION_REMISE_APPLIQUEE:       "warning",
    ACTION_MODIF_CLIENT_NUMERO:    "warning",
    ACTION_DESACTIVATION_USER:     "warning",

    # Info (bleu) — par défaut
}


def _get_severite(action: str) -> str:
    return SEVERITE_MAP.get(action, "info")


# ══════════════════════════════════════════════════════════════════
# Helpers internes
# ══════════════════════════════════════════════════════════════════
def _jsonify(valeur: Any) -> str | None:
    if valeur is None:
        return None
    try:
        return json.dumps(valeur, ensure_ascii=False, default=str)
    except Exception:
        return str(valeur)


def _hostname() -> str:
    try:
        return socket.gethostname()
    except Exception:
        return "unknown"


def _get_local_ip() -> str:
    """IP locale de la machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip
    except Exception:
        return ""


def _get_last_hash() -> str:
    """Retourne le hash de la dernière entrée d'audit."""
    try:
        row = db.query_one(
            "SELECT current_hash FROM AuditLog "
            "WHERE current_hash IS NOT NULL "
            "ORDER BY date_action DESC, rowid DESC LIMIT 1")
        return row["current_hash"] if row else ""
    except Exception:
        return ""


def _compute_hash(prev_hash: str, contenu: str) -> str:
    """Calcule le hash chaîné de l'entrée."""
    try:
        chain = f"{prev_hash}|{contenu}"
        return hashlib.sha256(chain.encode("utf-8")).hexdigest()
    except Exception:
        return ""


# ══════════════════════════════════════════════════════════════════
# Fonction principale — LOG
# ══════════════════════════════════════════════════════════════════
def log(action: str, *,
        utilisateur_id: str | None = None,
        utilisateur_name: str | None = None,
        cible_type: str | None = None,
        cible_id: str | None = None,
        cible_nom: str | None = None,
        details: Any = None,
        avant: Any = None,
        apres: Any = None,
        severite: str | None = None,
        ip_address: str | None = None,
        machine_name: str | None = None) -> str | None:   # ← AJOUT
    """
    Insère une entrée dans AuditLog avec :
    - IP + hostname capturés
    - Hash chaîné anti-falsification
    - Sévérité automatique selon l'action
    """
    try:
        entry_id = db.new_id()

        # IP auto si non fournie
        ip_final = ip_address if ip_address is not None else _get_local_ip()

        # Sévérité auto
        sev_final = severite or _get_severite(action)

        # Hash chaîné
        prev_hash = _get_last_hash()
        details_json = _jsonify(details) or ""
        avant_json = _jsonify(avant) or ""
        apres_json = _jsonify(apres) or ""
        contenu = (
            f"{entry_id}|{action}|{utilisateur_id or ''}|"
            f"{cible_type or ''}|{cible_id or ''}|"
            f"{details_json}|{avant_json}|{apres_json}"
        )
        current_hash = _compute_hash(prev_hash, contenu)

        db.execute(
            """INSERT INTO AuditLog
               (id, action, utilisateur_id, utilisateur_name,
                cible_type, cible_id, cible_nom,
                details, avant, apres, machine_name,
                ip_address, severite, prev_hash, current_hash,
                date_action)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, datetime('now'))""",
            (entry_id, action, utilisateur_id, utilisateur_name,
             cible_type, cible_id, cible_nom,
             details_json, avant_json, apres_json,
             machine_name or _hostname(),  # ← nouveau
             ip_final, sev_final, prev_hash, current_hash))

        return entry_id
    except Exception:
        logger.exception("Échec écriture AuditLog (action=%s)", action)
        return None


# ══════════════════════════════════════════════════════════════════
# SNAPSHOT / DIFF — pour les modifications
# ══════════════════════════════════════════════════════════════════
def snapshot(table: str, id_column: str, id_value) -> dict | None:
    """
    Capture l'état actuel d'une ligne (avant modification).

    Usage :
        avant = audit.snapshot("produits", "Code_reference", "MED-00001")
        # ... modifier
        apres = audit.snapshot("produits", "Code_reference", "MED-00001")
        audit.log("MODIF_PRODUIT", avant=avant, apres=apres, ...)
    """
    try:
        if not table or not id_column:
            return None
        # Sécurité : nom de table/id whitelist basique
        if not table.replace("_", "").isalnum():
            return None
        if not id_column.replace("_", "").isalnum():
            return None

        row = db.query_one(
            f"SELECT * FROM {table} WHERE {id_column} = ? LIMIT 1",
            (id_value,))
        if not row:
            return None

        # Convertit en dict + nettoie les champs sensibles
        d = {}
        for k in row.keys():
            if k in ("pswd_hash",):
                d[k] = "***"
                continue
            v = row[k]
            # Convertit les bytes en str
            if isinstance(v, bytes):
                d[k] = "***"
            else:
                d[k] = v
        return d
    except Exception:
        logger.exception("Erreur snapshot %s/%s", table, id_column)
        return None


def diff(avant: dict | None, apres: dict | None) -> dict:
    """
    Calcule les différences entre 2 états.

    Retourne :
        {
            "champs_modifies": {
                "Prix_vente": {"avant": 2500, "apres": 2800},
                ...
            },
            "champs_ajoutes": [...],
            "champs_supprimes": [...],
        }
    """
    if avant is None or apres is None:
        return {"champs_modifies": {}, "champs_ajoutes": [],
                "champs_supprimes": []}

    try:
        modifies = {}
        for k in set(avant.keys()) | set(apres.keys()):
            a = avant.get(k)
            b = apres.get(k)
            if a != b:
                modifies[k] = {"avant": a, "apres": b}

        ajoutes = [k for k in apres.keys() if k not in avant]
        supprimes = [k for k in avant.keys() if k not in apres]

        return {
            "champs_modifies": modifies,
            "champs_ajoutes": ajoutes,
            "champs_supprimes": supprimes,
        }
    except Exception:
        return {"champs_modifies": {}, "champs_ajoutes": [],
                "champs_supprimes": []}


def trace(action: str, *,
          table: str,
          id_column: str,
          id_value,
          champs_modifies: dict = None,
          utilisateur_id: str = None,
          utilisateur_name: str = None,
          cible_type: str = None,
          cible_nom: str = None,
          details: Any = None) -> str | None:
    """
    Helper haute-niveau : log + diff automatique.

    Usage :
        # Avant modification :
        avant = audit.snapshot("produits", "Code_reference", code)

        # ... faire la modif

        # Après :
        apres = audit.snapshot("produits", "Code_reference", code)
        audit.trace("MODIF_PRODUIT", table="produits",
                    id_column="Code_reference", id_value=code,
                    utilisateur_id=user_id, ...)
    """
    return log(
        action,
        utilisateur_id=utilisateur_id,
        utilisateur_name=utilisateur_name,
        cible_type=cible_type or table,
        cible_id=str(id_value) if id_value else None,
        cible_nom=cible_nom,
        details=details,
        avant=champs_modifies,
    )


def trace_modif(action: str, *,
                table: str,
                id_column: str,
                id_value,
                avant_snapshot: dict,
                utilisateur_id: str = None,
                utilisateur_name: str = None,
                cible_type: str = None,
                cible_nom: str = None,
                details: Any = None) -> str | None:
    """
    Version complète : prend l'`avant` et calcule l'`apres` automatiquement.

    Usage :
        avant = audit.snapshot("produits", "Code_reference", code)
        # ... modifier en DB ...
        audit.trace_modif("MODIF_PRODUIT",
                          table="produits",
                          id_column="Code_reference",
                          id_value=code,
                          avant_snapshot=avant,
                          utilisateur_id=user_id,
                          cible_nom=nom)
    """
    try:
        apres_snapshot = snapshot(table, id_column, id_value)
        d = diff(avant_snapshot, apres_snapshot)

        # Ne log que si quelque chose a changé
        if (not d["champs_modifies"]
                and not d["champs_ajoutes"]
                and not d["champs_supprimes"]):
            return None

        return log(
            action,
            utilisateur_id=utilisateur_id,
            utilisateur_name=utilisateur_name,
            cible_type=cible_type or table,
            cible_id=str(id_value) if id_value else None,
            cible_nom=cible_nom,
            details=details,
            avant=avant_snapshot,
            apres=apres_snapshot,
        )
    except Exception:
        logger.exception("Erreur trace_modif")
        return None


# ══════════════════════════════════════════════════════════════════
# Vérification de la chaîne (anti-falsification)
# ══════════════════════════════════════════════════════════════════
def verify_chain(limit: int = 1000) -> dict:
    """
    Vérifie l'intégrité de la chaîne d'audit.

    Retourne :
        {
            "ok": bool,
            "total_verifie": int,
            "rupture_id": str | None,
            "rupture_index": int | None,
            "message": str
        }
    """
    try:
        rows = db.query(
            """SELECT id, action, utilisateur_id, cible_type, cible_id,
                      details, avant, apres, prev_hash, current_hash,
                      date_action
               FROM AuditLog
               WHERE current_hash IS NOT NULL
               ORDER BY date_action ASC, rowid ASC
               LIMIT ?""",
            (limit,))

        prev = ""
        for idx, r in enumerate(rows):
            entry_id = r["id"]
            contenu = (
                f"{entry_id}|{r['action']}|{r['utilisateur_id'] or ''}|"
                f"{r['cible_type'] or ''}|{r['cible_id'] or ''}|"
                f"{r['details'] or ''}|{r['avant'] or ''}|"
                f"{r['apres'] or ''}"
            )
            expected = _compute_hash(prev, contenu)

            if expected != r["current_hash"]:
                return {
                    "ok": False,
                    "total_verifie": idx,
                    "rupture_id": entry_id,
                    "rupture_index": idx,
                    "message": (
                        f"Chaîne rompue à l'entrée {idx + 1} "
                        f"({entry_id}). Les données d'audit ont été "
                        f"altérées."
                    ),
                }
            prev = r["current_hash"]

        return {
            "ok": True,
            "total_verifie": len(rows),
            "rupture_id": None,
            "rupture_index": None,
            "message": f"Chaîne intègre ({len(rows)} entrées vérifiées).",
        }
    except Exception as e:
        logger.exception("Erreur vérification chaîne")
        return {
            "ok": False,
            "total_verifie": 0,
            "rupture_id": None,
            "rupture_index": None,
            "message": f"Erreur : {e}",
        }


# ══════════════════════════════════════════════════════════════════
# Lecture (page Audit + exports)
# ══════════════════════════════════════════════════════════════════
def query_logs(*, action=None, utilisateur_id=None,
               cible_type=None, cible_id=None,
               severite=None,
               date_debut=None, date_fin=None,
               limit=100, offset=0) -> list[dict]:
    where, params = ["1=1"], []
    if action:        where.append("action = ?");        params.append(action)
    if utilisateur_id:where.append("utilisateur_id = ?");params.append(utilisateur_id)
    if cible_type:    where.append("cible_type = ?");    params.append(cible_type)
    if cible_id:      where.append("cible_id = ?");      params.append(cible_id)
    if severite:      where.append("severite = ?");      params.append(severite)
    if date_debut:    where.append("date_action >= ?");  params.append(date_debut)
    if date_fin:      where.append("date_action <= ?");  params.append(date_fin)
    rows = db.query(
        f"""SELECT * FROM AuditLog WHERE {' AND '.join(where)}
            ORDER BY date_action DESC LIMIT ? OFFSET ?""",
        tuple(params + [limit, offset]))
    return [dict(r) for r in rows]


def count_logs(*, action=None, utilisateur_id=None,
               severite=None) -> int:
    where, params = ["1=1"], []
    if action:        where.append("action = ?");        params.append(action)
    if utilisateur_id:where.append("utilisateur_id = ?");params.append(utilisateur_id)
    if severite:      where.append("severite = ?");      params.append(severite)
    row = db.query_one(
        f"SELECT COUNT(*) AS n FROM AuditLog WHERE {' AND '.join(where)}",
        tuple(params))
    return int(row["n"] or 0) if row else 0