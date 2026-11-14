#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/parametres.py — Config globale + infos pharmacie (Phase 2).
===================================================================
Réservé OWNER / DEVELOPER / ADMIN (sauf lecture publique déjà gérée
par /api/config/public).
"""

import logging
import socket
from datetime import datetime

from fastapi import APIRouter, Request, HTTPException
from Database import db, audit

from Server.server_models import (
    ConfigFullResponse, ConfigUpdate,
    PharmacieResponse, PharmacieUpdate,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["parametres"])


# ══════════════════════════════════════════════════════════════════
def _require_admin(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401, "Non authentifié")
    is_privileged = (user.get("own") or user.get("dev")
                     or user.get("role", "").upper() == "ADMIN")
    if not is_privileged:
        raise HTTPException(403, "Réservé aux administrateurs")


# Mapping config → type interne
_CFG_KEYS = {
    "nom_entreprise": "str",
    "adresse_entreprise": "str",
    "telephone_entreprise": "str",
    "devise": "str",
    "taux_change": "float",
    "afficher_dual": "bool",
    "chiffre_affaire_periode": "str",
    "marge_benefice": "float",
    "facture_numero_caisse": "str",
    "max_postes": "int",
    "impression_facture_auto": "bool",
    "qrcode_actif": "bool",
    "mentions_ticket": "json",
    "sauvegarde_auto": "bool",
    "sauvegarde_intervalle_jours": "int",
    "sauvegarde_max_conservees": "int",
    "backup_dir": "str",
    "backup_secondary_enabled": "bool",
    "backup_secondary_dir": "str",
    "pwd_min_length": "int",
    "pwd_expiration_days": "int",
    "pwd_require_digit": "bool",
    "pwd_require_upper": "bool",
    "pwd_require_special": "bool",
    "require_password_critical": "bool",
    "backup_urgence_auto": "bool",
    "seuil_stock": "int",
    "allow_admin_on_client": "bool",
    "printer_auto_print": "bool",
    "printer_auto_print_report": "bool",
    "printer_auto_open": "bool",
}


# ══════════════════════════════════════════════════════════════════
# GET — Toutes les configs admin
# ══════════════════════════════════════════════════════════════════
@router.get("/config/full", response_model=ConfigFullResponse)
def get_full_config(request: Request):
    """Retourne toutes les configs admin (avec valeurs par défaut)."""
    _require_admin(request)

    try:
        data = {}
        for key, typ in _CFG_KEYS.items():
            default = {
                "str": "", "float": 0.0, "bool": False,
                "int": 0, "json": [],
            }[typ]
            try:
                val = db.get_config(key, default)
                data[key] = val
            except Exception:
                data[key] = default

        # Valeurs par défaut pour les champs critiques
        data.setdefault("devise", "FC")
        if not data.get("taux_change"):
            data["taux_change"] = 2250.0
        if not data.get("marge_benefice"):
            data["marge_benefice"] = 30.0
        if not data.get("facture_numero_caisse"):
            data["facture_numero_caisse"] = "01"
        if not data.get("max_postes"):
            data["max_postes"] = 100
        if not data.get("seuil_stock"):
            data["seuil_stock"] = 20
        if not data.get("pwd_min_length"):
            data["pwd_min_length"] = 8
        if not isinstance(data.get("mentions_ticket"), list):
            data["mentions_ticket"] = []

        return data
    except Exception as e:
        logger.exception("Erreur get_full_config")
        raise HTTPException(500, f"Erreur : {e}")


# ══════════════════════════════════════════════════════════════════
# PUT — Sauvegarder config (update partiel)
# ══════════════════════════════════════════════════════════════════
@router.put("/config", response_model=ConfigFullResponse)
def save_config(payload: ConfigUpdate, request: Request):
    """Sauvegarde un ou plusieurs paramètres."""
    _require_admin(request)
    user = request.state.user

    try:
        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            raise HTTPException(400, "Aucun champ à modifier")

        # ─── Validation ───
        if "facture_numero_caisse" in updates:
            import re
            val = (updates["facture_numero_caisse"] or "01").strip()
            if not re.match(r"^\d{1,2}$", val):
                raise HTTPException(
                    400, "Code caisse invalide (1-2 chiffres)")
            updates["facture_numero_caisse"] = val

        if "devise" in updates:
            if updates["devise"] not in ("FC", "CDF", "USD", "EUR"):
                raise HTTPException(400, "Devise invalide")

        # ─── Snapshot avant ───
        avant = {}
        for k in updates:
            try:
                avant[k] = db.get_config(k, None)
            except Exception:
                avant[k] = None

        # ─── Écriture ───
        with db.transaction():
            for key, val in updates.items():
                if key not in _CFG_KEYS:
                    continue
                typ = _CFG_KEYS[key]
                db.set_config(key, val, type_=typ)

            # ─── Taux de change : audit spécial ───
            if "taux_change" in updates:
                try:
                    from Database.currency import set_taux
                    set_taux(
                        float(updates["taux_change"]),
                        user_id=user.get("uid"),
                        user_name=user.get("ident"))
                except Exception:
                    logger.exception("Erreur set_taux")

            # ─── Audit global ───
            audit.log(
                audit.ACTION_MODIF_CONFIG,
                utilisateur_id=user.get("uid"),
                utilisateur_name=user.get("ident"),
                cible_type="Configuration",
                cible_id="system",
                cible_nom="Paramètres système (API)",
                details={
                    "champs_modifies": list(updates.keys()),
                    "source": "api_client",
                },
                avant=avant,
                apres=updates,
                severite="warning")

        logger.info(
            "Config mise à jour via API : %d champ(s)", len(updates))

        # ─── Retour : recharger tout ───
        data = {}
        for key, typ in _CFG_KEYS.items():
            try:
                data[key] = db.get_config(key, None)
            except Exception:
                data[key] = None
        return data

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur save_config")
        raise HTTPException(500, f"Erreur sauvegarde : {e}")


# ══════════════════════════════════════════════════════════════════
# GET — Infos pharmacie
# ══════════════════════════════════════════════════════════════════
@router.get("/pharmacie", response_model=PharmacieResponse)
def get_pharmacie(request: Request):
    """Retourne les infos de la pharmacie."""
    _require_admin(request)

    try:
        row = db.query_one(
            "SELECT nom, type, email, numero, adresse, path_logo, "
            "seuil_stock, marge_benefice "
            "FROM Pharmacie WHERE id = 1 LIMIT 1")
        if not row:
            return {
                "nom": "NOVA PHARMA", "type": "MOYENNE",
                "email": "", "numero": "", "adresse": "",
                "path_logo": None, "seuil_stock": 25,
                "marge_benefice": 30.0,
            }
        return {k: row[k] for k in row.keys()}
    except Exception as e:
        logger.exception("Erreur get_pharmacie")
        raise HTTPException(500, f"Erreur : {e}")


# ══════════════════════════════════════════════════════════════════
# PUT — Modifier pharmacie
# ══════════════════════════════════════════════════════════════════
@router.put("/pharmacie", response_model=PharmacieResponse)
def save_pharmacie(payload: PharmacieUpdate, request: Request):
    """Modifie les infos de la pharmacie."""
    _require_admin(request)
    user = request.state.user

    try:
        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            raise HTTPException(400, "Aucun champ à modifier")

        existing = db.query_one(
            "SELECT * FROM Pharmacie WHERE id = 1 LIMIT 1")

        with db.transaction():
            if existing:
                champs, params = [], []
                for k, v in updates.items():
                    if k in ("seuil_stock", "marge_benefice"):
                        champs.append(f"{k} = ?")
                    else:
                        champs.append(f"{k} = ?")
                    params.append(v)
                params.append(1)
                db.execute(
                    f"UPDATE Pharmacie SET {', '.join(champs)}, "
                    f"updated_at = datetime('now') WHERE id = ?",
                    tuple(params))
            else:
                db.execute(
                    """INSERT INTO Pharmacie
                       (id, nom, type, email, numero, adresse,
                        path_logo, seuil_stock, marge_benefice, actif)
                       VALUES (1,?,?,?,?,?,?,?,?,1)""",
                    (updates.get("nom", "NOVA PHARMA"),
                     updates.get("type", "MOYENNE"),
                     updates.get("email", ""),
                     updates.get("numero", ""),
                     updates.get("adresse", ""),
                     updates.get("path_logo"),
                     updates.get("seuil_stock", 25),
                     updates.get("marge_benefice", 30.0)))

            # Audit
            audit.log(
                audit.ACTION_MODIF_CONFIG,
                utilisateur_id=user.get("uid"),
                utilisateur_name=user.get("ident"),
                cible_type="Pharmacie",
                cible_id="1",
                cible_nom="Infos pharmacie",
                details={"champs_modifies": list(updates.keys())})

        logger.info("Pharmacie mise à jour via API")

        row = db.query_one(
            "SELECT nom, type, email, numero, adresse, path_logo, "
            "seuil_stock, marge_benefice "
            "FROM Pharmacie WHERE id = 1 LIMIT 1")
        return {k: row[k] for k in row.keys()}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur save_pharmacie")
        raise HTTPException(500, f"Erreur : {e}")