#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
system_status.py — État système (disque, réseau, logs).
"""

import logging
import os
import shutil
import socket
from datetime import datetime

from Database import db

logger = logging.getLogger(__name__)


def get_disk_status(path: str = None) -> dict:
    """Retourne l'état du disque pour la DB."""
    try:
        if path is None:
            path = str(db.DB_PATH)
        folder = os.path.dirname(path) or "."

        total, used, free = shutil.disk_usage(folder)
        pct = (used / total * 100) if total else 0

        # Alerte si < 500 Mo ou > 90 %
        alerte = (free < 500 * 1024 * 1024) or (pct > 90)

        return {
            "path": folder,
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
            "used_pct": round(pct, 1),
            "alerte": alerte,
        }
    except Exception:
        logger.exception("Erreur get_disk_status")
        return {}


def get_db_status() -> dict:
    """Taille de la DB + nombre d'entrées par table."""
    try:
        size = os.path.getsize(str(db.DB_PATH)) / (1024 * 1024)

        tables = ["Utilisateur", "produits", "Client", "Historique",
                  "BonLivraison", "Fournisseur", "Encaissement",
                  "AuditLog", "RapportZ", "RetourVente"]

        counts = {}
        for t in tables:
            try:
                row = db.query_one(f"SELECT COUNT(*) AS n FROM {t}")
                counts[t] = int(row["n"] or 0) if row else 0
            except Exception:
                counts[t] = -1

        return {
            "path": str(db.DB_PATH),
            "size_mb": round(size, 2),
            "tables": counts,
        }
    except Exception:
        logger.exception("Erreur get_db_status")
        return {}


def get_network_status(host: str = None, port: int = None) -> dict:
    """Teste la joignabilité du serveur."""
    try:
        if host is None:
            host = db.get_config("server_host", "127.0.0.1")
        if port is None:
            port = int(db.get_config("server_port", 5001))

        start = datetime.now()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        elapsed = (datetime.now() - start).total_seconds() * 1000

        return {
            "host": host,
            "port": port,
            "reachable": result == 0,
            "latency_ms": round(elapsed, 1),
            "error": None if result == 0 else f"Code {result}",
        }
    except Exception as e:
        return {
            "host": host, "port": port,
            "reachable": False, "latency_ms": 0,
            "error": str(e),
        }


def get_logs_status() -> list:
    """Liste les fichiers de logs."""
    try:
        logs = []
        for d in ("logs", "Logs", "."):
            if os.path.isdir(d):
                for f in os.listdir(d):
                    if f.endswith(".log"):
                        p = os.path.join(d, f)
                        try:
                            size = os.path.getsize(p) / 1024
                            mtime = datetime.fromtimestamp(
                                os.path.getmtime(p))
                            logs.append({
                                "path": p,
                                "size_kb": round(size, 1),
                                "modified": mtime.strftime("%d/%m/%Y %H:%M"),
                            })
                        except Exception:
                            pass
        return sorted(logs, key=lambda x: x["modified"], reverse=True)
    except Exception:
        return []