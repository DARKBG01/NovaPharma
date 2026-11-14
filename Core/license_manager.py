#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
license_manager.py — Gestion de la licence et de l'essai gratuit.
====================================================================
- Essai gratuit de 30 jours au premier lancement
- Blocage à l'expiration
- Vérification de la clé générée par NovaPharma Dev
- Protection contre le recul d'horloge
"""

import os
import json
import hmac
import hashlib
import platform
import base64
import logging
from datetime import datetime, timedelta
import secrets

from Database import db, machine_id

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════
TRIAL_DAYS = 30
MASTER_SECRET = b"NovaPharma-MASTER-2026-DEV-ONLY-CHANGE-ME-3.14159265358979323846"
CLOCK_TOLERANCE_HOURS = 1


# ══════════════════════════════════════════════════════════════════
# Fichier de trial caché (invisible pour l'utilisateur)
# ══════════════════════════════════════════════════════════════════
def _get_trial_file_path() -> str:
    """Retourne le chemin du fichier caché selon l'OS."""
    if platform.system() == "Windows":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif platform.system() == "Darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.path.expanduser("~/.local/share")

    folder = os.path.join(base, "NovaPharma")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, ".sys_cache.dat")


def _sign(data: dict, mid: str) -> str:
    key = MASTER_SECRET + mid.encode()
    payload = json.dumps(data, sort_keys=True).encode()
    return hmac.new(key, payload, hashlib.sha256).hexdigest()

# ══════════════════════════════════════════════════════════════════
# Vérification de la licence stockée
# ══════════════════════════════════════════════════════════════════
def _verify_license(key: str) -> tuple[bool, dict, str]:
    """Vérifie une clé de licence."""
    if not key or not key.startswith("NOVA-"):
        return False, {}, "Format de licence invalide"

    mid = machine_id.get_machine_id()

    try:
        parts = key[5:].split("-")
        if len(parts) != 5:
            return False, {}, "Format de licence invalide"

        mid8, typ, exp8, nonce6, sig = parts

        if typ not in ("L", "T"):
            return False, {}, "Type de licence invalide"

        # Vérifie signature
        payload_to_sign = f"{mid8}|{typ}|{exp8}|{nonce6}".encode()
        expected_sig = hmac.new(
            MASTER_SECRET, payload_to_sign, hashlib.sha256
        ).hexdigest()[:16].upper()

        if not hmac.compare_digest(sig, expected_sig):
            return False, {}, "Signature invalide"

        # Vérifie machine
        mid_hash = hashlib.sha256(mid.encode()).hexdigest().upper()
        if mid_hash[:8] != mid8:
            return False, {}, "Cette licence ne correspond pas à ce PC"

        # Vérifie expiration
        if typ == "T":
            try:
                exp_ts = int(exp8, 16)
            except ValueError:
                return False, {}, "Date d'expiration invalide"
            if exp_ts < datetime.now().timestamp():
                return False, {}, "Licence expirée"
            return True, {
                "lifetime": False,
                "exp": exp_ts,
            }, "Licence valide"

        # À vie
        return True, {"lifetime": True, "exp": 0}, "Licence à vie valide"

    except Exception as e:
        logger.exception("Erreur vérification licence")
        return False, {}, f"Erreur : {e}"


def _get_stored_license() -> str:
    try:
        return db.get_config("license_key", "") or ""
    except Exception:
        return ""


def save_license(key: str) -> bool:
    """Enregistre une clé dans la DB (si elle est valide)."""
    ok, _, _ = _verify_license(key)
    if not ok:
        return False
    try:
        with db.transaction():
            db.set_config("license_key", key, type_="str")
        return True
    except Exception:
        logger.exception("Erreur sauvegarde licence")
        return False


# ══════════════════════════════════════════════════════════════════
# Fichier de trial caché (invisible pour l'utilisateur)
# ══════════════════════════════════════════════════════════════════
def _get_trial_file_path() -> str:
    """Retourne le chemin du fichier caché selon l'OS."""
    if platform.system() == "Windows":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif platform.system() == "Darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.path.expanduser("~/.local/share")

    folder = os.path.join(base, "NovaPharma")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, ".sys_cache.dat")


def _get_trial_backup_path() -> str:
    """2ème emplacement caché (backup redondant) pour détecter falsification."""
    if platform.system() == "Windows":
        base = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
    elif platform.system() == "Darwin":
        base = os.path.expanduser("~/Library/Preferences")
    else:
        base = os.path.expanduser("~/.config")

    folder = os.path.join(base, "NovaPharma")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, ".cache_np")


def _sign(data: dict, mid: str) -> str:
    key = MASTER_SECRET + mid.encode()
    payload = json.dumps(data, sort_keys=True).encode()
    return hmac.new(key, payload, hashlib.sha256).hexdigest()


def _read_trial_from(path: str) -> tuple[dict | None, bool]:
    """
    Lit un fichier trial.
    Returns: (data, is_corrupted)
      - (dict, False) : fichier valide
      - (None, False) : fichier absent (premier lancement)
      - (None, True)  : fichier présent MAIS falsifié (fraude !)
    """
    if not os.path.exists(path):
        return None, False

    try:
        with open(path, "r") as f:
            content = json.load(f)
    except Exception:
        # Fichier existe mais illisible → falsification
        return None, True

    try:
        data = content.get("data")
        sig = content.get("signature")
        if not data or not sig:
            return None, True

        mid = machine_id.get_machine_id()
        expected = _sign(data, mid)
        if not hmac.compare_digest(sig, expected):
            return None, True

        return data, False
    except Exception:
        return None, True


def _write_trial_to(path: str, data: dict):
    mid = machine_id.get_machine_id()
    sig = _sign(data, mid)
    try:
        with open(path, "w") as f:
            json.dump({"data": data, "signature": sig}, f, indent=2)
    except Exception:
        logger.exception(f"Erreur écriture trial : {path}")


def _write_trial(data: dict):
    """Écrit dans les 2 emplacements (principal + backup)."""
    _write_trial_to(_get_trial_file_path(), data)
    _write_trial_to(_get_trial_backup_path(), data)


def _read_trial() -> tuple[dict | None, bool]:
    """
    Lit les 2 fichiers.
    Returns: (data, is_corrupted)
      - (dict, False) : OK
      - (None, False) : premier lancement
      - (None, True)  : FRAUDE détectée
    """
    main_data, main_corrupt = _read_trial_from(_get_trial_file_path())
    backup_data, backup_corrupt = _read_trial_from(_get_trial_backup_path())

    # Cas fraude : un fichier existe mais est falsifié
    if main_corrupt or backup_corrupt:
        logger.warning("⚠️ Fichier de licence falsifié détecté !")
        return None, True

    # Cas premier lancement : aucun des 2 n'existe
    if main_data is None and backup_data is None:
        return None, False

    # Cas restauration : un des 2 manque (utilisateur a supprimé)
    # → On restaure depuis celui qui existe
    if main_data is None and backup_data is not None:
        logger.warning("Fichier trial principal absent → restauration depuis backup")
        _write_trial_to(_get_trial_file_path(), backup_data)
        return backup_data, False

    if backup_data is None and main_data is not None:
        logger.warning("Fichier trial backup absent → restauration depuis principal")
        _write_trial_to(_get_trial_backup_path(), main_data)
        return main_data, False

    # Les 2 existent : on prend le plus restrictif (install_date le plus ancien)
    # pour éviter que l'utilisateur modifie un seul des 2
    try:
        install_main = datetime.fromisoformat(main_data["install_date"])
        install_backup = datetime.fromisoformat(backup_data["install_date"])

        # Prend la date la plus ancienne (= plus de jours écoulés = plus stricte)
        if install_backup < install_main:
            logger.warning(
                "Dates incohérentes → utilisation du backup (plus restrictif)")
            _write_trial_to(_get_trial_file_path(), backup_data)
            return backup_data, False
        else:
            # Synchro le backup avec le principal
            _write_trial_to(_get_trial_backup_path(), main_data)
            return main_data, False
    except Exception:
        return None, True


# ══════════════════════════════════════════════════════════════════
# Point d'entrée principal (version renforcée)
# ══════════════════════════════════════════════════════════════════
def check_license_and_trial() -> tuple[bool, int, str]:
    """
    Vérifie l'état de la licence / essai.
    Returns: (ok, days_left, message)
      - ok=True, days_left>0 : essai en cours
      - ok=True, days_left=-1 : licence valide (illimité)
      - ok=False : blocage (trial expiré / horloge suspecte / FRAUDE)
    """
    mid = machine_id.get_machine_id()

    # ═══ 1. Mode test (DEV uniquement) ═══
    try:
        if db.get_config("trial_force_expired", False):
            return False, 0, (
                "MODE TEST : L'essai a été forcé comme expiré.\n\n"
                "Désactivez 'trial_force_expired' dans la DB "
                "pour revenir à la normale."
            )
        if db.get_config("trial_force_corrupted", False):
            return False, 0, (
                "⚠️ Le fichier de licence a été falsifié ou est corrompu.\n\n"
                "Contactez TEAM NOVA pour régulariser votre situation."
            )
    except Exception:
        pass

    # ═══ 2. Licence enregistrée ? ═══
    stored = _get_stored_license()
    if stored:
        ok, payload, msg = _verify_license(stored)
        if ok:
            return True, -1, "Licence valide"

    # ═══ 3. Vérification du trial ═══
    trial, is_corrupted = _read_trial()

    # ═══ 4. FRAUDE DÉTECTÉE ═══
    if is_corrupted:
        logger.warning("⚠️ Falsification du fichier trial détectée")
        return False, 0, (
            "⚠️ Le fichier de licence a été modifié ou est corrompu.\n\n"
            "Si vous pensez qu'il s'agit d'une erreur, "
            "contactez TEAM NOVA pour régulariser votre situation.\n\n"
            "Email : teamnovaoff@gmail.com\n"
            "WhatsApp : +243 808 775 085"
        )

    now = datetime.now()

    # ═══ 5. Premier lancement ═══
    if trial is None:
        _write_trial({
            "install_date": now.isoformat(),
            "last_run": now.isoformat(),
            "machine_id": mid[:32],
        })
        logger.info(f"Essai démarré : {TRIAL_DAYS} jours")
        return True, TRIAL_DAYS, f"Essai de {TRIAL_DAYS} jours démarré"

    # ═══ 6. Protection anti-recul d'horloge ═══
    try:
        last_run = datetime.fromisoformat(trial["last_run"])
    except Exception:
        return False, 0, (
            "Le fichier de licence est corrompu.\n\n"
            "Contactez TEAM NOVA."
        )

    if now < last_run - timedelta(hours=CLOCK_TOLERANCE_HOURS):
        return False, 0, (
            "⚠ L'heure de votre système a été reculée.\n\n"
            "Veuillez corriger la date et l'heure de votre PC "
            "dans les paramètres système, puis relancez Nova Pharma.\n\n"
            "Si le problème persiste, contactez TEAM NOVA."
        )

    # Met à jour last_run
    trial["last_run"] = now.isoformat()
    _write_trial(trial)

    # ═══ 7. Calcul des jours restants ═══
    try:
        install = datetime.fromisoformat(trial["install_date"])
    except Exception:
        return False, 0, "Fichier de licence corrompu. Contactez TEAM NOVA."

    elapsed = (now - install).days
    remaining = TRIAL_DAYS - elapsed

    if remaining > 0:
        return True, remaining, f"Essai : {remaining} jour(s) restant(s)"

    return False, 0, (
        f"Votre période d'essai de {TRIAL_DAYS} jours est terminée.\n\n"
        "Veuillez saisir votre clé de licence pour continuer à "
        "utiliser Nova Pharma."
    )


# ══════════════════════════════════════════════════════════════════
# Helper pour l'UI : nombre de jours restants
# ══════════════════════════════════════════════════════════════════
def get_trial_days_left() -> int:
    """
    Retourne le nombre de jours restants d'essai.
    -1 si licence valide (illimité)
    0 si essai expiré
    -2 si erreur (horloge / fichier corrompu)
    """
    try:
        ok, days, _ = check_license_and_trial()
        if ok:
            return days
        # Vérifier si c'est une licence valide malgré tout
        stored = _get_stored_license()
        if stored:
            v_ok, _, _ = _verify_license(stored)
            if v_ok:
                return -1
        return 0
    except Exception:
        return -2