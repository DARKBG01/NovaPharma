#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database/server_manager.py — Gestion des appareils serveur (remplace devices.json).
===================================================================================
Utilise la table Configuration pour persister la liste des appareils.
"""

import json
import logging
import socket

from Database import db

logger = logging.getLogger(__name__)

CONFIG_KEY = "server_devices"


# ══════════════════════════════════════════════════════════════════
def get_my_ip() -> str:
    """Retourne l'IP locale de la machine."""
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


def list_devices() -> dict:
    """Retourne {device_id: {"host": ..., "ip": ..., "port": ...}}."""
    try:
        data = db.get_config(CONFIG_KEY, {})
        return data if isinstance(data, dict) else {}
    except Exception:
        logger.exception("Erreur lecture devices")
        return {}


def register_device(host: str, device_id: str, ip: str = "",
                    port: int = 5000) -> None:
    """Ajoute / met à jour un appareil."""
    try:
        devices = list_devices()
        devices[device_id] = {
            "host": host,
            "ip": ip or get_my_ip(),
            "port": port,
        }
        db.set_config(CONFIG_KEY, devices, type_="json")
        logger.info("Appareil enregistré : %s (%s)", host, ip)
    except Exception:
        logger.exception("Erreur enregistrement appareil")


def remove_device(device_id: str) -> None:
    """Supprime un appareil."""
    try:
        devices = list_devices()
        devices.pop(device_id, None)
        db.set_config(CONFIG_KEY, devices, type_="json")
    except Exception:
        logger.exception("Erreur suppression appareil")


def clear_devices() -> None:
    """Vide la liste des appareils."""
    db.set_config(CONFIG_KEY, {}, type_="json")