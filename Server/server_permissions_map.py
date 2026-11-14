#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server_permissions_map.py — Permissions requises par route.
=============================================================
Mappe chaque endpoint à la permission granulaire nécessaire.
Le middleware refuse (403) si l'utilisateur n'a pas la permission.
"""

import re

# ══════════════════════════════════════════════════════════════════
# Mapping (méthode, pattern) → permission requise
# ══════════════════════════════════════════════════════════════════
ROUTES_PERMISSIONS = [
    # ─── PRODUITS ───
    ("GET",    r"^/api/produits$",                    "voir_produits"),
    ("GET",    r"^/api/produits/[^/]+$",              "voir_produits"),
    ("POST",   r"^/api/produits$",                    "ajouter_produit"),
    ("PUT",    r"^/api/produits/[^/]+$",              "modifier_produit"),
    ("DELETE", r"^/api/produits/[^/]+$",              "supprimer_produit"),
    ("POST",   r"^/api/produits/[^/]+/stock$",        "modifier_stock"),

    # ─── CLIENTS ───
    ("GET",    r"^/api/clients$",                     "voir_clients"),
    ("GET",    r"^/api/clients/[^/]+$",               "voir_clients"),
    ("GET",    r"^/api/clients/numero/[^/]+$",        "voir_clients"),
    ("POST",   r"^/api/clients$",                     "ajouter_client"),
    ("PUT",    r"^/api/clients/[^/]+$",               "modifier_client"),
    ("DELETE", r"^/api/clients/[^/]+$",               "supprimer_client"),
    ("POST",   r"^/api/clients/[^/]+/reactiver$",     "modifier_client"),

    # ─── VENTES ───
    ("POST",   r"^/api/ventes$",                      "faire_vente"),
    ("GET",    r"^/api/ventes$",                      "voir_historique_ventes"),
    ("GET",    r"^/api/ventes/[^/]+$",                "voir_historique_ventes"),
    ("POST",   r"^/api/ventes/[^/]+/annuler$",        "annuler_vente"),
    ("GET",    r"^/api/ventes/stats/jour$",           "voir_stats_ca"),

    # ─── BLF ───
    ("GET",    r"^/api/blf$",                         "voir_blf"),
    ("GET",    r"^/api/blf/[^/]+$",                   "voir_blf"),
    ("POST",   r"^/api/blf$",                         "creer_blf"),
    ("POST",   r"^/api/blf/[^/]+/valider$",           "valider_blf"),
    ("POST",   r"^/api/blf/[^/]+/annuler$",           "annuler_blf"),
    ("DELETE", r"^/api/blf/[^/]+$",                   "annuler_blf"),

    # ─── RAPPORTS ───
    ("GET", r"^/api/rapports/ventes$", "voir_rapport_ventes"),
    ("GET", r"^/api/rapports/equipe$", "voir_rapport_equipe"),
    ("GET", r"^/api/rapports/operations$", "voir_rapport_operations"),
    ("GET", r"^/api/rapports/z/preview$", "voir_rapport_ventes"),
    ("POST", r"^/api/rapports/z$", "voir_rapport_ventes"),  # ← AJOUT

    # ─── AUDIT ───
    ("GET", r"^/api/audit.*$", "voir_audit_log"),

    # ─── RETOURS ───
    ("GET",  r"^/api/retours$",              "voir_historique_ventes"),
    ("GET",  r"^/api/retours/[^/]+$",        "voir_historique_ventes"),
    ("POST", r"^/api/retours$",              "annuler_vente"),

    # ─── MONITORING (OWNER/DEV uniquement) ───
    ("GET", r"^/api/monitoring/machines$", "configurer"),

    # ─── UTILISATEURS (Phase 2) ───
    ("GET", r"^/api/users$", "voir_utilisateurs"),
    ("GET", r"^/api/users/[^/]+$", "voir_utilisateurs"),
    ("POST", r"^/api/users$", "ajouter_user"),
    ("PUT", r"^/api/users/[^/]+$", "modifier_user"),
    ("POST", r"^/api/users/[^/]+/reset-password$", "modifier_user"),
    ("DELETE", r"^/api/users/[^/]+$", "desactiver_user"),

    # ─── PARAMÈTRES / CONFIG (Phase 2) ───
    ("GET", r"^/api/config/full$", "configurer"),
    ("PUT", r"^/api/config$", "configurer"),
    ("GET", r"^/api/pharmacie$", "configurer"),
    ("PUT", r"^/api/pharmacie$", "configurer"),

    # ─── FOURNISSEURS (Phase 2) ───
    ("GET", r"^/api/fournisseurs$", "voir_fournisseurs"),
    ("GET", r"^/api/fournisseurs/[^/]+$", "voir_fournisseurs"),
    ("POST", r"^/api/fournisseurs$", "ajouter_fournisseur"),
    ("PUT", r"^/api/fournisseurs/[^/]+$", "modifier_fournisseur"),

    # ─── CATÉGORIES (Phase 2) ───
    ("GET", r"^/api/categories$", "voir_produits"),
    ("POST", r"^/api/categories$", "ajouter_produit"),
    ("PUT", r"^/api/categories/[^/]+$", "modifier_produit"),
    ("DELETE", r"^/api/categories/[^/]+$", "supprimer_produit"),

    # ─── CHARTS (Phase 2+) ───
    ("GET", r"^/api/charts/dashboard$", "voir_dashboard"),


]

# ══════════════════════════════════════════════════════════════════
# Routes autorisées pour un CAISSIER (whitelist)
# Le CAISSIER ne peut QUE faire des ventes et consulter ses stats.
# ══════════════════════════════════════════════════════════════════
CAISSIER_ALLOWED_PATTERNS = [
    # ─── Auth ───
    ("POST", r"^/api/auth/login$"),
    ("POST", r"^/api/auth/logout$"),
    ("POST", r"^/api/auth/change-password$"),  # ← AJOUT
    ("GET", r"^/api/auth/me$"),

    # ─── Santé & config publique ───
    ("GET",  r"^/api/sante$"),
    ("GET",  r"^/api/config/public$"),              # ← AJOUT

    # ─── Heartbeat (surveillance poste) ───
    ("POST", r"^/api/sessions/heartbeat$"),         # ← AJOUT (LE BUG)

    # ─── Facturation ───
    ("POST", r"^/api/ventes$"),
    ("GET",  r"^/api/ventes/stats/jour$"),
    ("GET",  r"^/api/ventes$"),
    ("GET",  r"^/api/ventes/[^/]+$"),
    ("GET",  r"^/api/ventes/[^/]+/encaissement$"),  # ← AJOUT (détail)
    ("POST", r"^/api/ventes/[^/]+/annuler$"),

    # ─── Clients ───
    ("GET",  r"^/api/clients/numero/[^/]+$"),
    ("POST", r"^/api/clients$"),

    # ─── Produits ───
    ("GET",  r"^/api/produits$"),
    ("GET",  r"^/api/produits/[^/]+$"),

    # ─── Rapport Z ───
    ("GET", r"^/api/rapports/z/preview$"),  # ← AJOUT si manquant
    ("POST", r"^/api/rapports/z$"),

    # ─── Retours ───
    ("POST", r"^/api/retours$"),
    ("GET",  r"^/api/retours$"),
    ("GET",  r"^/api/retours/[^/]+$"),
]


def is_caissier_allowed(method: str, path: str) -> bool:
    """Vrai si la route est autorisée pour un CAISSIER."""
    method = method.upper()
    for m, pattern in CAISSIER_ALLOWED_PATTERNS:
        if m == method and re.match(pattern, path):
            return True
    return False


def get_required_permission(method: str, path: str) -> str | None:
    """Retourne la permission requise, ou None si publique."""
    method = method.upper()
    for m, pattern, perm in ROUTES_PERMISSIONS:
        if m == method and re.match(pattern, path):
            return perm
    return None