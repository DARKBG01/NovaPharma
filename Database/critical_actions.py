#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
critical_actions.py — Garde-fou pour actions critiques.
========================================================
Demande mot de passe + backup urgence si activés.
"""

import logging

import bcrypt
from PySide6 import QtWidgets

from Database import db, backup_engine

logger = logging.getLogger(__name__)


def require_password_and_backup(parent, user_id, action_label: str) -> bool:
    """
    Vérifie si mot de passe requis + backup urgence.
    Retourne True si action autorisée.
    """
    try:
        # ─── 1. Mot de passe requis ? ───
        require_pwd = bool(
            db.get_config("require_password_critical", False))

        if require_pwd:
            if not _ask_password(parent, user_id):
                logger.warning(
                    "Action critique refusée : mot de passe invalide")
                return False

        # ─── 2. Backup urgence automatique ? ───
        backup_auto = bool(
            db.get_config("backup_urgence_auto", True))

        if backup_auto:
            try:
                path = backup_engine.create_backup(
                    "PRE_MIGRATION",
                    user_id=user_id,
                    user_name=f"Urgence : {action_label}")
                if path:
                    logger.info(
                        "✅ Backup urgence créée : %s (action: %s)",
                        path, action_label)
                else:
                    QtWidgets.QMessageBox.warning(
                        parent, "Sauvegarde impossible",
                        "Impossible de créer la sauvegarde d'urgence.\n\n"
                        "Voulez-vous continuer quand même ?")
            except Exception:
                logger.exception("Erreur backup urgence")

        return True
    except Exception:
        logger.exception("Erreur require_password_and_backup")
        return False


def _ask_password(parent, user_id) -> bool:
    """Demande le mot de passe utilisateur et vérifie."""
    pwd, ok = QtWidgets.QInputDialog.getText(
        parent, "Confirmation requise",
        "Cette action est critique.\n\n"
        "Saisissez votre mot de passe pour confirmer :",
        QtWidgets.QLineEdit.Password, "")

    if not ok or not pwd:
        return False

    try:
        row = db.query_one(
            "SELECT pswd_hash FROM Utilisateur WHERE id = ? LIMIT 1",
            (user_id,))
        if not row:
            return False

        return bcrypt.checkpw(
            pwd.encode("utf-8"),
            row["pswd_hash"].encode("utf-8"))
    except Exception:
        logger.exception("Erreur vérification mot de passe")
        return False