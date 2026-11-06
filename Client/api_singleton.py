#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
api_singleton.py — Point d'accès global à l'API.
=================================================
Fournit un singleton NovaApiClient accessible partout.

Usage :
    from Client.api_singleton import get_api
    api = get_api()
    produits = api.list_produits()
"""

import logging
from typing import Optional

from Client.client_api import NovaApiClient, NovaApiError

logger = logging.getLogger(__name__)

_api: Optional[NovaApiClient] = None
_mode: str = "autonome"   # autonome | serveur | client
_config_cache = {}


# ══════════════════════════════════════════════════════════════════
def init_api(base_url: str = None, mode: str = "client"):
    """Initialise l'API client (appelé au démarrage)."""
    global _api, _mode

    if base_url is None:
        from Database import db
        host = db.get_config("server_host", "127.0.0.1")
        port = int(db.get_config("server_port", 5001))
        base_url = f"http://{host}:{port}"

    _api = NovaApiClient(base_url)
    _mode = mode
    logger.info("API initialisée : %s (mode=%s)", base_url, mode)
    return _api


def get_api() -> Optional[NovaApiClient]:
    """Retourne le client API (None si mode autonome/serveur)."""
    return _api


def get_mode() -> str:
    """Retourne le mode actuel : autonome|serveur|client."""
    return _mode


def is_client_mode() -> bool:
    """Vrai si on est en mode client (utilise l'API)."""
    return _mode == "client" and _api is not None


def reset_api():
    """Réinitialise (utile pour les tests)."""
    global _api, _mode
    _api = None
    _mode = "autonome"




def get_config(key: str, default=None):
    """
    Récupère un paramètre (API si client, DB locale sinon).
    Met en cache pour éviter les appels répétés.
    """
    global _config_cache

    if not is_client_mode():
        from Database import db
        return db.get_config(key, default)

    # Mode client → cache
    if not _config_cache:
        try:
            api = get_api()
            if api is not None:
                _config_cache = api.get_public_config()
        except Exception:
            logger.exception("Erreur get_public_config")

    return _config_cache.get(key, default)


def clear_config_cache():
    """Force le rechargement au prochain appel."""
    global _config_cache
    _config_cache = {}