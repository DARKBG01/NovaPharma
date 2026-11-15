#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database/machine_id.py — Empreinte machine STABLE.
====================================================
Combine un fichier caché + composants matériels physiques.
Jamais hostname/MAC (instables).
"""

import hashlib
import logging
import os
import platform
import subprocess
import socket
import uuid

logger = logging.getLogger(__name__)

_cache = None

# MAC virtuelles à exclure (VM, Docker, VPN)
VIRTUAL_MAC_PREFIXES = {
    "00:50:56", "00:0c:29", "00:05:69",  # VMware
    "08:00:27", "0a:00:27",  # VirtualBox
    "52:54:00", "02:42",  # QEMU/KVM, Docker
    "00:15:5d", "00:16:3e",  # Hyper-V, Xen
    "00:1c:42",  # Parallels
}


# ══════════════════════════════════════════════════════════════════
# Composants matériels
# ══════════════════════════════════════════════════════════════════
def _safe(fn, default=""):
    try:
        r = fn()
        return str(r) if r else default
    except Exception:
        return default


def _disk_serial_linux():
    try:
        for path in ("/dev/sda", "/dev/nvme0n1", "/dev/vda", "/dev/mmcblk0"):
            if not os.path.exists(path):
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
    s = platform.system()
    if s == "Windows":
        return _disk_serial_windows()
    if s == "Darwin":
        return _disk_serial_mac()
    return _disk_serial_linux()


def _board_serial():
    try:
        for path in ("/sys/class/dmi/id/board_serial",
                     "/sys/class/dmi/id/product_uuid"):
            try:
                with open(path) as f:
                    v = f.read().strip()
                    if v and v.lower() not in ("none", "to be filled",
                                               "unknown", "default string"):
                        return v
            except Exception:
                pass
    except Exception:
        pass
    return ""


def _is_physical_mac(mac: str) -> bool:
    if not mac or len(mac) < 12:
        return False
    mac_lower = mac.lower().replace("-", ":")
    if ":" not in mac_lower and len(mac_lower) >= 12:
        mac_lower = ":".join(mac_lower[i:i + 2] for i in range(0, 12, 2))
    prefix = ":".join(mac_lower.split(":")[:3])
    for virtual in VIRTUAL_MAC_PREFIXES:
        if prefix.startswith(virtual):
            return False
    return True


def _get_physical_mac() -> str:
    """Retourne la première MAC PHYSIQUE (pas VM/VPN)."""
    try:
        node = f"{uuid.getnode():012x}"
        if _is_physical_mac(node):
            return node
    except Exception:
        pass
    return ""


def get_components() -> dict:
    return {
        "hostname": _safe(socket.gethostname),
        "platform": f"{platform.system()}-{platform.release()}",
        "disk_serial": _disk_serial(),
        "board_serial": _board_serial(),
        "physical_mac": _get_physical_mac(),
    }


# ══════════════════════════════════════════════════════════════════
# Fichier caché machine_id
# ══════════════════════════════════════════════════════════════════
def _get_machine_id_file_path() -> str:
    if platform.system() == "Windows":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif platform.system() == "Darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.path.expanduser("~/.config")

    folder = os.path.join(base, "NovaPharma")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, ".machine_id")


def _read_machine_id_file() -> str:
    try:
        path = _get_machine_id_file_path()
        if not os.path.exists(path):
            return ""
        with open(path) as f:
            data = f.read().strip()
        if len(data) == 64 and all(c in "0123456789abcdef" for c in data):
            return data
    except Exception:
        pass
    return ""


def _write_machine_id_file(mid: str):
    try:
        path = _get_machine_id_file_path()
        with open(path, "w") as f:
            f.write(mid)
    except Exception:
        logger.exception("Erreur écriture .machine_id")


# ══════════════════════════════════════════════════════════════════
# API publique
# ══════════════════════════════════════════════════════════════════
def get_machine_id() -> str:
    """
    Retourne un hash SHA-256 STABLE.

    Ordre de priorité :
    1. Fichier caché .machine_id existant (source de vérité)
    2. Reconstruction depuis disk_serial (stable)
    3. Reconstruction depuis board_serial (stable)
    4. Reconstruction depuis MAC physique (stable)
    5. Génération d'un UUID unique (dernier recours)
    """
    global _cache
    if _cache:
        return _cache

    # 1. Fichier caché
    file_id = _read_machine_id_file()
    if file_id:
        _cache = file_id
        logger.info("Machine ID chargé depuis fichier")
        return file_id

    # 2. Composants matériels
    c = get_components()
    seed = ""
    source = ""

    if c["disk_serial"] and len(c["disk_serial"]) > 3:
        seed = f"disk:{c['disk_serial']}"
        source = "disk_serial"
    elif c["board_serial"] and len(c["board_serial"]) > 3:
        seed = f"board:{c['board_serial']}"
        source = "board_serial"
    elif c["physical_mac"]:
        seed = f"mac:{c['physical_mac']}"
        source = "physical_mac"
    else:
        seed = f"uuid:{uuid.uuid4().hex}"
        source = "uuid (généré)"
        logger.warning(
            "Aucun composant matériel stable → UUID unique généré")

    # 3. Hash final
    h = hashlib.sha256(seed.encode()).hexdigest()

    # 4. Persister
    _write_machine_id_file(h)
    _cache = h
    logger.info("Machine ID généré et sauvé (source : %s)", source)
    return h


def get_machine_short_id() -> str:
    mid = get_machine_id()[:16].upper()
    return "-".join([mid[i:i + 4] for i in range(0, 16, 4)])


def get_hostname() -> str:
    return _safe(socket.gethostname, "unknown")


if __name__ == "__main__":
    print("Composants :")
    for k, v in get_components().items():
        print(f"  {k:15} : {v or '(vide)'}")
    print()
    print("Machine ID    :", get_machine_id())
    print("Short ID      :", get_machine_short_id())
    print("Fichier       :", _get_machine_id_file_path())