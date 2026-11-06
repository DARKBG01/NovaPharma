#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server_main.py — Serveur Nova Pharma (FastAPI).
=================================================
Lance le serveur REST. Toutes les routes sauf /api/sante et
/api/auth/login nécessitent un token valide.

Usage :
    python -m Server.server_main
    # ou
    python Server/run_server.py
"""

import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from Server import server_db
from Server import server_config as cfg
from Server import server_middlewares as mw
from Server import server_audit_middleware as audit_mw
from Server import server_permissions_middleware as perm_mw
from Server.routes import blf, health, auth, produits, clients, rapports, ventes, sessions, audit as audit_route, retours

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
def create_app() -> FastAPI:
    """Crée l'application FastAPI."""
    app = FastAPI(
        title="Nova Pharma Server",
        version="0.1.0",
        description="API REST pour Nova Pharma — gestion pharmacie",
    )

    # ─── CORS (autorise tous les clients du LAN) ───
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ─── Middlewares (ordre inverse d'exécution) ───
    # Ordre d'exécution réel (du premier au dernier) :
    # 1. horaires  (bloque hors plage)
    # 2. auth      (vérifie token)
    # 3. permissions (vérifie permission granulaire)
    # 4. log       (log technique)
    # 5. audit     (trace consultation / 401 / 403)
    app.middleware("http")(audit_mw.middleware_audit_requests)
    app.middleware("http")(mw.middleware_log)
    app.middleware("http")(perm_mw.middleware_permissions)
    app.middleware("http")(mw.middleware_auth)
    app.middleware("http")(mw.middleware_horaires)

    # ─── Routes ───
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(produits.router)
    app.include_router(clients.router)
    app.include_router(ventes.router)
    app.include_router(blf.router)
    app.include_router(rapports.router)
    app.include_router(audit_route.router)
    app.include_router(retours.router)
    app.include_router(sessions.router)

    # ─── Gestionnaires d'erreurs ───
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.exception("Erreur non gérée sur %s", request.url.path)
        return JSONResponse(
            {"error": "Erreur interne", "detail": str(exc)},
            status_code=500)

    @app.on_event("startup")
    async def on_startup():
        logger.info("═" * 60)
        logger.info("  Nova Pharma Server — Démarrage")
        logger.info("═" * 60)
        server_db.init()

    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("Nova Pharma Server — Arrêt")
        server_db.close()

    return app


app = create_app()