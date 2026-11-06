#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database/backup_crypto.py — Dérivation du mot de passe backup.
================================================================
Le mot de passe des archives ZIP est DÉRIVÉ de l'empreinte machine.
Jamais stocké en clair → impossible de déchiffrer les archives volées
sur une autre machine.

Format du mot de passe : 32 caractères hex + préfixe NOVA- (36 char)
"""

import hashlib
import hmac
import logging

from Database import machine_id

logger = logging.getLogger(__name__)

# Sel constant (change si on change de version de chiffrement)
BACKUP_SALT = b"NovaPharma-Backup-v1"
BACKUP_PREFIX = "NOVA-"


# ══════════════════════════════════════════════════════════════════
def get_backup_password() -> str:
    """
    Retourne le mot de passe dérivé de la machine courante.
    Format : NOVA-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  (37 caractères)
    """
    try:
        mid = machine_id.get_machine_id()
        h = hmac.new(
            key=mid.encode("utf-8"),
            msg=BACKUP_SALT,
            digestmod=hashlib.sha256,
        ).hexdigest()[:32]
        return BACKUP_PREFIX + h.upper()
    except Exception:
        logger.exception("Erreur dérivation mot de passe backup")
        return ""


def get_backup_password_masked() -> str:
    """Retourne un mot de passe masqué pour l'affichage public."""
    pwd = get_backup_password()
    if len(pwd) < 12:
        return "—"
    return f"{pwd[:8]}••••••••••••••••{pwd[-8:]}"


def verify_password(password: str) -> bool:
    """Vérifie que le mot de passe correspond à celui de cette machine."""
    try:
        return password == get_backup_password()
    except Exception:
        return False


def get_backup_password_for_machine_id(mid: str) -> str:
    """Version utilisable avec un machine_id externe (tests)."""
    h = hmac.new(
        key=mid.encode("utf-8"),
        msg=BACKUP_SALT,
        digestmod=hashlib.sha256,
    ).hexdigest()[:32]
    return BACKUP_PREFIX + h.upper()


if __name__ == "__main__":
    print("Machine ID  :", machine_id.get_machine_id())
    print("Short ID    :", machine_id.get_machine_short_id())
    print("Password    :", get_backup_password())
    print("Masked      :", get_backup_password_masked())