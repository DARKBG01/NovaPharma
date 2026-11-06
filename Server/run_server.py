#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_server.py — Lanceur du serveur Nova Pharma.
================================================
Point d'entrée unique. Peut être lancé en standalone ou via systemd.
"""

import logging
import sys

import uvicorn

from Server import server_config as cfg


def setup_logging():
    import os
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s : %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/server.log", encoding="utf-8"),
        ],
    )


def main():
    setup_logging()
    logger = logging.getLogger("server")

    host = cfg.get("server_host") or "0.0.0.0"
    port = int(cfg.get("server_port") or 5001)

    logger.info("→ Démarrage du serveur sur %s:%d", host, port)

    uvicorn.run(
        "Server.server_main:app",
        host=host,
        port=port,
        log_level="info",
        reload=False,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServeur arrêté par l'utilisateur.")
        sys.exit(0)