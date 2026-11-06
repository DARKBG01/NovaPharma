#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server_config.py — Configuration du serveur Nova Pharma.
=========================================================
Lit les paramètres depuis la DB + variables d'environnement.
"""

import logging
import os
from datetime import datetime, time

from Database import db

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Config par défaut
# ══════════════════════════════════════════════════════════════════
DEFAULTS = {
    "server_host":              "0.0.0.0",   # écoute sur toutes les interfaces
    "server_port":              5001,
    "server_horaires_actif":    False,        # désactivé par défaut
    "server_horaires_debut":    "07:00",
    "server_horaires_fin":      "22:00",
    "server_token_duree_jours": 365,          # jusqu'au logout (long)
}


# ✅ APRÈS
def get(key: str):
    """
    Retourne une config serveur.
    Les clés sont déjà préfixées 'server_' dans la DB
    (ex: 'server_host', 'server_port').
    """
    try:
        # Empêche le double préfixe si on passe déjà 'server_host'
        db_key = key if key.startswith("server_") else f"server_{key}"
        val = db.get_config(db_key, None)
        if val is None:
            return DEFAULTS.get(key)
        return val
    except Exception:
        return DEFAULTS.get(key)


def set_(key: str, value, type_: str = None):
    """Enregistre une config serveur (préfixe auto)."""
    db_key = key if key.startswith("server_") else f"server_{key}"
    db.set_config(db_key, value, type_=type_)


# ══════════════════════════════════════════════════════════════════
# Plage horaire
# ══════════════════════════════════════════════════════════════════
def _parse_heure(s: str) -> time | None:
    try:
        h, m = s.split(":")
        return time(int(h), int(m))
    except Exception:
        return None


def horaires_actifs() -> bool:
    """Vrai si le serveur accepte les requêtes maintenant."""
    try:
        if not get("horaires_actif"):
            return True

        debut = _parse_heure(get("horaires_debut"))
        fin = _parse_heure(get("horaires_fin"))
        if debut is None or fin is None:
            return True

        now = datetime.now().time()

        if debut <= fin:
            # Plage normale : 07:00 → 22:00
            return debut <= now <= fin
        else:
            # Plage chevauchant minuit : 22:00 → 06:00
            return now >= debut or now <= fin

    except Exception:
        logger.exception("Erreur vérification horaires")
        return True