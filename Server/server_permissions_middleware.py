#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server_permissions_middleware.py — Vérifie les permissions granulaires.
========================================================================
Refuse (403) si l'utilisateur n'a pas la permission pour la route.
"""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from Database import db
from Server.server_permissions_map import (
    get_required_permission, is_caissier_allowed,
)

logger = logging.getLogger(__name__)


# Routes publiques (pas de vérification)
PUBLIC_PATHS = {
    "/api/sante",
    "/api/auth/login",
    "/api/auth/logout",
    "/api/auth/me",
    "/api/auth/change-password",
    "/api/auth/validate-machine",   # ← AJOUT
    "/docs",
    "/openapi.json",
    "/redoc",
}


async def middleware_permissions(request: Request, call_next):
    """Vérifie que l'utilisateur a la permission pour cette route."""
    path = request.url.path
    method = request.method.upper()

    # ─── Route publique → passe ───
    if path in PUBLIC_PATHS:
        return await call_next(request)

    # ─── Récupère l'utilisateur ───
    user = getattr(request.state, "user", None)
    if user is None:
        return await call_next(request)  # déjà géré par auth

    # OWNER / DEVELOPER → tout autorisé
    if user.get("own") or user.get("dev"):
        return await call_next(request)

    # ═══ CAISSIER : whitelist stricte ═══
    if (user.get("role") or "").upper() == "CAISSIER":
        if not is_caissier_allowed(method, path):
            logger.warning(
                "CAISSIER bloqué : %s %s",
                method, path)

            # Audit
            try:
                from Database import audit
                audit.log(
                    "ACCES_REFUSE",
                    utilisateur_id=user.get("uid"),
                    utilisateur_name=user.get("ident"),
                    cible_type="api",
                    cible_nom=f"{method} {path}",
                    details={
                        "raison": "caissier_whitelist",
                        "source": "permissions_middleware",
                    },
                    severite="warning")
            except Exception:
                pass

            return JSONResponse(
                {
                    "error": "Accès refusé",
                    "detail": "Cette action n'est pas autorisée pour "
                              "votre rôle (CAISSIER).",
                },
                status_code=403)

    # ─── Permission requise pour cette route ? ───
    required = get_required_permission(method, path)
    if not required:
        # Route non mappée → on laisse passer (à mapper au besoin)
        return await call_next(request)

    # ─── Vérifie la permission en base ───
    user_id = user.get("uid")
    try:
        row = db.query_one(
            "SELECT 1 FROM UtilisateurPermission "
            "WHERE utilisateur_id = ? AND permission_key = ? AND actif = 1 "
            "LIMIT 1",
            (user_id, required))
        if row is not None:
            return await call_next(request)
    except Exception:
        logger.exception("Erreur vérification permission")

    # ─── Refus ───
    logger.warning(
        "Permission refusée : user=%s perm=%s route=%s %s",
        user.get("ident"), required, method, path)

    # Trace l'audit
    try:
        from Database import audit
        audit.log(
            "ACCES_REFUSE",
            utilisateur_id=user_id,
            utilisateur_name=user.get("ident"),
            cible_type="api",
            cible_nom=f"{method} {path}",
            details={
                "permission_manquante": required,
                "role": user.get("role"),
                "source": "permissions_middleware",
            },
            severite="warning")
    except Exception:
        pass

    return JSONResponse(
        {
            "error": "Accès refusé",
            "detail": f"Permission manquante : {required}",
        },
        status_code=403)