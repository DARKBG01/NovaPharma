#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database/machine_id.py — Empreinte matérielle unique par machine.
=================================================================
Combine plusieurs identifiants matériels pour générer un ID stable
mais tolérant aux changements mineurs (RAM, USB, etc.).

Usage :
    from Database import machine_id
    mid = machine_id.get_machine_id()          # hash 64 char
    short = machine_id.get_machine_short_id()  # XXXX-XXXX-XXXX-XXXX
"""

import hashlib
import logging
import platform
import socket
import subprocess
import uuid

logger = logging.getLogger(__name__)

_cache = None


# ══════════════════════════════════════════════════════════════════
def _safe(callable_, default=""):
    try:
        r = callable_()
        return str(r) if r else default
    except Exception:
        return default


def _hostname():
    return _safe(socket.gethostname)


def _platform_info():
    return f"{platform.system()}-{platform.release()}-{platform.machine()}"


def _mac_address():
    """MAC de la 1ère interface non-loopback."""
    try:
        return f"{uuid.getnode():012x}"
    except Exception:
        return ""


def _cpu_info():
    return f"{_safe(platform.processor)}-{platform.machine()}"


def _disk_serial_linux():
    """Numéro de série du disque principal (Linux)."""
    try:
        for path in ("/dev/sda", "/dev/nvme0n1", "/dev/vda"):
            if not __import__("os").path.exists(path):
                continue
            r = subprocess.run(
                ["lsblk", "-no", "SERIAL", path],
                capture_output=True, text=True, timeout=2)
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip()
    except Exception:
        pass
    return ""


def _disk_serial_windows():
    try:
        r = subprocess.run(
            ["wmic", "diskdrive", "get", "serialnumber"],
            capture_output=True, text=True, timeout=3)
        if r.returncode == 0:
            lines = [l.strip() for l in r.stdout.splitlines()
                     if l.strip() and l.strip().lower() != "serialnumber"]
            return lines[0] if lines else ""
    except Exception:
        pass
    return ""


def _disk_serial_mac():
    try:
        r = subprocess.run(
            ["system_profiler", "SPStorageDataType"],
            capture_output=True, text=True, timeout=3)
        for line in r.stdout.splitlines():
            if "Volume UUID" in line:
                return line.split(":")[-1].strip()
    except Exception:
        pass
    return ""


def _disk_serial():
    sysname = platform.system()
    if sysname == "Windows":
        return _disk_serial_windows()
    if sysname == "Darwin":
        return _disk_serial_mac()
    return _disk_serial_linux()


def _board_serial():
    """Numéro de série de la carte mère (Linux)."""
    try:
        for path in ("/sys/class/dmi/id/board_serial",
                     "/sys/class/dmi/id/product_uuid"):
            try:
                with open(path, "r") as f:
                    v = f.read().strip()
                    if v and v.lower() not in ("none", "to be filled"):
                        return v
            except Exception:
                pass
    except Exception:
        pass
    return ""


# ══════════════════════════════════════════════════════════════════
# API publique
# ══════════════════════════════════════════════════════════════════
def get_components() -> dict:
    """Retourne les composants utilisés pour l'empreinte."""
    return {
        "hostname":    _hostname(),
        "platform":    _platform_info(),
        "mac":         _mac_address(),
        "cpu":         _cpu_info(),
        "disk_serial": _disk_serial(),
        "board_serial": _board_serial(),
    }


def get_machine_id() -> str:
    """
    Retourne un hash SHA-256 hex (64 caractères) stable pour cette machine.
    Combinaison pondérée : on garde hostname + MAC + disk_serial + board_serial.
    """
    global _cache
    if _cache:
        return _cache

    c = get_components()
    # On garde les composants assez stables pour ne pas casser sur
    # un changement mineur (RAM, USB, IP).
    combined = "|".join([
        c["hostname"],
        c["mac"],
        c["disk_serial"],
        c["board_serial"],
    ])
    h = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    _cache = h
    return h


def get_machine_short_id() -> str:
    """Retourne XXXX-XXXX-XXXX-XXXX (pour affichage)."""
    mid = get_machine_id()[:16].upper()
    return "-".join([mid[i:i+4] for i in range(0, 16, 4)])


if __name__ == "__main__":
    print("Composants :")
    for k, v in get_components().items():
        print(f"  {k:15} : {v or '(vide)'}")
    print()
    print("Machine ID    :", get_machine_id())
    print("Short ID      :", get_machine_short_id())