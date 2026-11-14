#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
permissions.py — Catalogue des permissions Nova Pharma
========================================================
Liste toutes les permissions disponibles, organisées par catégorie.
"""

# ══════════════════════════════════════════════════════════════════
# Catalogue complet
# ══════════════════════════════════════════════════════════════════
PERMISSIONS_CATALOG = {
    "Dashboard": {
        "icon": "chart-pie",
        "items": [
            ("voir_dashboard",       "Voir le tableau de bord"),
            ("voir_stats_ca",        "Voir les statistiques de CA"),
            ("voir_stats_stock",     "Voir les statistiques de stock"),
        ],
    },
    "Produits": {
        "icon": "pill",
        "items": [
            ("voir_produits",        "Voir la liste des produits"),
            ("ajouter_produit",      "Ajouter un produit"),
            ("modifier_produit",     "Modifier un produit"),
            ("supprimer_produit",    "Désactiver un produit"),
            ("voir_prix_achat",      "Voir les prix d'achat", "sensible"),
            ("voir_marges",          "Voir les marges", "sensible"),
        ],
    },
    "Clients": {
        "icon": "users",
        "items": [
            ("voir_clients",         "Voir la liste des clients"),
            ("ajouter_client",       "Ajouter un client"),
            ("modifier_client",      "Modifier un client"),
            ("supprimer_client",     "Désactiver un client"),
        ],
    },
    "Facturation": {
        "icon": "invoice",
        "items": [
            ("faire_vente",          "Effectuer une vente"),
            ("annuler_vente",        "Annuler une vente"),
            ("faire_remise",         "Appliquer une remise"),
            ("voir_historique_ventes","Voir l'historique des ventes"),
            ("imprimer_facture",     "Imprimer une facture"),
        ],
    },
    "BLF": {
        "icon": "package",
        "items": [
            ("voir_blf",             "Voir les BLF"),
            ("creer_blf",            "Créer un BLF"),
            ("valider_blf",          "Valider un BLF", "sensible"),
            ("annuler_blf",          "Annuler un BLF", "sensible"),
        ],
    },
    "Fournisseurs": {
        "icon": "truck",
        "items": [
            ("voir_fournisseurs",    "Voir les fournisseurs"),
            ("ajouter_fournisseur",  "Ajouter un fournisseur"),
            ("modifier_fournisseur", "Modifier un fournisseur"),
        ],
    },
    "Rapports": {
        "icon": "chart-line",
        "items": [
            ("voir_rapport_ventes",     "Voir le rapport Ventes"),
            ("voir_rapport_equipe",     "Voir le rapport Équipe"),
            ("voir_rapport_operations", "Voir le rapport Opérations"),
            ("exporter_rapport",        "Exporter les rapports"),
        ],
    },
        "Utilisateurs": {
        "icon": "settings",
        "items": [
            ("voir_utilisateurs",    "Voir les utilisateurs"),
            ("ajouter_user",         "Ajouter un utilisateur"),
            ("modifier_user",        "Modifier un utilisateur"),
            ("desactiver_user",      "Désactiver un utilisateur"),
            ("creer_admin",          "Créer d'autres administrateurs", "owner"),   # ← AJOUT
            ("gerer_permissions",    "Gérer les permissions", "owner"),
        ],
    },
    "Système": {
        "icon": "server",
        "items": [
            ("configurer",           "Configurer l'application", "owner"),
            ("sauvegarder",          "Effectuer une sauvegarde", "owner"),
            ("restaurer",            "Restaurer une sauvegarde", "owner"),
            ("voir_audit_log",       "Consulter le journal d'audit", "owner"),
            ("acceder_mode_technique","Mode technique avancé", "developer"),
        ],
    },
}


# ══════════════════════════════════════════════════════════════════
# Presets par rôle (permissions cochées par défaut)
# ══════════════════════════════════════════════════════════════════
PRESETS = {
    "CAISSIER": [
        # Produits (lecture seule)
        "voir_produits",
        # Clients (lecture + ajout)
        "voir_clients",
        "ajouter_client",
        # Ventes (créer + annuler)
        "faire_vente",
        "annuler_vente",
        # Historique (ses propres ventes)
        "voir_historique_ventes",
        # Le rapport de ventes
        "voir_rapport_ventes",
        # Impression
        "imprimer_facture",
    ],
    "UTILISATEUR": [
        # Base Caissier
        "voir_dashboard",
        "voir_produits",
        "voir_clients",
        "faire_vente",
        "voir_historique_ventes",
        "imprimer_facture",
        # Extensions
        "voir_stats_ca",
        "ajouter_client",
        "modifier_client",
        "faire_remise",
        "voir_fournisseurs",
    ],
    "ADMIN": [
        # Presque tout sauf les permissions "owner"
        "voir_dashboard", "voir_stats_ca", "voir_stats_stock",
        "voir_produits", "ajouter_produit", "modifier_produit",
        "supprimer_produit", "voir_prix_achat", "voir_marges",
        "voir_clients", "ajouter_client", "modifier_client",
        "supprimer_client",
        "faire_vente", "annuler_vente", "faire_remise",
        "voir_historique_ventes", "imprimer_facture",
        "voir_blf", "creer_blf", "valider_blf", "annuler_blf",
        "voir_fournisseurs", "ajouter_fournisseur", "modifier_fournisseur",
        "voir_rapport_ventes", "voir_rapport_equipe",
        "voir_rapport_operations", "exporter_rapport",
        "voir_utilisateurs", "ajouter_user", "modifier_user",
        "desactiver_user",
        # NOTE : PAS de gerer_permissions, configurer,
        # sauvegarder, restaurer, voir_audit_log, acceder_mode_technique
    ],
    "OWNER": ["ALL"],       # Toutes les permissions
    "DEVELOPER": ["ALL"],   # Toutes les permissions
}


# ══════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════
def get_all_permissions() -> list:
    """Retourne la liste de toutes les clés de permission."""
    keys = []
    for cat in PERMISSIONS_CATALOG.values():
        for item in cat["items"]:
            keys.append(item[0])
    return keys


def get_preset(role: str, is_owner: bool = False,
               is_developer: bool = False) -> list:
    """Retourne les permissions par défaut pour un rôle."""
    if is_owner or is_developer:
        return get_all_permissions()
    return list(PRESETS.get(role, PRESETS["UTILISATEUR"]))


def get_permission_label(key: str) -> str:
    """Retourne le libellé d'une permission."""
    for cat in PERMISSIONS_CATALOG.values():
        for item in cat["items"]:
            if item[0] == key:
                return item[1]
    return key

# ══════════════════════════════════════════════════════════════════
# Helpers base de données (utilisés par Setting_main_window)
# ══════════════════════════════════════════════════════════════════
def has_permission(user_id: str, key: str) -> bool:
    """
    Vérifie si un utilisateur possède une permission active.
    Retourne False en cas d'erreur (sécurité par défaut).
    """
    if not user_id:
        return False
    try:
        from Database import db
        row = db.query_one(
            "SELECT 1 FROM UtilisateurPermission "
            "WHERE utilisateur_id = ? AND permission_key = ? AND actif = 1 "
            "LIMIT 1",
            (user_id, key))
        return row is not None
    except Exception:
        return False


def get_user_permissions(user_id: str) -> set:
    """Retourne l'ensemble des permissions actives d'un utilisateur."""
    if not user_id:
        return set()
    try:
        from Database import db
        rows = db.query(
            "SELECT permission_key FROM UtilisateurPermission "
            "WHERE utilisateur_id = ? AND actif = 1",
            (user_id,))
        return {r["permission_key"] for r in rows}
    except Exception:
        return set()

def is_sensible(key: str) -> bool:
    """Indique si une permission est sensible."""
    for cat in PERMISSIONS_CATALOG.values():
        for item in cat["items"]:
            if item[0] == key and len(item) >= 3 and item[2] == "sensible":
                return True
    return False


def is_owner_only(key: str) -> bool:
    """Indique si une permission est réservée au propriétaire."""
    for cat in PERMISSIONS_CATALOG.values():
        for item in cat["items"]:
            if item[0] == key and len(item) >= 3 and item[2] == "owner":
                return True
    return False