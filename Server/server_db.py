#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server_db.py — Point d'accès DB partagé pour le serveur.
=========================================================
Réutilise Database/db.py pour garantir la cohérence des transactions
et de la config.
"""

import logging

from Database import db  # noqa: F401 — réexporté

logger = logging.getLogger(__name__)


def init():
    """Initialise la connexion DB au démarrage du serveur."""
    try:
        # ─── Crée la connexion ───
        db.get_conn()
        logger.info("DB connectée : %s", db.DB_PATH)

        # ─── Vérifie que les tables essentielles existent ───
        try:
            tables = db.query(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='Utilisateur'")
            if not tables:
                logger.warning(
                    "Table Utilisateur absente → exécution de seed.run()")
                from Database import seed
                seed.run()
            else:
                logger.info("Schéma DB OK")
        except Exception:
            logger.exception("Erreur vérification schéma")

    except Exception:
        logger.exception("Échec init DB")
        raise


def close():
    """Ferme proprement la connexion."""
    try:
        db.close()
        logger.info("DB fermée")
    except Exception:
        logger.exception("Erreur fermeture DB")