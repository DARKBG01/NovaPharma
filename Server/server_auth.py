#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server_auth.py — Authentification token HMAC.
==============================================
Pas de JWT externe : token signé avec HMAC-SHA256 + sel unique.
Clé = Configuration.unique_key (déjà en DB).
"""

import base64
import hashlib
import hmac
import json
import logging
import time
from typing import Optional

import bcrypt
from Database import db

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
def _get_secret() -> bytes:
    """Récupère la clé HMAC depuis la DB."""
    key = db.get_config("unique_key", "")
    if not key:
        raise RuntimeError("unique_key absente de la Configuration")
    return str(key).encode("utf-8")


# ══════════════════════════════════════════════════════════════════
def verify_login(identifiant: str, password: str) -> Optional[dict]:
    """
    Vérifie les identifiants.
    Retourne un dict utilisateur { id, role, identifiant, is_owner,
    is_developer } ou None.
    """
    try:
        row = db.query_one(
            """SELECT id, identifiant, email, role, pswd_hash, actif,
                      is_owner, is_developer, must_change_password
               FROM Utilisateur
               WHERE LOWER(identifiant) = ? OR LOWER(email) = ?
               LIMIT 1""",
            (identifiant.lower(), identifiant.lower()))
        if row is None:
            return None

        user = dict(row)
        if not user["actif"]:
            return None

        try:
            ok = bcrypt.checkpw(
                password.encode("utf-8"),
                user["pswd_hash"].encode("utf-8"))
        except Exception:
            return None

        if not ok:
            return None

        return {
            "id": user["id"],
            "identifiant": user["identifiant"],
            "email": user["email"],
            "role": user["role"],
            "is_owner": bool(user["is_owner"]),
            "is_developer": bool(user["is_developer"]),
            "must_change_password": bool(user["must_change_password"]),  # ← AJOUT
        }
    except Exception:
        logger.exception("Erreur verify_login")
        return None


# ══════════════════════════════════════════════════════════════════
def create_token(user: dict, duree_jours: int = 365) -> str:
    """Crée un token signé pour un utilisateur."""
    now = int(time.time())
    payload = {
        "uid": user["id"],
        "ident": user["identifiant"],
        "role": user["role"],
        "own": int(user["is_owner"]),
        "dev": int(user["is_developer"]),
        "iat": now,
        "exp": now + duree_jours * 86400,
    }
    payload_json = json.dumps(payload, separators=(",", ":"))
    payload_b64 = base64.urlsafe_b64encode(
        payload_json.encode("utf-8")).decode("ascii").rstrip("=")

    signature = hmac.new(
        _get_secret(),
        payload_b64.encode("ascii"),
        hashlib.sha256
    ).hexdigest()

    return f"{payload_b64}.{signature}"


def decode_token(token: str) -> Optional[dict]:
    """Décode et vérifie un token. Retourne le payload ou None."""
    if not token or "." not in token:
        return None

    try:
        payload_b64, signature = token.split(".", 1)

        expected_sig = hmac.new(
            _get_secret(),
            payload_b64.encode("ascii"),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_sig):
            return None

        # Pad base64
        padding = "=" * (-len(payload_b64) % 4)
        payload_json = base64.urlsafe_b64decode(
            (payload_b64 + padding).encode("ascii")).decode("utf-8")
        payload = json.loads(payload_json)

        if payload.get("exp", 0) < int(time.time()):
            return None

        return payload
    except Exception:
        logger.exception("Erreur decode_token")
        return None


# ══════════════════════════════════════════════════════════════════
def invalidate_token(token: str) -> bool:
    """
    Invalide un token (logout).
    Ajoute son hash dans une blacklist en DB.
    """
    try:
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()

        # Stocke dans Configuration sous clé JSON
        blacklist = db.get_config("server_token_blacklist", [])
        if not isinstance(blacklist, list):
            blacklist = []

        if token_hash not in blacklist:
            blacklist.append(token_hash)
            # Garde les 500 derniers
            blacklist = blacklist[-500:]
            db.set_config("server_token_blacklist", blacklist,
                          type_="json")

        return True
    except Exception:
        logger.exception("Erreur invalidate_token")
        return False


def is_token_blacklisted(token: str) -> bool:
    """Vrai si le token a été invalidé."""
    try:
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        blacklist = db.get_config("server_token_blacklist", [])
        return token_hash in blacklist if isinstance(blacklist, list) else False
    except Exception:
        return False