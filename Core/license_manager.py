#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
license_manager.py — Gestion des licences Nova Pharma (Ed25519).
================================================================
Vérifie les signatures Ed25519 avec la clé publique embarquée.
NE PEUT PAS générer de licences (pas de clé privée ici).

Format licence v2 :
    NOVA2-{mid8}-{type}-{exp8}-{nonce6}-{sig_b64url}

Payload signé (binaire UTF-8) :
    v2|{mid8}|{type}|{exp8}|{nonce6}|{issued_at_iso}
"""
import base64
import hashlib
import hmac
import json
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from Database import db

logger = logging.getLogger(__name__)

APP_DIR = Path(__file__).resolve().parent.parent
PUBLIC_KEY_PATH = APP_DIR / "Core" / "public.pem"

# Configuration essai
TRIAL_DAYS = 30
TRIAL_FILE_MAIN = Path.home() / ".novapharma" / "trial.dat"
TRIAL_FILE_BAK = APP_DIR / "Database" / ".trial.dat"
CLOCK_TOLERANCE_SECONDS = 3600  # 1h de tolérance de recul


# ══════════════════════════════════════════════════════════════════
# Utilitaires base64url
# ══════════════════════════════════════════════════════════════════
def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    pad = "=" * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)

def _build_payload(mid8: str, typ: str, exp8: str,
                   nonce: str, issued_at: str) -> bytes:
    """Payload signé (convention à garder IDENTIQUE dans Master)."""
    return f"v2|{mid8}|{typ}|{exp8}|{nonce}|{issued_at}".encode("utf-8")
# ══════════════════════════════════════════════════════════════════
# Chargement de la clé publique
# ══════════════════════════════════════════════════════════════════
_PUBLIC_KEY_CACHE: Optional[Ed25519PublicKey] = None


def _get_public_key() -> Ed25519PublicKey:
    """Charge la clé publique Ed25519 depuis Core/public.pem."""
    global _PUBLIC_KEY_CACHE
    if _PUBLIC_KEY_CACHE is not None:
        return _PUBLIC_KEY_CACHE

    if not PUBLIC_KEY_PATH.exists():
        raise RuntimeError(
            f"Clé publique absente : {PUBLIC_KEY_PATH}\n"
            "Lance tools/generate_ed25519_keys.py sur le PC Master.")

    pem = PUBLIC_KEY_PATH.read_bytes()
    _PUBLIC_KEY_CACHE = serialization.load_pem_public_key(pem)
    logger.info(
        "Clé publique Ed25519 chargée (fingerprint=%s)",
        hashlib.sha256(pem).hexdigest()[:16])
    return _PUBLIC_KEY_CACHE


# ══════════════════════════════════════════════════════════════════
# Machine ID
# ══════════════════════════════════════════════════════════════════
def _get_mid() -> str:
    """Machine ID complet (SHA-256 hex)."""
    try:
        from Database import machine_id
        return machine_id.get_machine_id()
    except Exception:
        logger.exception("Impossible de lire le Machine ID")
        return "unknown"


def _get_mid8() -> str:
    """8 premiers caractères du Machine ID (identifiant visuel)."""
    return _get_mid()[:8].upper()


# ══════════════════════════════════════════════════════════════════
# Parsing / vérification licence v2
# ══════════════════════════════════════════════════════════════════
def _parse_license(key: str) -> Optional[dict]:
    """Parse NOVA2-{mid8}-{type}-{exp8}-{nonce6}-{issued6}-{sig_b64}."""
    key = key.strip()
    if not key.startswith("NOVA2-"):
        return None

    parts = key.split("-")
    if len(parts) != 7:
        return None

    _, mid8, typ, exp8, nonce6, issued6, sig_b64 = parts
    if len(mid8) != 8 or typ not in ("L", "T"):
        return None
    if typ == "L" and exp8 != "00000000":
        return None
    if typ == "T":
        try:
            datetime.strptime(exp8, "%Y%m%d")
        except ValueError:
            return None
    if len(nonce6) != 6 or len(issued6) != 6:
        return None

    return {
        "mid8": mid8, "type": typ, "exp8": exp8,
        "nonce": nonce6, "issued": issued6,
        "sig_b64": sig_b64,
    }


def _verify_license(key: str) -> tuple[bool, dict, str]:
    """Vérifie une clé de licence v2.1."""
    parsed = _parse_license(key)
    if not parsed:
        return False, {}, "Format de clé invalide"

    # 1. Vérif MID8
    if parsed["mid8"] != _get_mid8():
        return False, {}, (
            f"Clé liée à un autre poste "
            f"(attendu {parsed['mid8']}, actuel {_get_mid8()})")

    # 2. Reconstruit payload
    issued_iso = _issued6_to_iso(parsed["issued"])
    if not issued_iso:
        return False, {}, "Date d'émission invalide"

    payload = _build_payload(
        parsed["mid8"], parsed["type"],
        parsed["exp8"], parsed["nonce"], issued_iso)

    # 3. Vérifie signature
    try:
        sig = _b64url_decode(parsed["sig_b64"])
        if len(sig) != 64:
            return False, {}, "Signature Ed25519 invalide (longueur)"
        _get_public_key().verify(sig, payload)
    except InvalidSignature:
        return False, {}, "Signature cryptographique invalide"
    except Exception as e:
        logger.exception("Erreur vérification Ed25519")
        return False, {}, f"Erreur de vérification : {e}"

    # 4. Vérifie expiration (si temporaire)
    lifetime = parsed["type"] == "L"
    exp_ts = 0
    if not lifetime:
        try:
            exp_dt = datetime.strptime(parsed["exp8"], "%Y%m%d")
            exp_dt = exp_dt.replace(hour=23, minute=59, second=59)
            exp_ts = exp_dt.timestamp()
            if time.time() > exp_ts:
                return False, {}, (
                    f"Licence expirée le "
                    f"{exp_dt.strftime('%d/%m/%Y')}")
        except Exception:
            return False, {}, "Date d'expiration invalide"

    return True, {
        "mid8": parsed["mid8"],
        "type": parsed["type"],
        "lifetime": lifetime,
        "exp8": parsed["exp8"],
        "exp_ts": exp_ts,
        "nonce": parsed["nonce"],
        "issued": parsed["issued"],
    }, "Licence valide"


def _issued6_to_iso(issued6: str) -> str:
    """Convertit YYMMDD → ISO 8601."""
    try:
        dt = datetime.strptime(issued6, "%y%m%d")
        return dt.strftime("%Y-%m-%dT00:00:00")
    except Exception:
        return ""


# ══════════════════════════════════════════════════════════════════
# Persistance licence (DB)
# ══════════════════════════════════════════════════════════════════
def _get_stored_license() -> str:
    """Retourne la licence stockée en DB, ou ''."""
    try:
        return db.get_config("license_key", "") or ""
    except Exception:
        return ""


def save_license(key: str) -> bool:
    """Enregistre une licence en DB (après vérification)."""
    ok, payload, msg = _verify_license(key)
    if not ok:
        logger.warning("save_license refusé : %s", msg)
        return False
    try:
        db.set_config("license_key", key.strip().upper(), type_="str")
        db.set_config("license_type",
                      payload["type"], type_="str")
        db.set_config("license_exp_ts",
                      str(payload["exp_ts"]), type_="str")
        db.set_config("license_issued",
                      payload["issued"], type_="str")
        return True
    except Exception:
        logger.exception("Erreur save_license")
        return False


# ══════════════════════════════════════════════════════════════════
# Essai gratuit (trial) — conservé de l'ancien code
# ══════════════════════════════════════════════════════════════════
def _write_trial(stamp: dict) -> None:
    """Écrit le stamp d'essai dans les 2 emplacements (signé)."""
    payload = json.dumps(stamp, sort_keys=True).encode("utf-8")
    mac = hmac.new(b"trial-v2", payload, hashlib.sha256).digest()
    blob = b"V2" + payload + b"|" + mac

    for path in (TRIAL_FILE_MAIN, TRIAL_FILE_BAK):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
        except Exception:
            logger.exception("Erreur écriture trial %s", path)


def _read_trial() -> Optional[dict]:
    """Lit le stamp d'essai (essaie les 2 emplacements)."""
    for path in (TRIAL_FILE_MAIN, TRIAL_FILE_BAK):
        try:
            if not path.exists():
                continue
            blob = path.read_bytes()
            if not blob.startswith(b"V2"):
                continue
            parts = blob[2:].rsplit(b"|", 1)
            if len(parts) != 2:
                continue
            payload, mac = parts
            expected = hmac.new(
                b"trial-v2", payload, hashlib.sha256).digest()
            if not hmac.compare_digest(mac, expected):
                logger.warning("Trial falsifié : %s", path)
                continue
            return json.loads(payload)
        except Exception:
            continue
    return None


def _init_trial() -> dict:
    """Initialise ou recharge le stamp d'essai."""
    stamp = _read_trial()
    if stamp:
        # Anti-recul d'horloge
        last = stamp.get("last_seen", 0)
        now = time.time()
        if now < last - CLOCK_TOLERANCE_SECONDS:
            logger.error("Recul d'horloge détecté")
            stamp["clock_tampered"] = True
        stamp["last_seen"] = now
        _write_trial(stamp)
        return stamp

    # Première initialisation
    stamp = {
        "start": time.time(),
        "last_seen": time.time(),
        "install_id": hashlib.sha256(
            os.urandom(32)).hexdigest()[:16],
    }
    _write_trial(stamp)
    return stamp


# ══════════════════════════════════════════════════════════════════
# API publique (compatible avec l'ancien code)
# ══════════════════════════════════════════════════════════════════
def get_trial_days_left() -> int:
    """
    Retourne :
      -1 : licence valide (pas d'essai en cours)
      -2 : erreur (horloge falsifiée)
       0 : essai expiré
      >0 : jours restants d'essai
    """
    # 1. Licence valide ?
    stored = _get_stored_license()
    if stored:
        ok, _, _ = _verify_license(stored)
        if ok:
            return -1

    # 2. Essai en cours ?
    stamp = _init_trial()

    if stamp.get("clock_tampered"):
        return -2

    start = stamp.get("start", 0)
    if not start:
        return 0

    elapsed = time.time() - start
    remaining = TRIAL_DAYS * 86400 - elapsed
    if remaining <= 0:
        return 0
    return int(remaining // 86400) + 1


def is_license_valid() -> bool:
    """Raccourci pour savoir si une licence valide est active."""
    stored = _get_stored_license()
    if not stored:
        return False
    ok, _, _ = _verify_license(stored)
    return ok


def reset_trial():
    """⚠️ Réservé aux tests — supprime le stamp d'essai."""
    for path in (TRIAL_FILE_MAIN, TRIAL_FILE_BAK):
        try:
            if path.exists():
                path.unlink()
        except Exception:
            pass


