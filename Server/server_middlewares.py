#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server_middlewares.py — Middlewares FastAPI.
=============================================
- check_horaires : bloque hors plage configurée
- check_auth     : exige un token valide (sauf routes publiques)
- log_requests   : log toutes les requêtes
"""

import logging
import time
from collections import defaultdict

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from Server import server_config as cfg
from Server import server_auth as auth

logger = logging.getLogger(__name__)

# Stockage en mémoire des requêtes par IP
_rate_limit_store = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 60


# Routes accessibles sans token
PUBLIC_PATHS = {
    "/api/sante",
    "/api/auth/login",
    "/api/auth/logout",
    #"/api/auth/me",
    "/api/auth/validate-machine",   # ← AJOUT (public, avant login)
    "/docs",
    "/openapi.json",
    "/redoc",
}


# ══════════════════════════════════════════════════════════════════
async def middleware_horaires(request: Request, call_next):
    """Bloque si hors plage horaire (sauf /api/sante)."""
    if request.url.path == "/api/sante":
        return await call_next(request)

    if not cfg.horaires_actifs():
        return JSONResponse(
            {
                "error": "Serveur fermé",
                "detail": (
                    f"Le serveur accepte les requêtes uniquement "
                    f"entre {cfg.get('horaires_debut')} et "
                    f"{cfg.get('horaires_fin')}."
                ),
            },
            status_code=503)

    return await call_next(request)


# ══════════════════════════════════════════════════════════════════
async def middleware_auth(request: Request, call_next):
    """Vérifie le token sur toutes les routes sauf publiques."""
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        # Marque comme non-authentifié pour le middleware d'audit
        request.state.user = None
        request.state.auth_failed = "token_missing"
        return JSONResponse(
            {"error": "Token manquant"},
            status_code=401)

    token = auth_header[7:].strip()

    if auth.is_token_blacklisted(token):
        request.state.user = None
        request.state.auth_failed = "token_blacklisted"
        return JSONResponse(
            {"error": "Token révoqué (déconnecté)"},
            status_code=401)

    payload = auth.decode_token(token)
    if payload is None:
        request.state.user = None
        request.state.auth_failed = "token_invalid"
        return JSONResponse(
            {"error": "Token invalide ou expiré"},
            status_code=401)

    # Injecte l'utilisateur dans request.state
    request.state.user = payload
    request.state.auth_failed = None
    return await call_next(request)


# ══════════════════════════════════════════════════════════════════
async def middleware_log(request: Request, call_next):
    """Log simple de chaque requête."""
    start = time.perf_counter()
    response = await call_next(request)
    duration = (time.perf_counter() - start) * 1000

    logger.info(
        "%s %s → %d (%.1f ms)",
        request.method, request.url.path,
        response.status_code, duration)
    return response


# ══════════════════════════════════════════════════════════════════
# Middleware : Rate Limiting (Anti-DoS)
# ══════════════════════════════════════════════════════════════════
async def middleware_rate_limit(request: Request, call_next):
    """Bloque une IP qui fait plus de 60 requêtes par minute."""
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    # Nettoie les requêtes de plus d'une minute
    _rate_limit_store[client_ip] = [
        t for t in _rate_limit_store[client_ip] if now - t < 60
    ]

    if len(_rate_limit_store[client_ip]) >= MAX_REQUESTS_PER_MINUTE:
        logger.warning(f"Rate limit atteint pour IP: {client_ip}")
        return JSONResponse(
            {"error": "Trop de requêtes. Veuillez patienter une minute."},
            status_code=429
        )

    _rate_limit_store[client_ip].append(now)
    return await call_next(request)