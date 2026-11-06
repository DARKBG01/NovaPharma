#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server_audit_middleware.py — Tracing automatique des requêtes.
===============================================================
Trace UNIQUEMENT les actions non couvertes par les routes :
  - Consultations sensibles (prix d'achat, marges, audit, clients)
  - Échecs d'authentification (401)
  - Accès refusés (403)
  - Erreurs serveur (500)

Les actions métier (POST/PUT/DELETE sur ventes, BLF, users, produits)
sont déjà tracées manuellement dans les routes → pas de doublon.
"""

import logging
import re
import time

from fastapi import Request

from Database import audit

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Mapping route → action de consultation
# ══════════════════════════════════════════════════════════════════
CONSULTATION_MAP = {
    # Sensible : consultations de prix d'achat / marges
    re.compile(r"^/api/produits$"):              "CONSULTATION_PRODUITS",
    re.compile(r"^/api/produits/[^/]+$"):        "CONSULTATION_PRODUIT",
    re.compile(r"^/api/rapports/operations$"):   "CONSULTATION_MARGES",
    re.compile(r"^/api/rapports/ventes$"):       "CONSULTATION_RAPPORT_VENTES",
    re.compile(r"^/api/rapports/equipe$"):       "CONSULTATION_RAPPORT_EQUIPE",

    # Audit — très sensible
    re.compile(r"^/api/audit$"):                 "CONSULTATION_AUDIT",
    re.compile(r"^/api/audit/[^/]+$"):           "CONSULTATION_AUDIT_DETAIL",

    # Clients — pour traquer les préparations de fraude
    re.compile(r"^/api/clients/[^/]+$"):         "CONSULTATION_CLIENT",
    re.compile(r"^/api/clients/numero/[^/]+$"):  "CONSULTATION_CLIENT_NUMERO",
}


# Endpoints à NE JAMAIS tracer automatiquement (bruit)
SKIP_PATTERNS = [
    re.compile(r"^/api/sante$"),
    re.compile(r"^/api/auth/login$"),           # tracé manuellement
    re.compile(r"^/api/auth/logout$"),          # tracé manuellement
    re.compile(r"^/api/auth/me$"),              # ping technique
    re.compile(r"^/docs"),
    re.compile(r"^/openapi\.json$"),
    re.compile(r"^/redoc"),
    re.compile(r"^/favicon\.ico$"),
]


def _should_skip(path: str) -> bool:
    return any(p.match(path) for p in SKIP_PATTERNS)


def _resolve_consultation_action(path: str) -> str | None:
    """Retourne l'action de consultation pour une route GET."""
    for pattern, action in CONSULTATION_MAP.items():
        if pattern.match(path):
            return action
    return None


# ══════════════════════════════════════════════════════════════════
# Middleware principal
# ══════════════════════════════════════════════════════════════════
async def middleware_audit_requests(request: Request, call_next):
    """
    Middleware FastAPI : trace automatiquement les requêtes sensibles.
    """
    path = request.url.path
    method = request.method.upper()

    # ─── Skip ───
    if _should_skip(path):
        return await call_next(request)

    # ─── Récupère l'utilisateur (déjà injecté par middleware_auth) ───
    user = getattr(request.state, "user", None)

    # ─── Exécute la requête ───
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as e:
        # Erreur serveur → trace
        _log_server_error(request, user, e)
        raise

    duration_ms = (time.perf_counter() - start) * 1000
    status = response.status_code

    # ─── Décide ce qu'on trace ───
    try:
        if status == 401:
            _log_401(request, user)
        elif status == 403:
            _log_403(request, user)
        elif status == 500:
            _log_500(request, user)
        elif status == 200 and method == "GET":
            # Consultation GET sensible
            _log_consultation(request, user, path)

        # Toujours : marque la requête comme tracée pour éviter les doublons
        request.state.audit_logged = True

    except Exception:
        logger.exception("Erreur middleware audit")

    # Log technique (pour debug serveur)
    logger.info(
        "%s %s → %d (%.1f ms)",
        method, path, status, duration_ms)

    return response


# ══════════════════════════════════════════════════════════════════
# Handlers de log
# ══════════════════════════════════════════════════════════════════
def _log_consultation(request, user, path):
    """Trace une consultation GET sensible."""
    action = _resolve_consultation_action(path)
    if not action:
        return

    # Extraction d'un ID éventuel (dernier segment)
    segments = path.strip("/").split("/")
    cible_id = segments[-1] if segments else None
    if cible_id in ("clients", "produits", "audit", "equipe", "ventes",
                    "operations", "numero"):
        cible_id = None

    audit.log(
        action,
        utilisateur_id=user.get("uid") if user else None,
        utilisateur_name=user.get("ident") if user else None,
        cible_type="api",
        cible_id=cible_id,
        cible_nom=f"{request.method} {path}",
        details={
            "path": path,
            "query": str(request.url.query) if request.url.query else None,
            "source": "server",
        },
        severite="info",
        ip_address=_client_ip(request),
    )


def _log_401(request, user):
    """Trace un échec d'authentification."""
    audit.log(
        audit.ACTION_ECHEC_CONNEXION,
        utilisateur_id=user.get("uid") if user else None,
        utilisateur_name=user.get("ident") if user else "(anonyme)",
        cible_type="api",
        cible_nom=f"{request.method} {request.url.path}",
        details={
            "path": request.url.path,
            "reason": "401_unauthorized",
            "source": "server_middleware",
        },
        severite="warning",
        ip_address=_client_ip(request),
    )


def _log_403(request, user):
    """Trace un accès refusé."""
    audit.log(
        "ACCES_REFUSE",
        utilisateur_id=user.get("uid") if user else None,
        utilisateur_name=user.get("ident") if user else None,
        cible_type="api",
        cible_nom=f"{request.method} {request.url.path}",
        details={
            "path": request.url.path,
            "reason": "403_forbidden",
            "role": user.get("role") if user else None,
            "source": "server_middleware",
        },
        severite="warning",
        ip_address=_client_ip(request),
    )


def _log_500(request, user):
    """Trace une erreur serveur."""
    audit.log(
        "ERREUR_SERVEUR",
        utilisateur_id=user.get("uid") if user else None,
        utilisateur_name=user.get("ident") if user else None,
        cible_type="api",
        cible_nom=f"{request.method} {request.url.path}",
        details={
            "path": request.url.path,
            "reason": "500_internal_error",
            "source": "server_middleware",
        },
        severite="danger",
        ip_address=_client_ip(request),
    )


def _log_server_error(request, user, exc):
    """Trace une exception non gérée."""
    try:
        audit.log(
            "ERREUR_SERVEUR_EXCEPTION",
            utilisateur_id=user.get("uid") if user else None,
            utilisateur_name=user.get("ident") if user else None,
            cible_type="api",
            cible_nom=f"{request.method} {request.url.path}",
            details={
                "path": request.url.path,
                "exception": str(exc),
                "type": type(exc).__name__,
                "source": "server_middleware",
            },
            severite="danger",
            ip_address=_client_ip(request),
        )
    except Exception:
        pass


def _client_ip(request: Request) -> str:
    """IP du client (gère X-Forwarded-For si présent)."""
    try:
        # Si derrière un proxy
        fwd = request.headers.get("X-Forwarded-For")
        if fwd:
            return fwd.split(",")[0].strip()

        # Sinon, IP directe
        if request.client:
            return request.client.host or ""
        return ""
    except Exception:
        return ""