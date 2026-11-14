#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_main_window.py — Fenêtre principale Nova Pharma
========================================================
Version 4.9 — Injection PageFacturation + nettoyage legacy

Changements :
  • Flags _is_owner / _is_developer chargés depuis la DB
  • PageFacturation injectée dans page_5 (alias des widgets)
  • _setup_client_selector() appelée APRÈS installation facturation
  • _decrement_stock() trace dans MouvementStock
  • Suppression des imports legacy (Other_setting, Setting_add_user,
    Setting_user, Setting_user_information)
  • _on_register_new_client_clicked() slot dédié
  • Impression facture : plus d'ouverture PDF automatique
"""

import calendar
import json
import logging
import os
import time
from functools import lru_cache
from typing import Optional
import re

import pandas as pd
from PySide6 import QtCore, QtGui, QtWidgets

from Client.api_singleton import get_api, is_client_mode
from Database import db, seed
from Facture_gen import Generer_ticket_final
from Interface_main_nova_pharma import Ui_MainWindow
from Setting_add_fourniss import Setting_add_fourniss
from Setting_add_produit import Add_produit
from Setting_audit_log import PageAudit
from Setting_rapport import PageRapports
from Setting_save import Setting_save
from Configuration import Configuration
from Setting_user_list import PageUsers
from Notification_manager import notify

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Constantes
# ══════════════════════════════════════════════════════════════════
CONTROL_JSON = "Control.json"  # legacy — conservé pour compat

PAGE_MAP = {
    "btn_onglet_accueil":       "page",
    "btn_onglet_tableau_bord":  "page_2",
    "btn_onglet_article":       "page_3",
    "btn_onglet_client":        "page_4",
    "btn_onglet_facturation":   "page_5",
    "btn_onglet_blf":           "page_9",
    "btn_onglet_historique":    "page_6",
    "btn_onglet_alertes":       "page_alertes",
    "btn_onglet_rapport":       "page_7",
    "btn_onglet_audit":         "page_13",
    "btn_onglet_utilisateur":   "page_8",
    "btn_onglet_parametre":     "page_12",
    "btn_onglet_surveillance": "page_surveillance",  # NOUVEAU
}

NAV_ICON_MAP = {
    "btn_onglet_accueil":       "home-svgrepo-com3",
    "btn_onglet_tableau_bord":  "pie-chart-1-svgrepo-com2",
    "btn_onglet_article":       "medical-medicine-health-11-svgrepo-com2",
    "btn_onglet_client":        "users-group-svgrepo-com4",
    "btn_onglet_facturation":   "invoice-dollar-svgrepo-com (Copie)",
    "btn_onglet_blf":           "shopping-cart-free-5-svgrepo-com",
    "btn_onglet_historique":    "history-svgrepo-com",
    "btn_onglet_rapport":       "report-svgrepo-com",
    "btn_onglet_audit":         "history-svgrepo-com2",
    "btn_onglet_utilisateur":   "user-setting-svgrepo-com",
    "btn_onglet_serveur":       "user-setting-svgrepo-com2",
}

PERMISSIONS = {
    "ADMIN": {
        "voir_dashboard", "ajouter_produit", "modifier_stock",
        "supprimer_produit", "ajouter_user", "ajouter_fournisseur",
        "configurer", "sauvegarder", "supprimer_client",
    },
    "UTILISATEUR": {"voir_dashboard"},
    "CAISSIER":    {"voir_dashboard"},
}

# Format : (ADMIN, UTILISATEUR, CAISSIER)
# CAISSIER : UNIQUEMENT facturation
ROLE_SECTION_VISIBILITY = {
    "btn_onglet_accueil":       (True,  False, False),   # ← CAISSIER: False
    "btn_onglet_tableau_bord":  (True,  False, False),
    "btn_onglet_article":       (True,  False, False),   # ← CAISSIER: False
    "btn_onglet_client":        (True,  False, False),
    "btn_onglet_facturation":   (True,  True,  True),    # ← SEUL onglet visible CAISSIER
    "btn_onglet_blf":           (True,  False, False),
    "btn_onglet_historique":    (True,  False, False),
    "btn_onglet_rapport":       (True,  False, False),
    "btn_onglet_audit":         (True, False, False),
    "btn_onglet_utilisateur":   (True,  False, False),
    "btn_onglet_serveur":       (True, False, False),
    "btn_onglet_alertes":       (True,  False, False),   # ← FORCE False pour CAISSIER
    "btn_onglet_surveillance":  (True, False, False),   # ← FORCE False
}

PHONE_REGEX = re.compile(r"^(?:\+243\d{9}|0\d{9})$")


class PermissionDeniedError(Exception):
    """Levée quand l'utilisateur tente une action non autorisée."""


# ══════════════════════════════════════════════════════════════════
# Fenêtre principale
# ══════════════════════════════════════════════════════════════════
class Setting_main_window(QtWidgets.QMainWindow, Ui_MainWindow):

    # ═══ Signaux ═══
    logout_requested = QtCore.Signal()
    window_closed = QtCore.Signal()

    def __init__(self,
                 user_id: str = None,
                 role: str = "ADMIN",
                 identifiant: str = "",
                 splash=None):
        super().__init__()
        self._splash = splash

        # ---------- Session ----------
        self.user_id = user_id
        self._is_logging_out = False
        self.role = (role or "UTILISATEUR").upper()
        self.identifiant = identifiant
        if self.user_id is None:
            logger.warning("MainWindow ouvert SANS user_id (mode test ?)")

        # ---------- Compteur heartbeat (mode client) ----------
        self._heartbeat_failures = 0
        self._server_time_offset = None   # offset calculé via /api/sante

        # ---------- Flags OWNER / DEVELOPER ----------
        self._is_owner = False
        self._is_developer = False
        if self.user_id:
            try:
                if is_client_mode():
                    from Client.api_singleton import get_api
                    api = get_api()
                    if api:
                        user_data = api.me()
                        self._is_owner = bool(user_data.get("is_owner"))
                        self._is_developer = bool(user_data.get("is_developer"))
                        self.role = (user_data.get("role") or self.role).upper()
                else:
                    row = db.query_one(
                        "SELECT is_owner, is_developer, role FROM Utilisateur "
                        "WHERE id = ? LIMIT 1",
                        (self.user_id,))
                    if row:
                        self._is_owner = bool(row["is_owner"])
                        self._is_developer = bool(row["is_developer"])

                    if not self._is_owner and not self._is_developer:
                        try:
                            check = db.query_one(
                                "SELECT COUNT(*) AS n FROM Utilisateur "
                                "WHERE is_owner = 1")
                            if not check or int(check["n"] or 0) == 0:
                                first = db.query_one(
                                    """SELECT id FROM Utilisateur
                                       ORDER BY created_at ASC, rowid ASC
                                       LIMIT 1""")
                                if first and first["id"] == self.user_id:
                                    db.execute(
                                        "UPDATE Utilisateur "
                                        "SET is_owner = 1 WHERE id = ?",
                                        (self.user_id,))
                                    self._is_owner = True
                                    logger.info(
                                        "Auto-promotion OWNER : %s",
                                        self.identifiant)
                        except Exception:
                            logger.exception(
                                "Erreur auto-promotion OWNER")
            except Exception:
                logger.exception(
                    "Impossible de charger les flags owner/developer")

        # ---------- État interne ----------
        self.df_produits: Optional[pd.DataFrame] = None
        self.df_produits_view: Optional[pd.DataFrame] = None
        self.df_client: Optional[pd.DataFrame] = None
        self.dic_user: dict = {}
        self._page_accueil_content = None
        self.page_clients = None
        self.page_facturation = None
        self.page_blf = None
        self.page_rapports = None
        self.page_users = None
        self.page_audit = None
        self.page_historique = None
        self.page_parametres = None
        self.page_alertes_content = None
        self._current_client_id = None

        # ---------- UI (UNE SEULE FOIS) ----------
        self.setupUi(self)

        # ---------- Carte profil utilisateur (sidebar) ----------
        self._setup_user_profile()  # ← AJOUT

        # ---------- Notifications ----------
        try:
            notify.attach_to_main(self)
        except Exception:
            logger.exception("Erreur attachement notifications")

        # 🔒 Pour les caissiers : désactive les actions de menu
        if self.role == "CAISSIER" and not (self._is_owner or self._is_developer):
            try:
                for action in self.findChildren(QtGui.QAction):
                    if action.objectName().startswith("action_"):
                        action.setEnabled(False)
            except Exception:
                pass

        # ---------- Config depuis la DB ----------
        self._splash_step("Chargement de la configuration…")
        self.config_file_json = {
            "chiffre_affaire": db.get_config("chiffre_affaire_periode", "Mois"),
            "devise": db.get_config("devise", "FC"),
        }
        self.devise = self.config_file_json["devise"]

        # ---------- Permissions ----------
        self._apply_permissions()

        # ---------- Injection des pages ----------
        self._splash_step("Installation des pages…")

        # ─── Toujours installées ───
        self._install_page_facturation()
        self._install_server_indicator()

        # ─── Pages avancées (sauf CAISSIER) ───
        if self._should_install_advanced_pages():
            self._install_page_accueil()
            self._install_page_clients()
            self._install_page_blf()
            self._install_page_users()
            self._install_page_audit()
            self._install_page_rapports()
            self._install_page_historique()
            self._install_page_parametres()
            self._install_page_alertes()
            self._install_page_surveillance()
            self._setup_article_search()
        else:
            logger.info(
                "CAISSIER : pages avancées non installées "
                "(facturation uniquement)")

        # ---------- Client selector (facturation) ----------
        # Maintenant que les widgets de page_5 sont aliasés au MainWindow
        self._setup_client_selector()

        # ---------- Base de données ----------
        self._splash_step("Chargement des produits et clients…")
        try:
            self.Connexion_database()
        except Exception as e:
            logger.exception("Échec initialisation BDD")
            QtWidgets.QMessageBox.critical(
                self, "Erreur fatale",
                f"Impossible d'initialiser la base :\n{e}")
            raise

        # ---------- Signaux & UI ----------
        self._splash_step("Préparation de l'interface…")
        self.Connexion()
        self.Applique_fonction()
        self.Load_data_onglet_1()
        self.Setting_table_widget()

        # ---------- Graphiques ----------
        self._splash_step("Installation des graphiques…")
        try:
            from Charts import install_dashboard_charts
            install_dashboard_charts(self)
        except Exception:
            logger.exception("Impossible d'installer les graphiques")

        # ---------- Timer ----------
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.Get_time)
        # 1 s partout (plus d'appel HTTP dans Get_time)
        self._timer.start(1000)
        self.Get_time()

        # ─── Heartbeat (mode client) ───
        if is_client_mode():
            self._hb_timer = QtCore.QTimer(self)
            self._hb_timer.timeout.connect(self._send_heartbeat)
            self._hb_timer.start(30000)  # 30 s
            QtCore.QTimer.singleShot(2000, self._send_heartbeat)

        # ---------- Vues ----------
        self.View_fournisseur()

        # ─── Notifications de démarrage ───
        QtCore.QTimer.singleShot(800, self._welcome_notify)
        QtCore.QTimer.singleShot(1500, self._check_low_stock_notify)
        QtCore.QTimer.singleShot(2000, self._check_startup_alerts)
        QtCore.QTimer.singleShot(2500, self._notify_trial_status)  # ← AJOUT

        # ─── Raccourci Ctrl+Alt+P : config imprimante ───
        try:
            shortcut_printer = QtGui.QShortcut(
                QtGui.QKeySequence("Ctrl+Alt+P"), self)
            shortcut_printer.activated.connect(self._open_printer_config)
            shortcut_printer.setContext(QtCore.Qt.ApplicationShortcut)
            self._shortcut_printer = shortcut_printer
            logger.info("Raccourci Ctrl+Alt+P → config imprimante")
        except Exception:
            logger.exception("Erreur raccourci imprimante")

        # ─── Raccourci Ctrl+Alt+T : taux de change ───
        try:
            shortcut_taux = QtGui.QShortcut(
                QtGui.QKeySequence("Ctrl+Alt+T"), self)
            shortcut_taux.activated.connect(self._open_taux_change)
            shortcut_taux.setContext(QtCore.Qt.ApplicationShortcut)
            self._shortcut_taux = shortcut_taux
        except Exception:
            logger.exception("Erreur raccourci taux")

        logger.info(
            "MainWindow prêt (role=%s, owner=%s, dev=%s, id=%s)",
            self.role, self._is_owner, self._is_developer, self.identifiant)

    # ══════════════════════════════════════════════════════════════
    # Notifications de démarrage
    # ══════════════════════════════════════════════════════════════
    def _welcome_notify(self):
        try:
            if self.role == "CAISSIER":
                notify.info(
                    f"Bonjour ! Prêt à encaisser vos ventes.", 4000)
            else:
                notify.info(
                    f"Bonjour {self.identifiant} — "
                    f"Bienvenue sur Nova Pharma.", 4000)
        except Exception:
            pass

    def _check_low_stock_notify(self):
        # ─── CAISSIER : pas concerné ───
        if self._is_caissier_restricted():
            return

        # ─── MODE CLIENT → API ───
        if is_client_mode():
            try:
                api = get_api()
                result = api.list_produits(
                    page=1, per_page=1, rupture=True)
                n = int(result.get("total", 0))
                if n > 0:
                    notify.warning(
                        f"{n} produit(s) en rupture de stock. "
                        f"Vérifiez l'inventaire.", 8000)
            except Exception:
                logger.debug("Rupture stock (API) indisponible")
            return

        # ─── MODE AUTONOME / SERVEUR → DB locale ───
        try:
            row = db.query_one(
                "SELECT COUNT(*) AS n FROM produits "
                "WHERE actif = 1 AND Quantite <= 5")
            n = int(row["n"] or 0) if row else 0
            if n > 0:
                notify.warning(
                    f"{n} produit(s) en rupture de stock. "
                    f"Vérifiez l'inventaire.", 8000)
        except Exception:
            pass

    def _splash_step(self, message: str) -> None:
        if self._splash is not None:
            try:
                self._splash.step(message)
            except Exception:
                pass

    def _splash_progress(self, value: int) -> None:
        if self._splash is not None:
            try:
                self._splash.set_progress(value)
            except Exception:
                pass

    def _check_startup_alerts(self):
        """Vérifie les alertes au démarrage (stock, backup, mot de passe, serveur)."""
        from Notification_manager import notify
        from Client.api_singleton import is_client_mode, get_api

        # ═══════════════════════════════════════════════════════════
        # 1. Mode client : Vérifier la connexion serveur
        # ═══════════════════════════════════════════════════════════
        if is_client_mode():
            api = get_api()
            if api is not None:
                try:
                    api.sante()  # test de connexion
                except Exception:
                    notify.error(
                        "Le serveur est actuellement injoignable. "
                        "Certaines fonctions peuvent être indisponibles.",
                        duration=8000
                    )

        # ═══════════════════════════════════════════════════════════
        # 2. Ruptures de stock
        # ═══════════════════════════════════════════════════════════
        try:
            seuil = int(db.get_config("seuil_stock", 20))
            if is_client_mode():
                # En client, on interroge l'API (via le dashboard ou les produits)
                api = get_api()
                if api:
                    res = api.list_produits(page=1, per_page=1, rupture=True)
                    n_rupture = int(res.get("total", 0))
                else:
                    n_rupture = 0
            else:
                # En local
                row = db.query_one(
                    "SELECT COUNT(*) AS n FROM produits "
                    "WHERE actif = 1 AND Quantite <= ?", (seuil,))
                n_rupture = int(row["n"] or 0) if row else 0

            if n_rupture > 0:
                notify.warning(
                    f"Attention : {n_rupture} produit(s) sont en rupture de stock "
                    f"(seuil ≤ {seuil}). Pensez à réapprovisionner.",
                    duration=6000
                )
        except Exception:
            logger.exception("Erreur check stock startup")

        # ═══════════════════════════════════════════════════════════
        # 3. Sauvegarde ancienne
        # ═══════════════════════════════════════════════════════════
        try:
            if is_client_mode():
                # En client, la config publique contient le last_daily
                from Client.api_singleton import get_config
                last = get_config("backup_last_daily", "")
            else:
                last = db.get_config("backup_last_daily", "")

            if not last:
                notify.warning(
                    "Aucune sauvegarde de sécurité n'a été effectuée. "
                    "Pensez à configurer les sauvegardes automatiques.",
                    duration=6000
                )
            else:
                from datetime import datetime as _dt
                last_dt = _dt.fromisoformat(last)
                jours = (_dt.now() - last_dt).days
                if jours > 7:
                    notify.warning(
                        f"La dernière sauvegarde date de {jours} jours. "
                        "Il est recommandé de sauvegarder la base.",
                        duration=6000
                    )
        except Exception:
            pass  # Silencieux si erreur de date

        # ═══════════════════════════════════════════════════════════
        # 4. Mot de passe temporaire
        # ═══════════════════════════════════════════════════════════
        try:
            need_change = False
            if is_client_mode():
                # L'info est dans api.me()
                api = get_api()
                if api and api.user:
                    need_change = bool(api.user.get("must_change_password"))
            else:
                row = db.query_one(
                    "SELECT must_change_password FROM Utilisateur WHERE id = ?",
                    (self.user_id,))
                if row:
                    need_change = bool(row["must_change_password"])

            if need_change:
                notify.info(
                    "Vous utilisez un mot de passe temporaire. "
                    "Veuillez le modifier dans les paramètres de votre profil.",
                    duration=8000
                )
        except Exception:
            pass

    def _notify_trial_status(self):
        """Affiche une notification 10s sur l'état de l'essai / licence."""
        from Notification_manager import notify

        try:
            from Core.license_manager import get_trial_days_left
            days = get_trial_days_left()
        except Exception:
            return

        # Licence valide → pas de notification
        if days == -1:
            return

        # Erreur (horloge / fichier)
        if days == -2:
            return

        # Essai expiré → on ne devrait pas arriver ici (bloqué avant)
        if days == 0:
            return

        # Essai en cours
        if days > 7:
            notify.info(
                f"💡 Essai gratuit : {days} jour(s) restant(s). "
                f"Activez votre licence dans Paramètres → Licence.",
                duration=10000
            )
        elif days > 1:
            notify.warning(
                f"⏰ Attention : votre essai expire dans {days} jour(s). "
                f"Pensez à activer votre licence.",
                duration=10000
            )
        else:
            notify.warning(
                f"⚠️ DERNIER JOUR D'ESSAI ! "
                f"Activez votre licence pour continuer à utiliser Nova Pharma.",
                duration=10000
            )

    # ══════════════════════════════════════════════════════════════
    # Helpers permissions
    # ══════════════════════════════════════════════════════════════
    def _has_perm(self, perm: str) -> bool:
        if self._is_owner or self._is_developer:
            return True
        try:
            from Database import permissions as perms
            if perms.has_permission(self.user_id, perm):
                return True
        except Exception:
            pass
        return perm in PERMISSIONS.get(self.role, set())

    def _is_caissier_restricted(self) -> bool:
        """CAISSIER pur (sans droits OWNER/DEV) → facturation uniquement."""
        return (self.role == "CAISSIER"
                and not (self._is_owner or self._is_developer))

    def _should_install_advanced_pages(self) -> bool:
        """Vrai si le rôle autorise l'installation des pages avancées."""
        return not self._is_caissier_restricted()

    def _require_perm(self, perm: str) -> None:
        if not self._has_perm(perm):
            logger.warning(
                "Permission refusée : role=%s, perm=%s, user=%s",
                self.role, perm, self.identifiant)
            raise PermissionDeniedError(
                "Vous n'avez pas les droits pour effectuer cette action.")

    # ══════════════════════════════════════════════════════════════
    # Permissions & navigation
    # ══════════════════════════════════════════════════════════════
    def _apply_permissions(self) -> None:
        idx = {"ADMIN": 0, "UTILISATEUR": 1, "CAISSIER": 2}.get(self.role, 1)

        is_caissier = (
                self.role == "CAISSIER"
                and not (self._is_owner or self._is_developer)
        )

        # ═══ CAISSIER : masquer TOUT sauf la facturation ═══
        if is_caissier:
            for name in (
                    "btn_onglet_accueil",
                    "btn_onglet_tableau_bord",
                    "btn_onglet_article",
                    "btn_onglet_client",
                    "btn_onglet_blf",
                    "btn_onglet_historique",
                    "btn_onglet_rapport",
                    "btn_onglet_audit",
                    "btn_onglet_utilisateur",
                    "btn_onglet_serveur",
                    "btn_onglet_parametre",
                    "btn_onglet_alertes",
                    "btn_onglet_surveillance",
            ):
                btn = getattr(self, name, None)
                if btn is not None:
                    btn.setVisible(False)

            # Seul bouton visible
            btn_fact = getattr(self, "btn_onglet_facturation", None)
            if btn_fact is not None:
                btn_fact.setVisible(True)

            # ─── Menu bar : cacher complètement ───
            try:
                menubar = self.menuBar()
                if menubar is not None:
                    menubar.setVisible(False)
            except Exception:
                pass

            # ─── Empêcher accès aux pages du stackedWidget ───
            self._lock_caissier_pages()

            logger.info(
                "CAISSIER : accès limité à la facturation")
            return

        # ═══ AUTRES RÔLES : logique normale ═══
        for name, vis in ROLE_SECTION_VISIBILITY.items():
            btn = getattr(self, name, None)
            if btn is not None:
                btn.setVisible(vis[idx])

        # Bouton Audit : OWNER / DEVELOPER uniquement
        btn_audit = getattr(self, "btn_onglet_audit", None)
        if btn_audit is not None:
            btn_audit.setVisible(self._is_owner or self._is_developer)

        # Bouton Paramètres
        btn_param = getattr(self, "btn_onglet_parametre", None)
        if btn_param is None:
            btn_param = getattr(self, "btn_onglet_serveur", None)
        if btn_param is not None:
            btn_param.setVisible(self.role != "CAISSIER")

        # Menu Administration
        menu_admin = getattr(self, "menu_admin", None)
        if menu_admin is not None:
            can_admin = (self._is_owner or self._is_developer
                         or self.role == "ADMIN")
            menu_admin.menuAction().setVisible(can_admin)

        # Menu Aide
        menu_aide = getattr(self, "menu_aide", None)
        if menu_aide is not None:
            menu_aide.menuAction().setVisible(self.role != "CAISSIER")

        try:
            menubar = self.menuBar()
            if menubar is not None:
                menubar.setVisible(True)
        except Exception:
            pass

    def _lock_caissier_pages(self) -> None:
        """Bloque l'accès aux pages non-autorisées du stackedWidget."""
        try:
            if not hasattr(self, "stackedWidget"):
                return

            # Récupère l'index de la page facturation (page_5)
            target_page = getattr(self, "page_5", None)
            if target_page is None:
                return

            allowed_idx = self.stackedWidget.indexOf(target_page)
            if allowed_idx < 0:
                return

            # Force la page facturation au premier plan
            self.stackedWidget.setCurrentIndex(allowed_idx)

            # Force aussi la page de facturation au démarrage
            self._caissier_allowed_page = allowed_idx

            logger.info(
                "CAISSIER : page verrouillée sur index %d", allowed_idx)
        except Exception:
            logger.exception("Erreur verrouillage pages caissier")

    def Changer_window(self) -> None:
        btn = self.sender()
        if btn is None:
            return

        # ═══ CAISSIER : bloque toute navigation sauf facturation ═══
        if (self.role == "CAISSIER"
                and not (self._is_owner or self._is_developer)):
            if btn.objectName() != "btn_onglet_facturation":
                logger.warning(
                    "CAISSIER : navigation vers %s bloquée",
                    btn.objectName())
                # Force la facturation
                btn_fact = getattr(self, "btn_onglet_facturation", None)
                if btn_fact is not None and btn_fact.isChecked() is False:
                    btn_fact.setChecked(True)
                return

        for b in self.frm_nav.findChildren(QtWidgets.QPushButton):
            b.setChecked(b is btn)

        page_name = PAGE_MAP.get(btn.objectName())
        if not page_name:
            logger.warning("Pas de mapping pour %s", btn.objectName())
            return

        target = getattr(self, page_name, None)
        if target is None:
            logger.warning("Page '%s' introuvable", page_name)
            return

        idx = self.stackedWidget.indexOf(target)
        if idx < 0:
            logger.warning("Page '%s' pas dans le stackedWidget", page_name)
            return

        if hasattr(self.stackedWidget, "slide_to_index"):
            self.stackedWidget.slide_to_index(idx)
        else:
            self.stackedWidget.setCurrentIndex(idx)

        if hasattr(self, "lbl_titre_change"):
            self.lbl_titre_change.setText(btn.text())

        icon_name = NAV_ICON_MAP.get(btn.objectName())
        if icon_name and hasattr(self, "lbl_ico_change"):
            self.lbl_ico_change.setStyleSheet(
                "#lbl_ico_change {"
                "  background-color: rgb(239, 246, 255);"
                f"  image: url(:/Icon/Icons/{icon_name}.svg);"
                "  border: 1px solid rgb(219, 234, 254);"
                "  border-radius: 13px;"
                "  padding: 8px;"
                "}")

    # ══════════════════════════════════════════════════════════════
    # Installation PageAccueil dans page
    # ══════════════════════════════════════════════════════════════
    def _install_page_accueil(self) -> None:
        try:
            from Setting_accueil import PageAccueil

            target = getattr(self, "page", None)
            if target is None:
                logger.warning("page absent du .ui")
                return

            content = PageAccueil(
                parent=target,
                user_id=self.user_id,
                user_name=self.identifiant,
                role=self.role,
                is_owner=self._is_owner,
                is_developer=self._is_developer,
            )

            layout = target.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(target)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()

            layout.addWidget(content)
            self._page_accueil_content = content
            logger.info("PageAccueil installée dans page")

        except Exception as e:
            logger.exception("Impossible d'installer PageAccueil")
            QtWidgets.QMessageBox.warning(
                self, "Erreur",
                f"Impossible d'installer la page accueil :\n{e}")

    # ══════════════════════════════════════════════════════════════
    # Installation PageClients dans page_4
    # ══════════════════════════════════════════════════════════════
    def _install_page_clients(self) -> None:
        try:
            from Setting_client import PageClients

            self.page_clients = PageClients(
                parent=self,
                user_id=self.user_id,
                role=self.role,
            )

            target = self.page_4
            layout = target.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(target)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()

            layout.addWidget(self.page_clients)
            logger.info("PageClients installée dans page_4")

        except Exception as e:
            logger.exception("Impossible d'installer PageClients")
            QtWidgets.QMessageBox.warning(
                self, "Erreur",
                f"Impossible d'installer la page clients :\n{e}")

    # ══════════════════════════════════════════════════════════════
    # Installation PageFacturation dans page_5
    # ══════════════════════════════════════════════════════════════
    def _install_page_facturation(self) -> None:
        """Instancie PageFacturation et l'injecte dans page_5.

        Expose ensuite tous ses widgets comme attributs du MainWindow
        pour rester compatible avec le code existant (self.edit_name_client,
        self.tableWidget, etc.).
        """
        try:
            from Setting_page_facturation import PageFacturation

            self.page_facturation = PageFacturation(
                parent=self,
                user_id=self.user_id,
                identifiant=self.identifiant,
                main_window=self,
            )

            target = self.page_5
            layout = target.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(target)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()

            layout.addWidget(self.page_facturation)

            # ═══════════════════════════════════════════════════════════
            # ALIAS : expose les widgets au MainWindow
            # → le code existant continue de fonctionner SANS modification.
            # ═══════════════════════════════════════════════════════════
            p = self.page_facturation
            for name in (
                # Champs client
                "edit_name_client",
                "edit_identification_client",
                "edit_numero_client",
                # Boutons
                "btn_register_new_client",
                "btn_recheche_person_facture",
                "btn_add_produit_for_facture",
                "btn_clear_table_facture",
                "btn_remove_line_facture",
                "btn_print_facture",
                "btn_rapport_z",
                "btn_mes_ventes_jour",
                # Produits
                "edit_recherche_produit",
                "spin_quantite_facture",
                "spin_nbr_stock",
                # Panier
                "tableWidget",
                # Totaux
                "lbl_totale_calc",
                "lbl_total_nbr_produit",
                # Labels (Set_client_status / debug)
                "label_7", "label_21", "label_22", "label_31",
            ):
                if hasattr(p, name):
                    setattr(self, name, getattr(p, name))

            # Layout vertical pour label_client_status
            if hasattr(p, "verticalLayout_12"):
                self.verticalLayout_12 = p.verticalLayout_12

            # ─── Table panier : 5 colonnes (4 + bouton retrait) ───
            if hasattr(self, "tableWidget"):
                tw = self.tableWidget
                while tw.columnCount() < 5:
                    tw.setColumnCount(5)
                tw.setHorizontalHeaderLabels([
                    "Article", "Qté", "P.U.", "Total", ""
                ])
                h = tw.horizontalHeader()
                h.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                for i in (1, 2, 3):
                    h.setSectionResizeMode(
                        i, QtWidgets.QHeaderView.ResizeToContents)
                h.setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
                tw.setColumnWidth(4, 44)
                logger.info("Table panier : 5 colonnes configurées")

            # Méthode optionnelle de mise à jour du header facture
            if hasattr(p, "update_facture_header"):
                self._update_facture_header = p.update_facture_header

            logger.info("PageFacturation installée dans page_5")

        except Exception as e:
            logger.exception("Impossible d'installer PageFacturation")
            QtWidgets.QMessageBox.warning(
                self, "Erreur",
                f"Impossible d'installer la page facturation :\n{e}")

    # ══════════════════════════════════════════════════════════════
    # Installation PageBLF dans page_9
    # ══════════════════════════════════════════════════════════════
    def _install_page_blf(self) -> None:
        try:
            from Setting_blf_list import PageBLF

            self.page_blf = PageBLF(
                parent=self,
                user_id=self.user_id,
                user_name=self.identifiant,
                role=self.role,
            )

            target = self.page_9
            layout = target.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(target)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()

            layout.addWidget(self.page_blf)
            logger.info("PageBLF installée dans page_9")

        except Exception as e:
            logger.exception("Impossible d'installer PageBLF")
            QtWidgets.QMessageBox.warning(
                self, "Erreur",
                f"Impossible d'installer la page BLF :\n{e}")

    # ══════════════════════════════════════════════════════════════
    # Installation PageUsers dans page_8
    # ══════════════════════════════════════════════════════════════
    def _install_page_users(self) -> None:
        try:
            self.page_users = PageUsers(
                parent=self,
                user_id=self.user_id,
                role=self.role,
                is_owner=self._is_owner,
                is_developer=self._is_developer,
            )

            target = self.page_8
            layout = target.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(target)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()

            layout.addWidget(self.page_users)
            logger.info("PageUsers installée dans page_8")

        except Exception as e:
            logger.exception("Impossible d'installer PageUsers")
            QtWidgets.QMessageBox.warning(
                self, "Erreur",
                f"Impossible d'installer la page utilisateurs :\n{e}")

    # ══════════════════════════════════════════════════════════════
    # Installation PageAudit dans page_13
    # ══════════════════════════════════════════════════════════════
    def _install_page_audit(self) -> None:
        try:
            if not (self._is_owner or self._is_developer):
                logger.info("PageAudit non installée (droits insuffisants)")
                return

            self.page_audit = PageAudit(
                parent=self,
                user_id=self.user_id,
                role=self.role,
                is_owner=self._is_owner,
                is_developer=self._is_developer,
            )

            target = self.page_13
            layout = target.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(target)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()

            layout.addWidget(self.page_audit)
            logger.info("PageAudit installée dans page_13")

        except Exception as e:
            logger.exception("Impossible d'installer PageAudit")
            QtWidgets.QMessageBox.warning(
                self, "Erreur",
                f"Impossible d'installer la page audit :\n{e}")

    # ══════════════════════════════════════════════════════════════
    # Installation PageHistorique dans page_6
    # ══════════════════════════════════════════════════════════════
    def _install_page_historique(self) -> None:
        try:
            from Setting_historique import PageHistorique

            self.page_historique = PageHistorique(
                parent=self,
                user_id=self.user_id,
                role=self.role,
                user_name=self.identifiant,
                is_owner=self._is_owner,
                is_developer=self._is_developer,
            )

            target = self.page_6
            layout = target.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(target)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()

            layout.addWidget(self.page_historique)
            logger.info("PageHistorique installée dans page_6")

        except Exception as e:
            logger.exception("Impossible d'installer PageHistorique")
            QtWidgets.QMessageBox.warning(
                self, "Erreur",
                f"Impossible d'installer la page historique :\n{e}")

    # ══════════════════════════════════════════════════════════════
    # Installation PageParametres dans page_12
    # ══════════════════════════════════════════════════════════════
    def _install_page_parametres(self) -> None:
        try:
            from Setting_parametres import PageParametres

            self.page_parametres = PageParametres(
                parent=self,
                user_id=self.user_id,
                user_name=self.identifiant,
                is_owner=self._is_owner,
                is_developer=self._is_developer,
            )
            self.page_parametres.parametres_changed.connect(
                self._on_parametres_changed)

            target = self.page_12
            layout = target.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(target)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()

            layout.addWidget(self.page_parametres)
            logger.info("PageParametres installée dans page_12")

        except Exception as e:
            logger.exception("Impossible d'installer PageParametres")
            QtWidgets.QMessageBox.warning(
                self, "Erreur",
                f"Impossible d'installer la page paramètres :\n{e}")

    def _on_parametres_changed(self) -> None:
        try:
            # Relit depuis la DB (pas depuis cache)
            self.config_file_json = {
                "chiffre_affaire":
                    db.get_config("chiffre_affaire_periode", "Mois"),
                "devise": db.get_config("devise", "FC"),
            }
            self.devise = self.config_file_json["devise"]

            # Recalcule l'accueil si installé
            accueil = getattr(self, "_page_accueil_content", None)
            if accueil is not None:
                try:
                    accueil._periode = self.config_file_json["chiffre_affaire"]
                    if hasattr(accueil, "btn_periode_semaine"):
                        accueil.btn_periode_semaine.setChecked(
                            accueil._periode == "Semaine")
                        accueil.btn_periode_mois.setChecked(
                            accueil._periode == "Mois")
                        accueil.btn_periode_annee.setChecked(
                            accueil._periode == "Année")
                    accueil.refresh()
                except Exception:
                    logger.exception("Erreur refresh accueil")

            self.Load_data_onglet_1()
            self.Add_produit_tablewidget()
            logger.info("Paramètres rechargés (période=%s)",
                        self.config_file_json["chiffre_affaire"])
        except Exception:
            logger.exception("Erreur rechargement paramètres")

    # ══════════════════════════════════════════════════════════════
    # Installation PageAlertes dans page_alertes
    # ══════════════════════════════════════════════════════════════
    def _install_page_alertes(self) -> None:
        try:
            from Alertes_dashboard import AlertesPage

            target = getattr(self, "page_alertes", None)
            if target is None:
                logger.warning("page_alertes absent du .ui")
                return

            content = AlertesPage(parent=target, main_window=self)

            layout = target.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(target)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()

            layout.addWidget(content)
            self.page_alertes_content = content
            logger.info("PageAlertes installée dans page_alertes")

        except Exception as e:
            logger.exception("Impossible d'installer PageAlertes")
            QtWidgets.QMessageBox.warning(
                self, "Erreur",
                f"Impossible d'installer la page alertes :\n{e}")

    def _install_page_surveillance(self) -> None:
        """Instancie PageSurveillance (OWNER/DEVELOPER uniquement)."""
        try:
            if not (self._is_owner or self._is_developer):
                logger.info("PageSurveillance non installée (droits)")
                return

            from Setting_surveillance import PageSurveillance

            # ─── La page cible est celle du .ui ───
            target = getattr(self, "page_surveillance", None)
            if target is None:
                logger.warning("page_surveillance absent du .ui")
                return

            # ⚠️ IMPORTANT : ne PAS écraser self.page_surveillance
            # On stocke le contenu dans un attribut dédié
            content = PageSurveillance(
                parent=target,
                user_id=self.user_id,
                role=self.role,
                user_name=self.identifiant,
                is_owner=self._is_owner,
                is_developer=self._is_developer,
            )

            layout = target.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(target)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()

            layout.addWidget(content)

            # ─── On garde une référence au CONTENU ───
            self._page_surveillance_content = content

            logger.info("PageSurveillance installée dans page_surveillance")

        except Exception as e:
            logger.exception("Erreur installation PageSurveillance")
            QtWidgets.QMessageBox.warning(
                self, "Erreur",
                f"Impossible d'installer la surveillance :\n{e}")

    def _install_server_indicator(self) -> None:
        """Ajoute un badge d'état serveur dans le header."""
        try:
            from Client.api_singleton import get_api, is_client_mode

            # ─── Conteneur ───
            self.server_badge = QtWidgets.QLabel()
            self.server_badge.setObjectName("server_badge")
            self.server_badge.setMinimumHeight(28)

            # ─── Insère dans le header (avant lbl_temps) ───
            layout = None
            if hasattr(self, "horizontalLayout_5"):
                layout = self.horizontalLayout_5
            elif hasattr(self, "frame_4"):
                layout = self.frame_4.layout()

            if layout is not None:
                idx = -1
                for i in range(layout.count()):
                    it = layout.itemAt(i)
                    if it and it.widget() is getattr(self, "lbl_temps", None):
                        idx = i
                        break

                if idx >= 0:
                    layout.insertWidget(idx, self.server_badge)
                else:
                    layout.addWidget(self.server_badge)

            # ─── Cloche de notifications ───
            self.btn_notif = QtWidgets.QPushButton()
            self.btn_notif.setFixedSize(36, 36)
            self.btn_notif.setCursor(QtCore.Qt.PointingHandCursor)
            self.btn_notif.setStyleSheet("""
                QPushButton {
                    background: #ffffff;
                    border: 1px solid #e2e8f0;
                    border-radius: 10px;
                }
                QPushButton:hover { background: #f8fafc; border-color: #cbd5e1; }
            """)
            self.btn_notif.setIcon(QtGui.QIcon(":/Icon/Icons/bell.svg"))
            self.btn_notif.setIconSize(QtCore.QSize(18, 18))
            self.btn_notif.clicked.connect(self._show_notifications_center)

            if layout is not None:
                layout.insertWidget(idx if idx >= 0 else layout.count(), self.btn_notif)

            # ─── Vérifier les nouvelles notifs ───
            self._notif_timer = QtCore.QTimer(self)
            self._notif_timer.timeout.connect(self._check_unread_notifs)
            self._notif_timer.start(10000)  # 10 s
            self._check_unread_notifs()

            # ─── Premier rendu ───
            self._refresh_server_badge()

            # ─── Timer de surveillance (toutes les 30s) ───
            self._server_timer = QtCore.QTimer(self)
            self._server_timer.timeout.connect(self._refresh_server_badge)
            self._server_timer.start(30000)

            logger.info("Indicateur serveur installé dans le header")

        except Exception:
            logger.exception("Erreur installation indicateur serveur")

        def _check_unread_notifs(self):
            """Vérifie s'il y a des notifications non lues et met à jour la cloche."""
            try:
                if not hasattr(self, "btn_notif"):
                    return

                if is_client_mode():
                    unread = 0
                else:
                    row = db.query_one("SELECT COUNT(*) AS n FROM Notification WHERE lu = 0")
                    unread = int(row["n"] or 0) if row else 0

                if unread > 0:
                    # Icône + badge texte si non-lu
                    self.btn_notif.setText(f" {unread} ")
                    self.btn_notif.setIcon(QtGui.QIcon(":/Icon/Icons/bell_white.svg"))
                    self.btn_notif.setStyleSheet("""
                        QPushButton {
                            background: #dc2626;
                            color: #ffffff;
                            border: 1px solid #b91c1c;
                            border-radius: 10px;
                            font-size: 11px;
                            font-weight: 800;
                        }
                    """)
                else:
                    # Icône seule si tout est lu
                    self.btn_notif.setText("")
                    self.btn_notif.setIcon(QtGui.QIcon(":/Icon/Icons/bell.svg"))
                    self.btn_notif.setStyleSheet("""
                        QPushButton {
                            background: #ffffff;
                            border: 1px solid #e2e8f0;
                            border-radius: 10px;
                        }
                        QPushButton:hover { background: #f8fafc; border-color: #cbd5e1; }
                    """)
            except Exception:
                pass

        def _show_notifications_center(self):
            """Ouvre le panneau des notifications."""
            try:
                # Pour l'instant, simple QMessageBox avec les dernières notifs.
                # Plus tard, on fera un vrai dialog UI.
                rows = db.query("SELECT * FROM Notification ORDER BY created_at DESC LIMIT 20")

                if not rows:
                    from Notification_manager import notify
                    notify.info("Aucune notification pour le moment.")
                    return

                html = "<h3>Notifications récentes</h3><ul>"
                for r in rows:
                    dt = str(r["created_at"])[11:16]
                    html += f"<li><b>[{dt}] {r['title']}</b> : {r['message']}</li>"
                html += "</ul>"

                # Marquer comme lu
                db.execute("UPDATE Notification SET lu = 1")
                self._check_unread_notifs()

                QtWidgets.QMessageBox.information(
                    self, "Centre de notifications", html
                )
            except Exception as e:
                logger.exception("Erreur ouverture notifs")

    def _open_printer_config(self):
        try:
            from Setting_printer_dialog import PrinterConfigDialog
            dlg = PrinterConfigDialog(parent=self)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture config imprimante")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir la configuration.")

    def _open_retour_vente(self) -> None:
        """Ouvre le dialogue de retour pour une facture sélectionnée."""
        # Récupère le numéro de facture depuis le contexte :
        # - soit la sélection en cours dans l'historique
        # - soit demande à l'utilisateur
        num_fact = None

        # Essaie depuis la page Historique si installée
        if self.page_historique is not None:
            try:
                num_fact = self.page_historique._selected_facture()
            except Exception:
                pass

        if not num_fact:
            # Dialogue de saisie manuelle
            num_fact, ok = QtWidgets.QInputDialog.getText(
                self, "Retour de vente",
                "Numéro de facture à retourner :",
                QtWidgets.QLineEdit.Normal, "")
            if not ok or not num_fact.strip():
                return
            num_fact = num_fact.strip()

        # Ouvre le dialogue
        try:
            from Setting_retour_vente import Setting_retour_vente
            dlg = Setting_retour_vente(
                parent=self,
                num_fact=num_fact,
                user_id=self.user_id,
                user_name=self.identifiant,
                role=self.role)
            dlg.retour_valide.connect(self._on_retour_valide)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture retour")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir le formulaire de retour.")

    def _on_retour_valide(self, num_fact: str) -> None:
        """Callback après un retour validé."""
        logger.info("Retour validé pour facture : %s", num_fact)

        # Rafraîchit les vues concernées
        try:
            self._reload_produits_master()
            self.Add_produit_tablewidget()
        except Exception:
            pass

        if self.page_historique is not None:
            try:
                self.page_historique.refresh()
            except Exception:
                pass

        self.Load_data_onglet_1()

    def _refresh_server_badge(self) -> None:
        """Met à jour le badge d'état serveur."""
        try:
            from Client.api_singleton import get_api, is_client_mode

            if not is_client_mode():
                self.server_badge.setVisible(False)
                return

            api = get_api()
            if api is None:
                self.server_badge.setVisible(False)
                return

            self.server_badge.setVisible(True)

            # ─── Teste la connexion ───
            ok = False
            try:
                info = api.sante()
                ok = True
            except Exception:
                ok = False

            if ok:
                self.server_badge.setText("● Serveur connecté")
                self.server_badge.setStyleSheet("""
                    QLabel#server_badge {
                        background: #dcfce7;
                        color: #15803d;
                        border: 1px solid #bbf7d0;
                        border-radius: 8px;
                        padding: 4px 12px;
                        font-size: 10px;
                        font-weight: 800;
                        letter-spacing: 0.5px;
                    }
                """)

                # ─── Met à jour l'offset de temps serveur ───
                try:
                    srv_iso = info.get("server_time", "")
                    if srv_iso:
                        from datetime import datetime as _dt
                        srv = _dt.fromisoformat(srv_iso)
                        self._server_time_offset = (
                                srv - _dt.now()).total_seconds()
                except Exception:
                    logger.debug("Offset serveur non calculé")
            else:
                self.server_badge.setText("● Serveur injoignable")
                self.server_badge.setStyleSheet("""
                    QLabel#server_badge {
                        background: #fee2e2;
                        color: #b91c1c;
                        border: 1px solid #fecaca;
                        border-radius: 8px;
                        padding: 4px 12px;
                        font-size: 10px;
                        font-weight: 800;
                        letter-spacing: 0.5px;
                    }
                """)
        except Exception:
            logger.exception("Erreur refresh badge serveur")

    def _setup_user_profile(self) -> None:
        """Met à jour la carte profil sidebar avec les infos du user connecté."""
        try:
            user = None

            if self.user_id:
                # ─── MODE CLIENT → API ───
                if is_client_mode():
                    try:
                        api = get_api()
                        if api is not None:
                            user = api.me()
                    except Exception:
                        logger.exception(
                            "Erreur /api/auth/me (client)")
                        user = None

                # ─── MODE AUTONOME / SERVEUR → DB locale ───
                if user is None:
                    try:
                        row = db.query_one(
                            """SELECT prenom, nom, post_nom, sexe, role,
                                      is_owner, is_developer, path_image
                               FROM Utilisateur WHERE id = ? LIMIT 1""",
                            (self.user_id,))
                        user = dict(row) if row else None
                    except Exception:
                        logger.exception("Erreur chargement profil user")

            if user is None:
                logger.warning(
                    "Profil user introuvable pour %s", self.user_id)
                return

            prenom = (user.get("prenom") or "").strip()
            nom = (user.get("nom") or "").strip()
            post_nom = (user.get("post_nom") or "").strip()
            sexe = (user.get("sexe") or "M").upper()
            role = (user.get("role") or "UTILISATEUR").upper()
            is_owner = bool(user.get("is_owner"))
            is_developer = bool(user.get("is_developer"))

            # ─── Initiales ───
            initiales = ""
            if prenom:
                initiales += prenom[0].upper()
            if nom:
                initiales += nom[0].upper()
            if not initiales:
                initiales = "?"

            # ─── Libellé du rôle ───
            if is_owner:
                role_label = "PROPRIÉTAIRE"
            elif is_developer:
                role_label = "DÉVELOPPEUR"
            elif role == "ADMIN":
                role_label = "ADMINISTRATEUR"
            elif role == "CAISSIER":
                role_label = "CAISSIER"
            else:
                role_label = "UTILISATEUR"

            # ─── Civilité ───
            civilite = "Mme" if sexe == "F" else "Mr."

            # ─── Nom complet affiché ───
            # Format : "Prénom Nom" (le post-nom est optionnel)
            nom_complet = f"{prenom} {nom}".strip() or "Utilisateur"

            # ═══════════════════════════════════════════════════════════
            # 1. Label initiales (label_3)
            # ═══════════════════════════════════════════════════════════
            lbl_init = getattr(self, "label_3", None)
            if lbl_init is not None:
                lbl_init.setText(initiales)

            # ═══════════════════════════════════════════════════════════
            # 2. Label nom + rôle (label_26)
            # ═══════════════════════════════════════════════════════════
            lbl_info = getattr(self, "label_26", None)
            if lbl_info is not None:
                html = (
                    '<html><head/><body>'
                    '<p>'
                    f'<span style="font-size:9pt; font-weight:700; '
                    f'color:#f8fafc;">{civilite} {nom_complet}</span>'
                    '<span style="font-size:11pt;"><br/></span>'
                    f'<span style="font-size:7pt; font-weight:700; '
                    f'color:#60a5fa; letter-spacing:1px;">{role_label}</span>'
                    '</p>'
                    '</body></html>'
                )
                lbl_info.setText(html)

            # ═══════════════════════════════════════════════════════════
            # 3. Photo de profil (optionnel)
            # ═══════════════════════════════════════════════════════════
            path_image = user.get("path_image")
            if path_image and lbl_init is not None:
                try:
                    # En mode client, ne pas essayer de charger une image
                    # dont le chemin n'existe que sur le serveur
                    if not is_client_mode() and os.path.isfile(path_image):
                        pix = QtGui.QPixmap(path_image)
                        if not pix.isNull():
                            lbl_init.setPixmap(pix.scaled(
                                42, 42, QtCore.Qt.KeepAspectRatioByExpanding,
                                QtCore.Qt.SmoothTransformation))
                            lbl_init.setText("")
                            lbl_init.setScaledContents(True)
                except Exception:
                    logger.exception("Erreur chargement photo profil")

            logger.info(
                "Carte profil mise à jour : %s (%s) — %s",
                nom_complet, role_label, initiales)

        except Exception:
            logger.exception("Erreur _setup_user_profile")

    def _setup_facturation_completer(self) -> None:
        """Configure l'autocomplétion produits (avec détails visibles)."""
        if not hasattr(self, "edit_recherche_produit"):
            return

        try:
            produits = []

            # ═══ MODE CLIENT → API (paginé) ═══
            if is_client_mode():
                api = get_api()
                if api is not None:
                    all_items = []
                    page = 1
                    per_page = 100
                    while page <= 50:
                        try:
                            data = api.list_produits(
                                page=page, per_page=per_page, actif=1)
                        except Exception:
                            logger.exception(
                                "Erreur pagination produits page %d", page)
                            break
                        items = data.get("items", [])
                        all_items.extend(items)
                        if len(items) < per_page:
                            break
                        page += 1
                    produits = all_items
                    logger.info(
                        "Completer API : %d produits (%d pages)",
                        len(produits), page)

            # ═══ MODE AUTONOME / SERVEUR → DB locale ═══
            else:
                if (self.df_produits is not None
                        and not self.df_produits.empty):
                    produits = self.df_produits.to_dict("records")
                    logger.info(
                        "Completer local : %d produits", len(produits))

            if not produits:
                logger.warning(
                    "Completer produits : aucun produit disponible")
                return

            self._produits_list = produits

            # Crée et installe le completer
            from Ui_helpers import ProduitCompleter
            completer = ProduitCompleter(
                produits, self.edit_recherche_produit)
            self.edit_recherche_produit.setCompleter(completer)

            # Connexion : activated → sélection d'un produit
            completer.activated.connect(self._on_produit_completer_selected)

            logger.info(
                "Completer installé sur edit_recherche_produit")

        except Exception:
            logger.exception("Erreur setup completer facturation")

    def _on_produit_completer_selected(self, display: str) -> None:
        """Quand l'utilisateur sélectionne un produit dans le completer."""
        completer = self.edit_recherche_produit.completer()
        if not completer or not hasattr(completer, "get_produit_par_display"):
            return

        produit = completer.get_produit_par_display(display)
        if not produit:
            return

        # Stocke le produit sélectionné
        self._produit_selectionne = produit

        # Met à jour la limite de quantité
        stock = int(produit.get("Quantite") or 0)
        self.spin_quantite_facture.setMaximum(max(1, stock))
        self.spin_nbr_stock.setValue(stock)

        # Vide le champ (le produit est en mémoire)
        self.edit_recherche_produit.blockSignals(True)
        self.edit_recherche_produit.clear()
        self.edit_recherche_produit.blockSignals(False)

        logger.info(
            "Produit sélectionné : %s (stock %d)",
            produit.get("Nom"), stock)

    # ══════════════════════════════════════════════════════════════
    # Base de données
    # ══════════════════════════════════════════════════════════════
    def Connexion_database(self) -> None:
        db.get_conn()
        try:
            seed.run()
        except Exception:
            logger.exception("Erreur seed.run()")

        try:
            if is_client_mode():
                from Client.api_singleton import get_api
                api = get_api()
                if api:
                    # ─── Produits ───
                    all_items = []
                    page = 1
                    while True:
                        data = api.list_produits(page=page, per_page=200, actif=1)
                        items = data.get("items", [])
                        all_items.extend(items)
                        if len(items) < 200:
                            break
                        page += 1
                    self.df_produits = pd.DataFrame(all_items)

                    if not self.df_produits.empty:
                        self.df_produits["Quantite"] = pd.to_numeric(
                            self.df_produits["Quantite"],
                            errors="coerce").fillna(0).astype(int)
                        self.df_produits["Prix_achat"] = pd.to_numeric(
                            self.df_produits["Prix_achat"], errors="coerce").fillna(0)
                        self.df_produits["Prix_vente"] = pd.to_numeric(
                            self.df_produits["Prix_vente"], errors="coerce").fillna(0)

                    self.df_client = pd.DataFrame()
                else:
                    self.df_produits = pd.DataFrame()
                    self.df_client = pd.DataFrame()
            else:
                self.df_produits = pd.read_sql(
                    "SELECT * FROM produits WHERE actif = 1 ORDER BY Nom ASC",
                    db.get_conn())
                if not self.df_produits.empty:
                    self.df_produits["Quantite"] = pd.to_numeric(
                        self.df_produits["Quantite"],
                        errors="coerce").fillna(0).astype(int)
                    self.df_produits["Prix_achat"] = pd.to_numeric(
                        self.df_produits["Prix_achat"], errors="coerce").fillna(0)
                    self.df_produits["Prix_vente"] = pd.to_numeric(
                        self.df_produits["Prix_vente"], errors="coerce").fillna(0)

                self.df_client = pd.read_sql(
                    "SELECT * FROM Client WHERE actif = 1 "
                    "ORDER BY COALESCE(C_name, nom) ASC",
                    db.get_conn())
            if (not self.df_client.empty
                    and "Montant_total" in self.df_client.columns):
                self.df_client["Montant_total"] = pd.to_numeric(
                    self.df_client["Montant_total"],
                    errors="coerce").fillna(0)

            self.df_produits_view = (
                self.df_produits.copy()
                if self.df_produits is not None else None)

            self.statusbar.showMessage("Connexion à la base réussie", 1500)
            if self._should_install_advanced_pages():
                self.Add_produit_tablewidget()

        except Exception as e:
            self.statusbar.showMessage(f"Erreur de connexion : {e}", 3000)
            logger.exception("Erreur chargement DataFrames")
            QtWidgets.QMessageBox.critical(
                self, "Erreur fatale",
                f"Impossible de charger les données :\n{e}")
            raise

    # ══════════════════════════════════════════════════════════════
    # Signaux
    # ══════════════════════════════════════════════════════════════
    def Connexion(self) -> None:
        # Navigation
        for b in self.frm_nav.findChildren(QtWidgets.QPushButton):
            b.clicked.connect(self.Changer_window)

        # ═══ Recherche rapide (sauf CAISSIER) ═══
        if (self._should_install_advanced_pages()
                and hasattr(self, "edit_recheche_rapide")):
            self.edit_recheche_rapide.textChanged.connect(
                lambda: self.Search_produit_by_code_or_name(
                    self.edit_recheche_rapide.text()))

        # ═══ Boutons articles (sauf CAISSIER) ═══
        if self._should_install_advanced_pages():
            if hasattr(self, "btn_voir_rupture_produit"):
                self.btn_voir_rupture_produit.clicked.connect(
                    self.View_rupture_stock)
            if hasattr(self, "btn_voir_tout_produit"):
                self.btn_voir_tout_produit.clicked.connect(
                    self.View_all_products)
            if hasattr(self, "btn_ajouter_produit"):
                self.btn_ajouter_produit.clicked.connect(
                    self.Add_produit_database)
            if hasattr(self, "btn_modifier_stock"):
                self.btn_modifier_stock.clicked.connect(self.Modifier_stock)
            if hasattr(self, "btn_supprimer_produit"):
                self.btn_supprimer_produit.clicked.connect(self.Delete_produit)

        # ═══ Facturation (toujours) ═══
        if hasattr(self, "btn_add_produit_for_facture"):
            self.btn_add_produit_for_facture.clicked.connect(
                self.Preparing_tablewidget_facturation)
        if hasattr(self, "btn_clear_table_facture"):
            self.btn_clear_table_facture.clicked.connect(
                self.Clear_table_facture)
        if hasattr(self, "btn_print_facture"):
            self.btn_print_facture.clicked.connect(
                self.Prepare_data_for_facture)
        if hasattr(self, "tableWidget"):
            self.tableWidget.itemChanged.connect(self.Get_total_paye)

        # ─── Bouton Rapport Z ───
        if hasattr(self, "btn_rapport_z"):
            self.btn_rapport_z.clicked.connect(self._open_rapport_z)
            logger.info("btn_rapport_z : connecté")

        # ─── Bouton Mes ventes du jour ───
        if hasattr(self, "btn_mes_ventes_jour"):
            self.btn_mes_ventes_jour.clicked.connect(self._open_mes_ventes_jour)
            logger.info("btn_mes_ventes_jour : connecté")

        # ─── Bouton Retirer la ligne ───
        if hasattr(self, "btn_remove_line_facture"):
            self.btn_remove_line_facture.clicked.connect(
                self._remove_selected_facture_line)
            logger.info("btn_remove_line_facture : connecté")

        # ═══ BLF (sauf CAISSIER) ═══
        if self._should_install_advanced_pages():
            if hasattr(self, "btn_blf_new_supplier"):
                self.btn_blf_new_supplier.clicked.connect(self.Add_fournisseur)
            if hasattr(self, "btn_blf_new_order"):
                self.btn_blf_new_order.clicked.connect(self.Recharge_stock)

            # Historique (sauf CAISSIER)
            if hasattr(self, "switch_btn"):
                self.switch_btn.clicked.connect(self.Switch_table_historique)

        # ═══ Menu ═══
        if hasattr(self, "actionSauvegarder"):
            self.actionSauvegarder.triggered.connect(self.Save_database)
        if hasattr(self, "actionConfigurations"):
            self.actionConfigurations.triggered.connect(
                self.Configuration_software)
        if hasattr(self, "actionActualiser"):
            self.actionActualiser.triggered.connect(self.Refresh_all_data)

        # Connecte les actions du menu (sauf CAISSIER)
        if self._should_install_advanced_pages():
            self._connect_menu_actions()

        # ═══ Rapport (sauf CAISSIER) ═══
        if (self._should_install_advanced_pages()
                and hasattr(self, "btn_onglet_rapport")):
            self.btn_onglet_rapport.clicked.connect(self.Open_rapports)

        # ═══ Logout (toujours) ═══
        if hasattr(self, "btn_logout"):
            self.btn_logout.clicked.connect(self.Logout)

    def _connect_menu_actions(self):
        """Connecte toutes les actions du menu."""
        # ─── Fichier ───
        self._bind("action_new_facture", self._menu_new_facture)
        self._bind("action_new_client", self._menu_new_client)
        self._bind("action_new_produit", self.Add_produit_database)
        self._bind("action_export_db", self._menu_export_db)
        self._bind("action_restore_db", self._menu_restore_db)
        self._bind("action_quit", self.close)
        self._bind("action_logout", self.Logout)

        # ─── Édition ───
        self._bind("action_actualiser", self.Refresh_all_data)
        self._bind("action_search", self._focus_search)
        self._bind("action_clear_panier", self.Clear_table_facture)

        # ─── Ventes ───
        self._bind("action_demarrer_vente", self._menu_new_facture)
        self._bind("action_ventes_jour", self._menu_ventes_jour)
        self._bind("action_rapport_z", self._open_rapport_z)

        # ─── Stock (utilise noms de boutons, plus robuste que index) ───
        self._bind("action_voir_produits", lambda: self._goto_name("btn_onglet_article"))
        self._bind("action_ruptures", self.View_rupture_stock)
        self._bind("action_new_blf", self.Recharge_stock)
        self._bind("action_new_fournisseur", self.Add_fournisseur)
        self._bind("action_voir_blf", lambda: self._goto_name("btn_onglet_blf"))

        # ─── Rapports (même page, onglets différents) ───
        self._bind("action_rapport_ventes", self._goto_rapport_ventes)
        self._bind("action_rapport_equipe", self._goto_rapport_equipe)
        self._bind("action_rapport_operations", self._goto_rapport_operations)

        # ─── Administration ───
        self._bind("action_users", lambda: self._goto_name("btn_onglet_utilisateur"))
        self._bind("action_new_user", self.Add_user)
        self._bind("action_audit", lambda: self._goto_name("btn_onglet_audit"))
        self._bind("action_backup_now", self._menu_backup_now)
        self._bind("action_manage_backups", self._menu_manage_backups)
        self._bind("action_parametres", lambda: self._goto_name("btn_onglet_parametre"))

        # ─── Aide ───
        self._bind("action_about", self._menu_about)
        self._bind("action_guide", self._menu_guide)
        self._bind("action_shortcuts", self._menu_shortcuts)

    def _bind(self, action_name: str, slot):
        try:
            action = getattr(self, action_name, None)
            if action is not None:
                action.triggered.connect(slot)
        except Exception:
            pass

    def _goto(self, index: int):
        try:
            if hasattr(self.stackedWidget, "slide_to_index"):
                self.stackedWidget.slide_to_index(index)
            else:
                self.stackedWidget.setCurrentIndex(index)
        except Exception:
            pass

    def _goto_name(self, btn_name: str):
        try:
            btn = getattr(self, btn_name, None)
            if btn is not None:
                btn.click()
        except Exception:
            logger.exception("Erreur _goto_name(%s)", btn_name)

    def _goto_rapport_ventes(self):
        """Ouvre la page Rapports puis sélectionne l'onglet Ventes."""
        self._goto_name("btn_onglet_rapport")
        if self.page_rapports is not None:
            try:
                self.page_rapports.tabs.setCurrentIndex(0)
            except Exception:
                pass

    def _goto_rapport_equipe(self):
        """Ouvre la page Rapports puis sélectionne l'onglet Équipe."""
        self._goto_name("btn_onglet_rapport")
        if self.page_rapports is not None:
            try:
                self.page_rapports.tabs.setCurrentIndex(1)
            except Exception:
                pass

    def _goto_rapport_operations(self):
        """Ouvre la page Rapports puis sélectionne l'onglet Opérations."""
        self._goto_name("btn_onglet_rapport")
        if self.page_rapports is not None:
            try:
                self.page_rapports.tabs.setCurrentIndex(2)
            except Exception:
                pass

    def _menu_new_facture(self):
        self.Clear_table_facture()
        self._goto_name("btn_onglet_facturation")

    def _menu_ventes_jour(self):
        self._goto(6)
        try:
            if self.page_historique is not None:
                self.page_historique.combo_periode.setCurrentText("Aujourd'hui")
        except Exception:
            pass

    def _menu_export_db(self):
        if self.page_parametres is not None:
            self._goto(10)
            self.page_parametres.tabs.setCurrentIndex(5)
            self.page_parametres._on_export_db()

    def _menu_restore_db(self):
        try:
            from Setting_load import Setting_load
            dlg = Setting_load(
                parent=self,
                user_id=self.user_id,
                user_name=self.identifiant)
            dlg.restauration_terminee.connect(self._on_restore_done)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture restauration")

    def _on_restore_done(self, safety_backup: str) -> None:
        logger.info("Restauration terminée, backup : %s", safety_backup)

    def _menu_backup_now(self):
        try:
            from Database import backup_engine
            path = backup_engine.create_backup(
                "manual", user_id=self.user_id, user_name=self.identifiant)
            if path:
                self.statusbar.showMessage(
                    f"Sauvegarde créée : {path}", 5000)
        except Exception:
            logger.exception("Erreur backup manuel")

    def _open_rapport_z(self) -> None:
        """Ouvre le dialogue de clôture de caisse."""
        try:
            from Setting_rapport_z import Setting_rapport_z

            # Récupère la caisse de l'utilisateur
            caisse_user = None
            try:
                row = db.query_one(
                    "SELECT numero_caisse FROM Utilisateur "
                    "WHERE id = ? LIMIT 1",
                    (self.user_id,))
                if row:
                    caisse_user = row["numero_caisse"]
            except Exception:
                pass

            dlg = Setting_rapport_z(
                parent=self,
                user_id=self.user_id,
                user_name=self.identifiant,
                role=self.role,
                is_owner=self._is_owner,
                is_developer=self._is_developer,
                caisse_utilisateur=caisse_user)
            dlg.rapport_z_genere.connect(self._on_rapport_z_genere)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture Rapport Z")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir le rapport Z.")

    def _open_mes_ventes_jour(self) -> None:
        """Ouvre le dialogue des ventes du caissier."""
        try:
            from Setting_mes_ventes import Setting_mes_ventes
            dlg = Setting_mes_ventes(
                parent=self,
                user_id=self.user_id,
                user_name=self.identifiant,
                role=self.role,
                is_owner=self._is_owner,
                is_developer=self._is_developer)
            dlg.vente_annulee.connect(self._on_vente_annulee)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture mes ventes")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir la liste des ventes.")

    def _on_vente_annulee(self, num_fact: str) -> None:
        """Callback après une annulation de vente."""
        logger.info("Vente annulée : %s", num_fact)
        # Rafraîchit les vues si nécessaire
        self.Load_data_onglet_1()

    def _on_rapport_z_genere(self, path_pdf: str) -> None:
        logger.info("Rapport Z généré : %s", path_pdf)
        self.statusbar.showMessage(
            f"Rapport Z généré : {os.path.basename(path_pdf)}", 6000)

    def _menu_manage_backups(self):
        try:
            from Setting_backup_manager import Setting_backup_manager
            dlg = Setting_backup_manager(
                parent=self, user_id=self.user_id,
                user_name=self.identifiant)
            dlg.exec()
        except Exception:
            logger.exception("Erreur gestionnaire backups")

    def _focus_search(self):
        if hasattr(self, "edit_recheche_rapide"):
            self.edit_recheche_rapide.setFocus()
            self.edit_recheche_rapide.selectAll()

    def _menu_about(self):
        QtWidgets.QMessageBox.about(
            self, "À propos de Nova Pharma",
            "<h3>Nova Pharma v2.0.0</h3>"
            "<p>Logiciel de gestion pour pharmacies.</p>"
            "<p><b>Développé par :</b> TEAM NOVA</p>"
            "<p><b>Email :</b> teamnovaoff@gmail.com</p>"
            "<p><b>Tél. :</b> 08 XX XX XX XX</p>"
            "<p><b>Licence :</b> Propriétaire</p>"
            "<p style='color:#94a3b8;font-size:10px;'>"
            "© 2026 TEAM NOVA — Tous droits réservés</p>")

    def _menu_guide(self):
        try:
            pdf_path = "Guide_utilisateur_NovaPharma.pdf"

            if not os.path.isfile(pdf_path):
                rep = QtWidgets.QMessageBox.question(
                    self, "Guide manquant",
                    "Le guide utilisateur n'a pas encore été généré.\n\n"
                    "Voulez-vous le créer maintenant ?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.Yes)
                if rep != QtWidgets.QMessageBox.Yes:
                    return

                try:
                    from docs.generer_doc import generer_guide
                    generer_guide(pdf_path)
                except Exception as e:
                    logger.exception("Erreur génération guide")
                    QtWidgets.QMessageBox.critical(
                        self, "Erreur",
                        f"Impossible de générer le guide :\n{e}")
                    return

            QtGui.QDesktopServices.openUrl(
                QtCore.QUrl.fromLocalFile(os.path.abspath(pdf_path)))

        except Exception:
            logger.exception("Erreur ouverture guide")

    def _menu_new_client(self):
        self._goto(3)
        try:
            from Setting_client_dialog import Setting_client_dialog
            dlg = Setting_client_dialog(
                parent=self,
                user_id=self.user_id)
            dlg.client_saved.connect(lambda _: (
                self.page_clients.refresh()
                if self.page_clients else None))
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture dialogue nouveau client")

    def _diagnose_overlay(self):
        """Trouve quel widget capture les clics."""
        try:
            import logging
            logger = logging.getLogger(__name__)

            logger.info("=" * 60)
            logger.info("DIAGNOSTIC OVERLAY")
            logger.info("=" * 60)

            # Teste la zone basse de la fenêtre (là où sont les onglets)
            w = self.width()
            h = self.height()

            points = [
                (w // 2, h - 100),      # bas centre
                (w // 2, h // 2),       # centre
                (w - 200, h - 200),     # bas droite
                (200, h - 200),         # bas gauche
            ]

            for (x, y) in points:
                child = self.childAt(x, y)
                if child:
                    logger.info(
                        "Point (%d, %d) → %s (%s)",
                        x, y,
                        child.objectName() or "(sans nom)",
                        child.__class__.__name__)

                    # Remonte la chaîne
                    p = child.parent()
                    depth = 0
                    while p and depth < 5:
                        logger.info(
                            "    parent[%d] : %s (%s) geo=%s",
                            depth,
                            p.objectName() or "(sans nom)",
                            p.__class__.__name__,
                            p.geometry())
                        p = p.parent()
                        depth += 1
                else:
                    logger.info("Point (%d, %d) → self (MainWindow)", x, y)

            logger.info("=" * 60)
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════════
    # UI helpers
    # ══════════════════════════════════════════════════════════════
    def Add_Shadow(self, widget, radius: int = 15, offset: int = 5) -> None:
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(radius)
        shadow.setOffset(offset, offset)
        shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        widget.setGraphicsEffect(shadow)

    def Applique_fonction(self) -> None:
        # Ombres navigation
        try:
            for btn in self.frm_nav.findChildren(QtWidgets.QPushButton):
                self.Add_Shadow(btn, 40, offset=3)
        except Exception:
            logger.exception("Erreur ombres navigation")

        # Ombres hero
        frame_hero = getattr(self, "frame_5", None)
        if frame_hero is not None:
            try:
                for btn in frame_hero.findChildren(QtWidgets.QPushButton):
                    self.Add_Shadow(btn)
            except Exception:
                logger.exception("Erreur ombres hero")

        # Ombres frames spécifiques
        for name, radius, offset in (
            ("frame", 5, 1),
            ("frame_20", 5, 1),
            ("frame_22", 5, 1),
        ):
            widget = getattr(self, name, None)
            if widget is not None:
                try:
                    self.Add_Shadow(widget, radius, offset)
                except Exception:
                    logger.exception("Erreur ombre %s", name)

        # Autocomplétion produits — FACTURATION (tous les rôles)
        self._setup_facturation_completer()

        # Autocomplétion clients — DÉSACTIVÉE sur edit_name_client
        # (le popup QCompleter bloquait le clic sur btn_register_new_client)
        try:
            if hasattr(self, "edit_name_client"):
                self.edit_name_client.setCompleter(None)
        except Exception:
            logger.exception("Erreur neutralisation completer client")

        # Icônes loupe
        icon_search = getattr(self, "icon_search", None)
        if icon_search is not None:
            for name in ("edit_recheche_rapide",
                         "edit_recherche_produit",
                         "edit_blf_search"):
                edit = getattr(self, name, None)
                if edit is not None:
                    try:
                        edit.addAction(
                            icon_search,
                            QtWidgets.QLineEdit.LeadingPosition)
                    except Exception:
                        pass

    def Suggestion(self, suggestion: list, widget) -> None:
        completer = QtWidgets.QCompleter(suggestion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        completer.setMaxVisibleItems(10)
        widget.setCompleter(completer)

    def Valeur_existe(self, table: QtWidgets.QTableWidget,
                      col: int, valeur) -> bool:
        for row in range(table.rowCount()):
            item = table.item(row, col)
            if item and item.text() == valeur:
                return True
        return False

    # ══════════════════════════════════════════════════════════════
    # Temps
    # ══════════════════════════════════════════════════════════════
    def Get_time(self) -> None:
        """Affiche l'heure (serveur si client synchronisé, locale sinon).

        Pas d'appel HTTP ici : l'offset est calculé par _refresh_server_badge
        (toutes les 30 s) et réutilisé.
        """
        if not hasattr(self, "lbl_temps"):
            return

        from datetime import datetime as dt, timedelta

        offset = getattr(self, "_server_time_offset", None)
        if is_client_mode() and offset is not None:
            srv_dt = dt.now() + timedelta(seconds=offset)
            heure = srv_dt.strftime("%H:%M:%S")
            date = srv_dt.strftime("%A %d/%m/%Y")
        else:
            heure = time.strftime("%H:%M:%S")
            date = time.strftime("%A %d/%m/%Y")

        html = f"""
            <html><body>
                <p align="right">
                    <span style="font-size:10pt; font-weight:700;">{heure}<br/></span>
                    <span style="font-size:8pt; color:#94a3b8;">{date.upper()}</span>
                </p>
            </body></html>
        """
        self.lbl_temps.setText(html)

    def Get_current_week(self) -> list:
        try:
            d, m, y = map(int, time.strftime("%d/%m/%Y").split("/"))
            for week in calendar.monthcalendar(y, m):
                if d in week:
                    return [x for x in week if x > 0]
            return []
        except Exception:
            logger.exception("Erreur Get_current_week")
            return []

    # ══════════════════════════════════════════════════════════════
    # Dashboard
    # ══════════════════════════════════════════════════════════════
    def Load_data_onglet_1(self) -> None:
        if self._is_caissier_restricted():
            return
        try:
            periode = self.config_file_json.get("chiffre_affaire", "Mois")
            if hasattr(self, "label_10"):
                self.label_10.setText(
                    "CHIFFRE D'AFFAIRE DU MOIS" if periode == "Mois"
                    else "CHIFFRE D'AFFAIRE DE LA SEMAINE")

            row = db.query_one("SELECT COUNT(*) AS n FROM Client")
            n_clients = int(row["n"] or 0) if row else 0
            if hasattr(self, "label_20"):
                self.label_20.setText(str(n_clients))

            seuil = 20
            try:
                seuil = int(db.get_config("seuil_stock", 20))
            except Exception:
                seuil = 20

            row = db.query_one(
                "SELECT COUNT(*) AS n FROM produits "
                "WHERE actif = 1 AND Quantite <= ?",
                (seuil,))
            n_rupture = int(row["n"] or 0) if row else 0
            if hasattr(self, "label_17"):
                self.label_17.setText(str(n_rupture))

            rows = db.query("SELECT * FROM Historique ORDER BY Date_vent ASC")
            nbr_vente = 0
            montant_total = 0.0
            cur_month = int(time.strftime("%m"))
            cur_year = time.strftime("%Y")
            cur_week = self.Get_current_week()

            for r in rows:
                try:
                    dv = str(r["Date_vent"]).split("/")
                    if len(dv) < 3:
                        continue
                    d, m, y = int(dv[0]), int(dv[1]), dv[2]
                    if periode == "Mois":
                        match = (m == cur_month and cur_year in y)
                    else:
                        match = (d in cur_week and m == cur_month
                                 and cur_year in y)
                    if match:
                        montant_total += float(r["Total"])
                        nbr_vente += 1
                except (ValueError, TypeError, IndexError, KeyError):
                    continue

            if hasattr(self, "label_11"):
                self.label_11.setText(f"{montant_total:,.0f} {self.devise}")
            if hasattr(self, "label_14"):
                self.label_14.setText(str(nbr_vente))

        except Exception:
            logger.exception("Erreur Load_data_onglet_1")

    # ══════════════════════════════════════════════════════════════
    # Configuration des tables
    # ══════════════════════════════════════════════════════════════
    def Setting_table_widget(self) -> None:
        if hasattr(self, "tableWidget"):
            try:
                h = self.tableWidget.horizontalHeader()
                h.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                for i in range(1, 4):
                    h.setSectionResizeMode(
                        i, QtWidgets.QHeaderView.ResizeToContents)
            except Exception:
                logger.exception("Erreur config tableWidget")

        if hasattr(self, "tableWidget_4"):
            try:
                h4 = self.tableWidget_4.horizontalHeader()
                h4.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                for i in (3, 4, 5, 6, 7, 8):
                    h4.setSectionResizeMode(
                        i, QtWidgets.QHeaderView.ResizeToContents)
            except Exception:
                logger.exception("Erreur config tableWidget_4")

        if hasattr(self, "tableWidget_5"):
            try:
                h5 = self.tableWidget_5.horizontalHeader()
                h5.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                for i in (3, 4, 5, 6, 7, 8):
                    h5.setSectionResizeMode(
                        i, QtWidgets.QHeaderView.ResizeToContents)
            except Exception:
                logger.exception("Erreur config tableWidget_5")

        if hasattr(self, "tbw_blf_lignes"):
            try:
                self.tbw_blf_lignes.horizontalHeader().setSectionResizeMode(
                    QtWidgets.QHeaderView.Stretch)
            except Exception:
                logger.exception("Erreur config tbw_blf_lignes")

        if hasattr(self, "tbw_voir_produit"):
            try:
                ph = self.tbw_voir_produit.horizontalHeader()
                ph.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                ph.setSectionResizeMode(
                    1, QtWidgets.QHeaderView.ResizeToContents)
                self.tbw_voir_produit.verticalHeader().setVisible(False)
                self.tbw_voir_produit.verticalHeader().setDefaultSectionSize(60)
                self.tbw_voir_produit.setShowGrid(False)
                self.tbw_voir_produit.setSelectionBehavior(
                    QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
                self.tbw_voir_produit.setSelectionMode(
                    QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
                self.tbw_voir_produit.setAlternatingRowColors(True)
            except Exception:
                logger.exception("Erreur config tbw_voir_produit")

    @staticmethod
    @lru_cache(maxsize=32)
    def _get_stock_color(quantite: int) -> str:
        if quantite > 50:
            return "#10b981"
        if quantite > 20:
            return "#f59e0b"
        return "#ef4444"

    def _create_styled_item(self, text: str,
                            font_name: str = "Arial",
                            font_size: int = 10,
                            bold: bool = False,
                            color: str = "#1e293b",
                            bg_color: str = None,
                            alignment: int = None) -> QtWidgets.QTableWidgetItem:
        item = QtWidgets.QTableWidgetItem(str(text))
        font = QtGui.QFont(font_name, font_size)
        font.setBold(bold)
        item.setFont(font)
        item.setForeground(QtGui.QColor(color))
        if bg_color:
            item.setBackground(QtGui.QColor(bg_color))
        if alignment:
            item.setTextAlignment(alignment)
        return item

    def Add_produit_tablewidget(self) -> None:
        if not hasattr(self, "tbw_voir_produit"):
            return

        df = self.df_produits_view
        if df is None or df.empty:
            self.tbw_voir_produit.setRowCount(0)
            return

        self.tbw_voir_produit.setRowCount(0)
        align_c = (QtCore.Qt.AlignmentFlag.AlignCenter |
                   QtCore.Qt.AlignmentFlag.AlignVCenter)
        align_l = (QtCore.Qt.AlignmentFlag.AlignLeft |
                   QtCore.Qt.AlignmentFlag.AlignVCenter)

        required = ["Code_reference", "Nom", "Categorie", "Quantite",
                    "Prix_achat", "Prix_vente", "Prix_unitaire", "Date_ajout"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            logger.error("Colonnes manquantes dans df_produits : %s", missing)
            logger.error("Colonnes disponibles : %s", list(df.columns))
            return

        for i, (_, r) in enumerate(df.iterrows()):
            self.tbw_voir_produit.insertRow(i)

            def _get(col, default=""):
                v = r.get(col, default)
                return str(v) if v is not None else str(default)

            try:
                self.tbw_voir_produit.setItem(i, 0, self._create_styled_item(
                    _get("Code_reference"), "Courier New", 9, False,
                    "#94a3b8", alignment=align_l))

                self.tbw_voir_produit.setItem(i, 1, self._create_styled_item(
                    _get("Nom"), "Segoe UI", 10, True, "#1e293b",
                    alignment=align_l))

                self.tbw_voir_produit.setItem(i, 2, self._create_styled_item(
                    _get("Categorie").upper(), "Arial", 8, True, "#64748b",
                    "#e2e8f0", align_c))

                q = int(r.get("Quantite") or 0)
                self.tbw_voir_produit.setItem(i, 3, self._create_styled_item(
                    str(q), "Arial", 10, True, self._get_stock_color(q),
                    alignment=align_c))

                self.tbw_voir_produit.setItem(i, 4, self._create_styled_item(
                    f"{r.get('Prix_achat', 0)} {self.devise}",
                    "Arial", 9, False, "#64748b", alignment=align_c))

                self.tbw_voir_produit.setItem(i, 5, self._create_styled_item(
                    f"{r.get('Prix_vente', 0)} {self.devise}",
                    "Arial", 10, True, "#2563eb", alignment=align_c))

                self.tbw_voir_produit.setItem(i, 6, self._create_styled_item(
                    f"{r.get('Prix_unitaire', 0)} {self.devise}",
                    "Arial", 9, True, "#1e293b", alignment=align_c))

                self.tbw_voir_produit.setItem(i, 7, self._create_styled_item(
                    _get("Expiration", "—") or "—", "Arial", 9, False,
                    "#64748b", alignment=align_c))

                self.tbw_voir_produit.setItem(i, 8, self._create_styled_item(
                    _get("Date_ajout"), "Arial", 8, False, "#94a3b8",
                    alignment=align_c))

            except Exception:
                logger.exception("Erreur ligne %d produit", i)
                continue

        logger.info("Table produits remplie : %d lignes",
                    self.tbw_voir_produit.rowCount())

    # ══════════════════════════════════════════════════════════════
    # Filtres / recherche produits
    # ══════════════════════════════════════════════════════════════
    def _afficher_donnees_filtrees(self, df: pd.DataFrame) -> None:
        self.df_produits_view = df
        self.Add_produit_tablewidget()

    def _reload_produits_master(self) -> None:
        try:
            self.df_produits = pd.read_sql(
                "SELECT * FROM produits WHERE actif = 1 ORDER BY Nom ASC",
                db.get_conn())
            self.df_produits["Quantite"] = pd.to_numeric(
                self.df_produits["Quantite"],
                errors="coerce").fillna(0).astype(int)
            self.df_produits_view = self.df_produits.copy()
        except Exception:
            logger.exception("Erreur reload produits")

    def View_all_products(self) -> None:
        self._reload_produits_master()
        self.Add_produit_tablewidget()

    def View_rupture_stock(self) -> None:
        try:
            if self.df_produits is None:
                self._reload_produits_master()

            if self.df_produits is None or self.df_produits.empty:
                notify.warning("Aucun produit en base.")
                return

            try:
                seuil = int(db.get_config("seuil_stock", 20))
            except Exception:
                seuil = 20

            if getattr(self, "search_article", None) is not None:
                self.search_article.blockSignals(True)
                self.search_article.clear()
                self.search_article.blockSignals(False)

            if getattr(self, "edit_recheche_rapide", None) is not None:
                self.edit_recheche_rapide.blockSignals(True)
                self.edit_recheche_rapide.clear()
                self.edit_recheche_rapide.blockSignals(False)

            df_filtre = self.df_produits[
                self.df_produits["Quantite"] <= seuil]

            if df_filtre.empty:
                notify.info(
                    f"Aucun produit en rupture (seuil ≤ {seuil}).")
            else:
                notify.info(
                    f"{len(df_filtre)} produit(s) avec stock ≤ {seuil}.")

            self._afficher_donnees_filtrees(df_filtre)

        except Exception:
            logger.exception("Erreur View_rupture_stock")
            notify.danger("Impossible de filtrer les ruptures.")

    def Search_produit_by_code_or_name(self, terme: str) -> None:
        if self._is_caissier_restricted():
            return
        if self.df_produits is None:
            return
        terme = (terme or "").strip()
        if not terme:
            self.df_produits_view = self.df_produits.copy()
            self.Add_produit_tablewidget()
            return
        mask = (
            self.df_produits["Code_reference"].str.contains(
                terme, case=False, na=False) |
            self.df_produits["Nom"].str.contains(
                terme, case=False, na=False)
        )
        self._afficher_donnees_filtrees(self.df_produits[mask])

    # ══════════════════════════════════════════════════════════════
    # Facturation — Sélecteur client (regex + recherche live)
    # ══════════════════════════════════════════════════════════════
    def _setup_client_selector(self) -> None:
        """Configure le sélecteur client (facturation).

        Les widgets sont désormais dans page_facturation, aliasés au
        MainWindow via _install_page_facturation(). Ce code n'a donc
        pas besoin d'être modifié.
        """
        try:
            # ─── Label de statut ───
            self.label_client_status = QtWidgets.QLabel(
                "Vente anonyme — aucun client associé")
            self.label_client_status.setObjectName("label_client_status")
            self.label_client_status.setStyleSheet(
                "color: #94a3b8; font-size: 11px; font-weight: 600; "
                "background: transparent; padding: 2px 0;")

            if hasattr(self, "verticalLayout_12"):
                self.verticalLayout_12.addWidget(self.label_client_status)

            # ─── Bouton "Créer ce client" ───
            if hasattr(self, "btn_register_new_client"):
                btn = self.btn_register_new_client
                btn.setVisible(False)
                btn.setCursor(QtCore.Qt.PointingHandCursor)
                btn.setEnabled(True)
                btn.setAttribute(
                    QtCore.Qt.WA_TransparentForMouseEvents, False)

                if not getattr(self, "_client_btn_connected", False):
                    try:
                        btn.clicked.connect(
                            self._on_register_new_client_clicked)
                        self._client_btn_connected = True
                        logger.info(
                            "btn_register_new_client : signal connecté")
                    except Exception:
                        logger.exception(
                            "Impossible de connecter btn_register_new_client")

                btn.raise_()

            # ─── Champ téléphone client ───
            if hasattr(self, "edit_name_client"):
                self.edit_name_client.setPlaceholderText(
                    "Ex : 0XXXXXXXXX  (vide = vente anonyme)")
                self.edit_name_client.setClearButtonEnabled(True)

                # Neutralise le completer (bug de clic)
                try:
                    self.edit_name_client.setCompleter(None)
                except Exception:
                    pass

                self.edit_name_client.returnPressed.connect(
                    lambda : self._on_client_input_changed(self.edit_name_client.text()))

            if hasattr(self, "label_7"):
                self.label_7.setText("Numéro du client")

            if hasattr(self, "btn_recheche_person_facture"):
                self.btn_recheche_person_facture.setText("Confirmer")
                self.btn_recheche_person_facture.setVisible(False)

            for name in ("edit_identification_client", "edit_numero_client"):
                w = getattr(self, name, None)
                if w is not None:
                    w.setPlaceholderText("—")

            logger.info("Sélecteur client configuré")

        except Exception:
            logger.exception("Erreur _setup_client_selector")

    def _on_register_new_client_clicked(self) -> None:
        """Slot dédié au clic du bouton 'Créer ce client'."""
        logger.info("→ Bouton 'Créer ce client' cliqué")
        try:
            self.Insert_new_person_database_users_option()
        except Exception:
            logger.exception("Erreur création client")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir le formulaire client.")

    def _on_client_input_changed(self, text: str) -> None:
        text = (text or "").strip()

        if not text:
            self._set_client_status("anonyme")
            self.edit_identification_client.setText("")
            self.edit_numero_client.setText("")
            self._current_client_id = None
            if hasattr(self, "btn_register_new_client"):
                self.btn_register_new_client.setVisible(False)
            return

        numero = text.replace(" ", "").replace("-", "").replace(".", "")

        try:
            client = self._find_client_by_numero(numero)

            if client:
                nom = client.get("nom") or "—"
                num = client.get("numero") or numero
                self._current_client_id = client.get("id")
                self._set_client_status("found", nom)
                self.edit_identification_client.setText(nom)
                self.edit_numero_client.setText(num)
                if hasattr(self, "btn_register_new_client"):
                    self.btn_register_new_client.setVisible(False)
                return

            self._current_client_id = None

            # Numéro valide mais inconnu
            if PHONE_REGEX.match(numero):
                self._set_client_status("not_found")
                self.edit_identification_client.setText("")
                self.edit_numero_client.setText("")

                # Ferme tout popup d'autocomplétion
                try:
                    comp = self.edit_name_client.completer()
                    if comp is not None:
                        popup = comp.popup()
                        if popup is not None:
                            popup.close()
                            popup.hide()
                except Exception:
                    pass

                if hasattr(self, "btn_register_new_client"):
                    btn = self.btn_register_new_client
                    btn.setVisible(True)
                    btn.setEnabled(True)
                    btn.raise_()
            else:
                self._set_client_status("invalid")
                self.edit_identification_client.setText("")
                self.edit_numero_client.setText("")
                if hasattr(self, "btn_register_new_client"):
                    self.btn_register_new_client.setVisible(False)

        except Exception:
            logger.exception("Erreur recherche client live")
            self._set_client_status("error")

    def _find_client_by_numero(self, numero: str):
        """Recherche un client par numéro (mode client → API)."""
        if not numero:
            return None

        # ═══ MODE CLIENT → API ═══
        if is_client_mode():
            try:
                api = get_api()
                client = api.find_client_by_numero(numero)
                if client:
                    return {
                        "id": client.get("id"),
                        "nom": client.get("nom"),
                        "numero": client.get("numero"),
                    }
            except Exception:
                # 404 = client non trouvé → comportement normal
                return None

        # ═══ MODE AUTONOME / SERVEUR → DB locale ═══
        client = db.query_one(
            "SELECT id, COALESCE(C_name, nom) AS nom, numero "
            "FROM Client WHERE numero = ? AND actif = 1 LIMIT 1",
            (numero,))
        if client:
            return dict(client)

        variantes = []
        if numero.startswith("+243") and len(numero) == 13:
            variantes.append("0" + numero[4:])
        elif numero.startswith("0") and len(numero) == 10:
            variantes.append("+243" + numero[1:])

        for var in variantes:
            client = db.query_one(
                "SELECT id, COALESCE(C_name, nom) AS nom, numero "
                "FROM Client WHERE numero = ? AND actif = 1 LIMIT 1",
                (var,))
            if client:
                return dict(client)

        return None

    def _set_client_status(self, status: str, nom: str = "") -> None:
        if not hasattr(self, "label_client_status"):
            return

        styles = {
            "anonyme": (
                "Vente anonyme — aucun client associé",
                "color: #94a3b8; font-size: 11px; font-weight: 600; "
                "background: transparent; padding: 2px 0;"),
            "found": (
                f"Client identifié : {nom}",
                "color: #16A34A; font-size: 11px; font-weight: 700; "
                "background: transparent; padding: 2px 0;"),
            "not_found": (
                "Numéro non enregistré — cliquez sur « Créer ce client » "
                "ou laissez vide pour anonyme",
                "color: #ea580c; font-size: 11px; font-weight: 600; "
                "background: transparent; padding: 2px 0;"),
            "invalid": (
                "Format invalide (ex : +243XXXXXXXXX ou 0XXXXXXXXX)",
                "color: #dc2626; font-size: 11px; font-weight: 600; "
                "background: transparent; padding: 2px 0;"),
            "error": (
                "Erreur de recherche",
                "color: #dc2626; font-size: 11px; font-weight: 600; "
                "background: transparent; padding: 2px 0;"),
        }

        text, style = styles.get(status, styles["anonyme"])
        self.label_client_status.setText(text)
        self.label_client_status.setStyleSheet(style)

    def Insert_new_person_database_users_option(self) -> None:
        """Ouvre le dialogue de création d'un nouveau client."""
        try:
            from Setting_client_dialog import Setting_client_dialog
        except Exception as e:
            logger.exception("Impossible d'importer Setting_client_dialog")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'ouvrir le formulaire client.\n\n"
                f"Vérifiez que ces fichiers existent :\n"
                f"• Setting_client_dialog.py\n"
                f"• Interface_client_dialog.py\n\n"
                f"Détails : {e}")
            return

        try:
            numero = self.edit_name_client.text().strip().replace(" ", "")
            dlg = Setting_client_dialog(parent=self, user_id=self.user_id)

            if numero and PHONE_REGEX.match(numero):
                dlg.input_numero.setText(numero)

            def on_saved(client_id):
                try:
                    # ─── MODE CLIENT → API ───
                    if is_client_mode():
                        api = get_api()
                        client = api.get_client(client_id)
                        if client and client.get("numero"):
                            num = str(client["numero"])
                            self.edit_name_client.setText(num)
                            # Redéclenche la recherche live pour
                            # que le nom s'affiche
                            self._on_client_input_changed(num)
                        return

                    # ─── MODE AUTONOME / SERVEUR → DB locale ───
                    row = db.query_one(
                        "SELECT COALESCE(C_name, nom) AS nom, numero "
                        "FROM Client WHERE id = ? LIMIT 1",
                        (client_id,))
                    if row and row["numero"]:
                        self.edit_name_client.setText(str(row["numero"]))
                except Exception:
                    logger.exception("Erreur rechargement client créé")

            dlg.client_saved.connect(on_saved)

            result = dlg.exec()
            if result != QtWidgets.QDialog.Accepted:
                logger.info("Création client annulée")

        except Exception as e:
            logger.exception("Erreur ouverture dialogue création client")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'ouvrir le formulaire client :\n{e}")

    def Preparing_tablewidget_facturation(self) -> None:
        if not hasattr(self, "tableWidget"):
            return

        # ─── Priorité 1 : produit sélectionné dans le completer ───
        produit = getattr(self, "_produit_selectionne", None)

        # ─── Fallback : recherche par texte ───
        if not produit:
            nom = self.edit_recherche_produit.text().strip()
            if not nom:
                return
            produit = self._lookup_product_for_facture(nom)
            if not produit:
                QtWidgets.QMessageBox.warning(
                    self, "Produit introuvable",
                    f"Aucun produit trouvé pour « {nom} ».")
                return

        nom = produit.get("Nom") or ""
        code_ref = produit.get("Code_reference") or "—"
        if not nom:
            return

        # ─── Doublon : incrémente la quantité ───
        for r in range(self.tableWidget.rowCount()):
            it = self.tableWidget.item(r, 0)
            # Compare sur le nom (colonne 0)
            if it and it.text() == nom:
                w = self.tableWidget.cellWidget(r, 1)
                if w is not None:
                    new_q = w.value() + self.spin_quantite_facture.value()
                    w.setValue(min(new_q, w.maximum()))
                    self.Get_total_paye()
                self._reset_produit_selection()
                return

        # ─── Nouvelle ligne ───
        self.Set_limite_quantite()
        tb_row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(tb_row + 1)

        prix_unitaire = float(
            produit.get("Prix_unitaire")
            or produit.get("Prix_vente") or 0)

        # Colonne 0 : Désignation (= nom)
        self.tableWidget.setItem(
            tb_row, 0, QtWidgets.QTableWidgetItem(nom))

        # Colonne 1 : Qté (spinbox)
        spin = QtWidgets.QSpinBox()
        spin.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        stock = int(produit.get("Quantite") or 0)
        spin.setMaximum(max(1, stock))
        spin.setValue(self.spin_quantite_facture.value())
        spin.valueChanged.connect(self.Get_total_paye)
        spin.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.tableWidget.setCellWidget(tb_row, 1, spin)

        # Colonne 2 : P.U
        item_pu = QtWidgets.QTableWidgetItem(str(prix_unitaire))
        item_pu.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.tableWidget.setItem(tb_row, 2, item_pu)

        # Colonne 3 : Total ligne
        total_ligne = spin.value() * prix_unitaire
        item_tot = QtWidgets.QTableWidgetItem(str(total_ligne))
        item_tot.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.tableWidget.setItem(tb_row, 3, item_tot)

        # Store le code_ref en UserRole pour usage futur
        self.tableWidget.item(tb_row, 0).setData(
            QtCore.Qt.UserRole, code_ref)

        # Reset sélection + vide champ
        self._reset_produit_selection()
        self.Get_total_paye()

    def _reset_produit_selection(self) -> None:
        """Reset le produit sélectionné + vide le champ."""
        self._produit_selectionne = None
        if hasattr(self, "edit_recherche_produit"):
            self.edit_recherche_produit.blockSignals(True)
            self.edit_recherche_produit.clear()
            self.edit_recherche_produit.blockSignals(False)

    def _lookup_product_for_facture(self, nom: str):
        """Retourne dict {Nom, Code_reference, Quantite, Prix_unitaire, Prix_vente}."""
        if is_client_mode():
            try:
                api = get_api()
                result = api.list_produits(search=nom, per_page=10)
                for it in result.get("items", []):
                    if it.get("Nom") == nom:
                        return it
            except Exception:
                logger.exception("Erreur lookup produit API")
            return None

        try:
            row = db.query_one(
                "SELECT Nom, Code_reference, Quantite, Prix_unitaire, Prix_vente "
                "FROM produits WHERE Nom = ? AND actif = 1 LIMIT 1",
                (nom,))
            return dict(row) if row else None
        except Exception:
            logger.exception("Erreur lookup produit local")
            return None

    def Set_limite_quantite(self) -> None:
        nom = self.edit_recherche_produit.text().strip()
        if not nom:
            return

        # ─── MODE CLIENT → API ───
        if is_client_mode():
            try:
                api = get_api()
                result = api.list_produits(search=nom, per_page=5)
                for it in result.get("items", []):
                    if it.get("Nom") == nom:
                        q = int(it.get("Quantite") or 0)
                        self.spin_quantite_facture.setMaximum(max(q, 1))
                        self.spin_nbr_stock.setValue(q)
                        return
            except Exception:
                logger.exception("Erreur Set_limite_quantite (API)")
            return

        # ─── MODE AUTONOME / SERVEUR → DB locale ───
        try:
            row = db.query_one(
                "SELECT Quantite FROM produits WHERE Nom = ? LIMIT 1",
                (nom,))
            if row:
                q = int(row["Quantite"])
                self.spin_quantite_facture.setMaximum(max(q, 1))
                self.spin_nbr_stock.setValue(q)
        except Exception:
            logger.exception("Erreur Set_limite_quantite")

    def _find_row_of_widget(self, widget) -> int:
        for r in range(self.tableWidget.rowCount()):
            if self.tableWidget.cellWidget(r, 1) is widget:
                return r
        return -1

    def Get_total_paye(self) -> None:
        try:
            sender = self.sender()
            row = self._find_row_of_widget(sender) if sender else -1

            if row >= 0:
                pu_item = self.tableWidget.item(row, 2)
                if pu_item:
                    try:
                        pu = float(pu_item.text())
                        total = sender.value() * pu
                        self.tableWidget.blockSignals(True)
                        self.tableWidget.setItem(
                            row, 3,
                            QtWidgets.QTableWidgetItem(str(total)))
                        self.tableWidget.blockSignals(False)
                    except ValueError:
                        pass

            total_general = 0.0
            total_articles = 0
            for r in range(self.tableWidget.rowCount()):
                t = self.tableWidget.item(r, 3)
                w = self.tableWidget.cellWidget(r, 1)
                if t:
                    try:
                        total_general += float(t.text())
                    except ValueError:
                        pass
                if w is not None:
                    total_articles += int(w.value())

            if hasattr(self, "lbl_totale_calc"):
                self.lbl_totale_calc.setText(
                    self._fmt_dual(total_general))
            if hasattr(self, "lbl_total_nbr_produit"):
                self.lbl_total_nbr_produit.setText(str(total_articles))

        except Exception:
            logger.exception("Erreur Get_total_paye")

    def Clear_table_facture(self) -> None:
        if hasattr(self, "tableWidget"):
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)

    def _remove_selected_facture_line(self) -> None:
        """Retire la ligne actuellement sélectionnée du panier."""
        if not hasattr(self, "tableWidget"):
            return
        row = self.tableWidget.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.information(
                self, "Aucune ligne sélectionnée",
                "Cliquez sur une ligne du panier pour la sélectionner, "
                "puis cliquez sur « Retirer la ligne ».")
            return
        self.tableWidget.removeRow(row)
        self.Get_total_paye()
        logger.info("Ligne retirée du panier : index %d", row)

    def Add_produit_database(self) -> None:
        self._require_perm("ajouter_produit")
        try:
            self.win1 = Add_produit(user_id=self.user_id)
            if self.win1.exec() == QtWidgets.QDialog.Accepted:
                self._reload_produits_master()
                self.Add_produit_tablewidget()
                self.Load_data_onglet_1()
                notify.success("Produit ajouté avec succès.")
        except PermissionDeniedError as e:
            notify.danger(f"Accès refusé : {e}")
        except Exception:
            logger.exception("Erreur Add_produit_database")
            notify.danger("Impossible d'ajouter le produit.")

    def _decrement_stock(self, nom_produit: str, qte: int,
                         numero_facture: str = "") -> None:
        """Décrémente le stock ET trace dans MouvementStock."""
        row = db.query_one(
            "SELECT Code_reference, Quantite FROM produits "
            "WHERE Nom = ? LIMIT 1",
            (nom_produit,))
        if row is None:
            raise ValueError(f"Produit introuvable : {nom_produit}")

        code_ref = row["Code_reference"]
        stock_avant = int(row["Quantite"])
        if stock_avant < qte:
            raise ValueError(
                f"Stock insuffisant pour {nom_produit} "
                f"(demandé : {qte}, dispo : {stock_avant})")
        stock_apres = stock_avant - qte

        db.execute(
            "UPDATE produits SET Quantite = ? WHERE Code_reference = ?",
            (stock_apres, code_ref))

        # ─── Trace dans MouvementStock ───
        uid_valide = None
        if self.user_id:
            try:
                if db.query_one(
                        "SELECT 1 FROM Utilisateur WHERE id = ? LIMIT 1",
                        (self.user_id,)
                ):
                    uid_valide = self.user_id
            except Exception:
                pass

        try:
            db.execute(
                """INSERT INTO MouvementStock
                   (id, produit_id, type, quantite,
                    stock_avant, stock_apres, motif, utilisateur_id)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (db.new_id(), code_ref, "SORTIE", qte,
                 stock_avant, stock_apres,
                 f"Vente {numero_facture}" if numero_facture else "Vente",
                 uid_valide))
        except Exception:
            logger.exception(
                "Échec écriture MouvementStock (vente %s, produit %s)",
                numero_facture, code_ref)

    def Prepare_data_for_facture(self) -> None:
        if not hasattr(self, "tableWidget") or self.tableWidget.rowCount() == 0:
            QtWidgets.QMessageBox.warning(
                self, "Panier vide",
                "Ajoutez au moins un article avant d'imprimer.")
            return

        # ─── 1. Panier ───
        panier = []
        try:
            for r in range(self.tableWidget.rowCount()):
                nom_item = self.tableWidget.item(r, 0)
                qte_widget = self.tableWidget.cellWidget(r, 1)
                pu_item = self.tableWidget.item(r, 2)
                tot_item = self.tableWidget.item(r, 3)
                if not (nom_item and qte_widget and pu_item and tot_item):
                    raise ValueError(f"Ligne {r + 1} incomplète")
                panier.append({
                    "nom": nom_item.text(),
                    "qte": int(qte_widget.value()),
                    "pu": float(pu_item.text()),
                    "total": float(tot_item.text()),
                })
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Erreur panier", str(e))
            return

        # ─── 2. Client ───
        nom_client_saisi = self.edit_identification_client.text().strip()
        num_client_saisi = self.edit_numero_client.text().strip()
        is_anonymous = not nom_client_saisi
        client_id = getattr(self, "_current_client_id", None)

        if is_anonymous:
            nom_client = "Client anonyme"
            num_client = ""
            client_id = None
        else:
            nom_client = nom_client_saisi
            num_client = num_client_saisi

        # ─── 3. Total (calcul depuis le panier, plus fiable que le label) ───
        try:
            total_general = sum(float(item["total"]) for item in panier)
        except Exception:
            logger.exception("Erreur calcul total depuis le panier")
            QtWidgets.QMessageBox.critical(
                self, "Erreur", "Impossible de calculer le total général.")
            return

        # ─── 4. NOUVEAU : Dialogue encaissement ───
        paiement_info = self._open_paiement_dialog(total_general)
        if paiement_info is None:
            # L'utilisateur a annulé → on ne crée RIEN
            logger.info("Encaissement annulé par l'utilisateur")
            return

        # ─── 5. Création de la vente + encaissement ───
        if is_client_mode():
            self._create_vente_via_api(
                panier, client_id, num_client,
                nom_client, is_anonymous, total_general,
                paiement_info)
        else:
            self._create_vente_local(
                panier, client_id, num_client,
                nom_client, is_anonymous, total_general,
                paiement_info)

    def _open_paiement_dialog(self, total: float) -> dict | None:
        """
        Ouvre le dialogue d'encaissement.
        Retourne le dict du paiement, ou None si annulé.
        """
        try:
            from Setting_encaissement import Setting_encaissement
            dlg = Setting_encaissement(
                parent=self,
                montant_facture=total,
                devise=self.devise)
            if dlg.exec() != QtWidgets.QDialog.Accepted:
                return None
            return dlg.get_result()
        except Exception:
            logger.exception("Erreur ouverture dialogue encaissement")
            return None

    # ══════════════════════════════════════════════════════════════════
    # Vente via API (mode client)
    # ══════════════════════════════════════════════════════════════════
    def _create_vente_via_api(self, panier, client_id, num_client,
                              nom_client, is_anonymous, total_general,
                              paiement_info: dict = None):
        """Crée une vente via l'API du serveur."""
        api = get_api()
        if api is None:
            QtWidgets.QMessageBox.critical(
                self, "Erreur", "API non initialisée.")
            return

        # Résolution des code_refs
        lignes = []
        for item in panier:
            try:
                prod = api.list_produits(search=item["nom"], per_page=5)
                matches = prod.get("items", [])
                if not matches:
                    raise ValueError(
                        f"Produit introuvable : {item['nom']}")
                code_ref = matches[0]["Code_reference"]
                lignes.append({
                    "code_ref": code_ref,
                    "quantite": item["qte"],
                    "prix_unitaire": item["pu"],
                })
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Erreur",
                    f"Impossible de préparer la vente :\n{e}")
                return

        # ─── Payload UNIQUE ───
        payload = {
            "lignes": lignes,
            "client_id": client_id if not is_anonymous else None,
            "client_numero": (num_client
                              if not is_anonymous and not client_id
                              else None),
            "caisse": None,
            "remise": 0,
        }

        if paiement_info:
            r = paiement_info["result"]
            payload["devise_paiement"] = r["devise_paiement"]
            payload["montant_recu"] = r["montant_recu"]

        try:
            result = api.create_vente(**payload)
        except Exception as e:
            logger.exception("Échec vente via API")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'enregistrer la vente :\n{e}")
            return

        num_fact = result.get("Num_fact")
        total_serveur = float(result.get("total", total_general))
        logger.info("Vente créée (API) : %s — %.0f", num_fact, total_serveur)

        # ─── PDF local ───
        self._generate_pdf_after_sale(
            num_fact, panier, nom_client, num_client,
            is_anonymous, total_serveur, caisse=None)

        # ─── Refresh UI ───
        try:
            if self.page_historique is not None:
                self.page_historique.refresh()
        except Exception:
            pass

        self.Load_data_onglet_1()

        if is_anonymous:
            notify.success(f"Facture anonyme enregistrée — {num_fact}")
        else:
            notify.success(
                f"Facture enregistrée pour {nom_client} — {num_fact}")

        self.Clear_table_facture()
        self._current_client_id = None

    # ══════════════════════════════════════════════════════════════════
    # Vente locale (mode autonome / serveur)
    # ══════════════════════════════════════════════════════════════════
    def _create_vente_local(self, panier, client_id, num_client,
                            nom_client, is_anonymous, total_general,
                            paiement_info: dict = None):
        """Crée une vente localement (DB SQLite)."""
        try:
            numero_caisse = db.get_config("facture_numero_caisse", "A")
            numero_temoin = int(db.get_config("facture_numero_temoin", 1))
        except Exception:
            numero_caisse = "A"
            numero_temoin = 1

        numero_facture = (
            f"F{numero_caisse}-"
            f"{time.strftime('%Y-%m-%d')}-"
            f"{numero_temoin:09d}"
        )

        date_facture = time.strftime("%d/%m/%Y %H:%M:%S")

        try:
            from Database import audit

            # ─── Snapshot AVANT pour chaque produit ───
            avant_par_produit = {}
            for item in panier:
                nom_produit = item["nom"]
                info = db.query_one(
                    "SELECT Code_reference FROM produits "
                    "WHERE Nom = ? AND actif = 1 LIMIT 1",
                    (nom_produit,))
                if info:
                    avant_par_produit[nom_produit] = audit.snapshot(
                        "produits", "Code_reference",
                        info["Code_reference"])

            with db.transaction():
                for item in panier:
                    nom_produit = item["nom"]
                    qte_vendue = item["qte"]

                    info = db.query_one(
                        "SELECT Code_reference FROM produits "
                        "WHERE Nom = ? AND actif = 1 LIMIT 1",
                        (nom_produit,))
                    if not info:
                        raise ValueError(
                            f"Produit introuvable : {nom_produit}")

                    db.execute(
                        """INSERT INTO Historique
                           (Num_fact, Code_reference, Article, Prix_uni,
                            Quantite, Total, Client_name,
                            Caisse, Date_vent, utilisateur_id)
                           VALUES (?,?,?,?,?,?,?,?,?,?)""",
                        (numero_facture,
                         info["Code_reference"], nom_produit,
                         item["pu"], qte_vendue, item["total"],
                         f"{nom_client} {num_client}".strip(),
                         numero_caisse, date_facture,
                         self.user_id))

                    self._decrement_stock(
                        nom_produit, qte_vendue,
                        numero_facture=numero_facture)

                if not is_anonymous and num_client:
                    row_client = db.query_one(
                        "SELECT Montant_total FROM Client "
                        "WHERE numero = ? AND actif = 1 LIMIT 1",
                        (num_client,))
                    total_actuel = (float(row_client["Montant_total"])
                                    if row_client else 0.0)
                    nouveau_total = total_actuel + total_general
                    db.execute(
                        "UPDATE Client SET Montant_total = ? "
                        "WHERE numero = ?",
                        (nouveau_total, num_client))

                db.set_config("facture_numero_temoin",
                              numero_temoin + 1, type_="int")
            if paiement_info:
                try:
                    from Database import encaissement
                    encaissement.save_encaissement(
                        num_fact=numero_facture,
                        result=paiement_info["result"],
                        user_id=self.user_id,
                        user_name=self.identifiant,
                        notes=None)
                    logger.info("Encaissement enregistré pour %s",
                                numero_facture)
                except Exception:
                    logger.exception("Erreur enregistrement encaissement")

            # ═══ AUDIT VENTE ═══
            try:
                audit.log(
                    audit.ACTION_CREATION_VENTE,
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.identifiant,
                    cible_type="vente",
                    cible_id=numero_facture,
                    cible_nom=numero_facture,
                    details={
                        "total": total_general,
                        "nb_articles": len(panier),
                        "client": nom_client,
                        "client_numero": num_client,
                        "anonyme": is_anonymous,
                        "caisse": numero_caisse,
                        "lignes": [
                            {"produit": it["nom"],
                             "qte": it["qte"],
                             "pu": it["pu"],
                             "total": it["total"]}
                            for it in panier
                        ],
                    })
            except Exception:
                logger.exception("Erreur audit vente")

        except Exception as e:
            logger.exception("Échec enregistrement facture (local)")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'enregistrer la facture :\n{e}")
            return

        # ─── Génération PDF locale ───
        self._generate_pdf_after_sale(
            numero_facture, panier, nom_client, num_client,
            is_anonymous, total_general, caisse=numero_caisse)



        # ─── Refresh ───
        try:
            self.Connexion_database()
            self.View_historique()
            self.Load_data_onglet_1()
        except Exception:
            logger.exception("Erreur rafraîchissement post-facture")

        if is_anonymous:
            notify.success(
                f"Facture anonyme enregistrée — {numero_facture}")
        else:
            notify.success(
                f"Facture enregistrée pour {nom_client} — "
                f"{numero_facture}")

        self.Clear_table_facture()
        self._current_client_id = None

    # ══════════════════════════════════════════════════════════════════
    # Génération du PDF (utilisé par les 2 modes)
    # ══════════════════════════════════════════════════════════════════
    def _generate_pdf_after_sale(self, numero_facture, panier,
                                 nom_client, num_client,
                                 is_anonymous, total_general,
                                 caisse=None,
                                 paiement_info: dict = None):
        """
        Génère le PDF de la facture + impression auto.
        Compatible mode autonome / serveur / client.
        """

        # ═══════════════════════════════════════════════════════════════
        # 0. Force le rechargement de la config côté client
        # ═══════════════════════════════════════════════════════════════
        if is_client_mode():
            try:
                from Client.api_singleton import clear_config_cache
                clear_config_cache()
            except Exception:
                pass

        # ═══════════════════════════════════════════════════════════════
        # 1. Récupère les infos pharmacie + config
        #    (via get_config qui utilise l'API en mode client)
        # ═══════════════════════════════════════════════════════════════
        from Client.api_singleton import get_config

        # ─── Infos pharmacie ───
        try:
            if is_client_mode():
                nom_entreprise = get_config("nom_entreprise", "NOVA PHARMA")
                adresse_entreprise = get_config("adresse_entreprise", "")
                telephone_entreprise = get_config("telephone_entreprise", "")
            else:
                pharmacie = db.query_one(
                    "SELECT nom, adresse, numero FROM Pharmacie "
                    "WHERE id = 1 AND actif = 1 LIMIT 1")
                if pharmacie:
                    nom_entreprise = pharmacie["nom"] or "NOVA PHARMA"
                    adresse_entreprise = pharmacie["adresse"] or ""
                    telephone_entreprise = pharmacie["numero"] or ""
                else:
                    nom_entreprise = "NOVA PHARMA"
                    adresse_entreprise = ""
                    telephone_entreprise = ""
        except Exception:
            nom_entreprise = "NOVA PHARMA"
            adresse_entreprise = ""
            telephone_entreprise = ""

        # ─── Devise ───
        devise = get_config("devise", "FC")

        # ─── Mentions ───
        try:
            mentions = get_config("mentions_ticket", None)
            if not mentions or not isinstance(mentions, list):
                mentions = [
                    "Les médicaments vendus ne sont ni repris ni échangés",
                    "À conserver hors de la portée des enfants",
                    "Signature ou cachet de la pharmacie",
                ]
        except Exception:
            mentions = []

        # ─── QR code ───
        try:
            qrcode_actif = get_config("qrcode_actif", True)
        except Exception:
            qrcode_actif = True

        # ─── Impression auto ───
        try:
            auto_print = get_config("printer_auto_print", False)
        except Exception:
            auto_print = False

        # ═══════════════════════════════════════════════════════════════
        # 2. Construit le dict data pour Generer_ticket_final
        # ═══════════════════════════════════════════════════════════════
        date_facture = time.strftime("%d/%m/%Y %H:%M:%S")

        produits_vendus = [
            [item["nom"], item["qte"], item["pu"], item["total"]]
            for item in panier
        ]

        data = {
            "Numero facture": numero_facture,
            "Produit vendu": produits_vendus,
            "Numero client": num_client,
            "Nom client": nom_client,
            "date": date_facture,
            "Total general": total_general,
            "Numero de la caisse": caisse or "A",
            "Nom entreprise": nom_entreprise,
            "Adresse entreprise": adresse_entreprise,
            "Telephone entreprise": telephone_entreprise,
            "Mention": mentions,
            "Qrcode": "1" if qrcode_actif else "0",
        }

        # ═══════════════════════════════════════════════════════════════
        # 3. Ajoute les infos de paiement (si présentes)
        # ═══════════════════════════════════════════════════════════════
        if paiement_info:
            r = paiement_info["result"]
            data["Montant recu"] = r["montant_recu"]
            data["Devise paiement"] = r["devise_paiement"]
            data["Montant recu FC"] = r["montant_recu_fc"]
            data["Montant rendu"] = r["montant_rendu"]
            data["Taux change"] = r["taux_change"]

        # ═══════════════════════════════════════════════════════════════
        # 4. Chemin du PDF
        # ═══════════════════════════════════════════════════════════════
        if is_anonymous:
            path_pdf = os.path.join(
                "Factures", "Anonymes", numero_facture + ".pdf")
        else:
            nom_dossier = "".join(
                c for c in nom_client if c.isalnum() or c in " -_"
            ).strip() or "Client"
            path_pdf = os.path.join(
                "Factures", nom_dossier, numero_facture + ".pdf")

        # ═══════════════════════════════════════════════════════════════
        # 5. Génère le PDF
        # ═══════════════════════════════════════════════════════════════
        try:
            os.makedirs(os.path.dirname(path_pdf), exist_ok=True)
            Generer_ticket_final(data, path_pdf)
            logger.info("Facture PDF générée : %s", path_pdf)
        except Exception:
            logger.exception("Échec génération PDF")
            QtWidgets.QMessageBox.warning(
                self, "PDF",
                "La facture a été enregistrée mais le PDF "
                "n'a pas pu être généré.")
            return

        # ═══════════════════════════════════════════════════════════════
        # 6. Impression auto (silencieuse)
        # ═══════════════════════════════════════════════════════════════
        # Impression auto (silencieuse) — utilise l'imprimante TICKET
        if auto_print:
            try:
                from Database import printer_manager
                printer_manager.print_pdf_silent(path_pdf, kind="ticket")
                logger.info("Facture envoyée à l'imprimante ticket")
            except Exception:
                logger.exception("Erreur impression auto")

    # ══════════════════════════════════════════════════════════════
    # Barre de recherche Articles (page_3)
    # ══════════════════════════════════════════════════════════════
    def _setup_article_search(self) -> None:
        try:
            layout = getattr(self, "horizontalLayout_7", None)
            if layout is None:
                logger.warning("horizontalLayout_7 introuvable")
                return

            if getattr(self, "search_article", None) is not None:
                return

            search = QtWidgets.QLineEdit()
            search.setObjectName("search_article")
            search.setPlaceholderText(
                "Rechercher par nom ou code référence…")
            search.setMinimumSize(320, 42)
            search.setMaximumSize(420, 42)
            search.setClearButtonEnabled(True)
            search.setStyleSheet("""
                QLineEdit {
                    background-color: #ffffff;
                    border: 2px solid #94a3b8;
                    border-radius: 11px;
                    padding: 10px 14px;
                    color: #0f172a;
                    font-size: 13px;
                    font-weight: 500;
                }
                QLineEdit:hover { border-color: #64748b; }
                QLineEdit:focus { border: 2px solid #0077B6; }
                QLineEdit::placeholder { color: #94a3b8; }
            """)

            icon_search = getattr(self, "icon_search", None)
            if icon_search is not None:
                try:
                    search.addAction(
                        icon_search,
                        QtWidgets.QLineEdit.LeadingPosition)
                except Exception:
                    pass

            layout.insertWidget(0, search)
            search.textChanged.connect(
                self.Search_produit_by_code_or_name)

            self.search_article = search
            logger.info("Barre de recherche Articles installée")

        except Exception:
            logger.exception("Erreur _setup_article_search")

    # ══════════════════════════════════════════════════════════════
    # Stock / modification / suppression produit
    # ══════════════════════════════════════════════════════════════
    def Modifier_stock(self) -> None:
        self._require_perm("modifier_stock")

        if not hasattr(self, "tbw_voir_produit"):
            return

        row = self.tbw_voir_produit.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(
                self, "Aucun produit sélectionné",
                "Sélectionnez un produit dans la liste pour le modifier.")
            return

        item = self.tbw_voir_produit.item(row, 0)
        if not item:
            return
        code_ref = item.text()

        try:
            from Setting_edit_produit import Edit_produit
            dlg = Edit_produit(code_reference=code_ref, user_id=self.user_id)
            dlg.product_updated.connect(self._on_produit_updated)
            if dlg.exec() == QtWidgets.QDialog.Accepted:
                self._reload_produits_master()
                self.Add_produit_tablewidget()
                self.Load_data_onglet_1()
        except PermissionDeniedError as e:
            QtWidgets.QMessageBox.warning(self, "Accès refusé", str(e))
        except Exception:
            logger.exception("Erreur Modifier_stock")

    def _on_produit_updated(self, code_ref: str):
        logger.info("Produit mis à jour : %s", code_ref)

    def Delete_produit(self) -> None:
        self._require_perm("supprimer_produit")

        if not hasattr(self, "tbw_voir_produit"):
            return

        row = self.tbw_voir_produit.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(
                self, "Aucun produit sélectionné",
                "Sélectionnez un produit dans la liste pour le supprimer.")
            return

        item = self.tbw_voir_produit.item(row, 0)
        if not item:
            return
        code_ref = item.text()

        try:
            produit = db.query_one(
                "SELECT Nom, Quantite, Categorie FROM produits "
                "WHERE Code_reference = ? LIMIT 1", (code_ref,))
        except Exception:
            logger.exception("Erreur recherche produit pour suppression")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible de charger les informations du produit.")
            return

        if not produit:
            QtWidgets.QMessageBox.warning(
                self, "Produit introuvable",
                "Ce produit n'existe plus en base.")
            self._reload_produits_master()
            self.Add_produit_tablewidget()
            return

        nom = produit["Nom"]
        quantite = int(produit["Quantite"] or 0)

        msg = (
            f"<b>Supprimer le produit « {nom} » ?</b><br><br>"
            f"Code référence : <code>{code_ref}</code><br>"
            f"Stock actuel : <b>{quantite} unité(s)</b><br><br>"
            "Le produit sera <b>masqué</b> mais restera dans l'historique "
            "des ventes et des ajustements de stock.<br><br>"
            "Cette action peut être annulée par un administrateur."
        )
        rep = QtWidgets.QMessageBox.question(
            self, "Confirmation de suppression", msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)

        if rep != QtWidgets.QMessageBox.Yes:
            return

        try:
            with db.transaction():
                db.execute(
                    "UPDATE produits SET actif = 0 "
                    "WHERE Code_reference = ?", (code_ref,))

            logger.info("Produit supprimé (soft) : %s (%s) par %s",
                        nom, code_ref, self.identifiant)

            notify.success(f"Produit « {nom} » supprimé.")

            self._reload_produits_master()
            self.Add_produit_tablewidget()
            self.Load_data_onglet_1()

        except PermissionDeniedError as e:
            notify.danger(f"Accès refusé : {e}")
        except Exception as e:
            logger.exception("Échec suppression produit")
            notify.danger(f"Impossible de supprimer « {nom} » : {e}")

    # ══════════════════════════════════════════════════════════════
    # Historique
    # ══════════════════════════════════════════════════════════════
    def View_historique(self) -> None:
        if self._is_caissier_restricted():
            return
        if not hasattr(self, "tableWidget_4"):
            return
        try:
            rows = db.query("SELECT * FROM Historique")
            self.tableWidget_4.setRowCount(len(rows))
            for r, row in enumerate(rows):
                for c, val in enumerate(row):
                    if c == 0:
                        continue
                    text = str(val)
                    if c == 8:
                        text = " ".join(text.split(" ")[:-1])
                    self.tableWidget_4.setItem(
                        r, c - 1, QtWidgets.QTableWidgetItem(text))
        except Exception:
            logger.exception("Erreur View_historique")

    def Switch_table_historique(self) -> None:
        if not (hasattr(self, "label_40") and hasattr(self, "switch_btn")):
            return
        titre = self.label_40.text()
        self.label_40.setText(self.switch_btn.text())
        self.switch_btn.setText(titre)
        idx = 1 - self.stackedWidget_2.currentIndex()
        if hasattr(self.stackedWidget_2, "slide_to_index"):
            self.stackedWidget_2.slide_to_index(idx)
        else:
            self.stackedWidget_2.setCurrentIndex(idx)

    def View_historique_commande(self) -> None:
        if self._is_caissier_restricted():
            return
        if not hasattr(self, "tableWidget_5"):
            return
        try:
            rows = db.query("SELECT * FROM Historique_commande")
            self.tableWidget_5.setRowCount(len(rows))
            for r, row in enumerate(rows):
                for c, val in enumerate(row):
                    if c == 0:
                        continue
                    self.tableWidget_5.setItem(
                        r, c - 1, QtWidgets.QTableWidgetItem(str(val)))
        except Exception:
            logger.exception("Erreur View_historique_commande")

    # ══════════════════════════════════════════════════════════════
    # Utilisateurs — délégué à PageUsers + Setting_user_dialog
    # ══════════════════════════════════════════════════════════════
    def View_user(self) -> None:
        pass

    def View_information_user(self) -> None:
        pass

    def Add_user(self) -> None:
        self._require_perm("ajouter_user")
        try:
            from Setting_user_dialog import Setting_user_dialog
            dlg = Setting_user_dialog(
                parent=self,
                current_user_id=self.user_id,
                current_is_owner=self._is_owner,
                current_is_developer=self._is_developer)
            dlg.user_saved.connect(self._on_user_saved)
            dlg.exec()
        except PermissionDeniedError as e:
            QtWidgets.QMessageBox.warning(self, "Accès refusé", str(e))
        except Exception:
            logger.exception("Erreur Add_user")

    def _on_user_saved(self, user_id: str) -> None:
        logger.info("Utilisateur enregistré : %s", user_id)
        if self.page_users is not None:
            try:
                self.page_users.refresh()
            except Exception:
                logger.exception("Erreur refresh PageUsers")

    # ══════════════════════════════════════════════════════════════
    # Fournisseurs
    # ══════════════════════════════════════════════════════════════
    def Add_fournisseur(self) -> None:
        self._require_perm("ajouter_fournisseur")
        try:
            dlg = Setting_add_fourniss(
                parent=self,
                user_id=self.user_id,
                user_name=self.identifiant)
            dlg.fournisseur_created.connect(self._on_fournisseur_created)
            dlg.exec()
        except PermissionDeniedError as e:
            QtWidgets.QMessageBox.warning(self, "Accès refusé", str(e))
        except Exception:
            logger.exception("Erreur Add_fournisseur")

    def _on_fournisseur_created(self, fid: str) -> None:
        logger.info("Fournisseur créé : %s", fid)
        self.View_fournisseur()
        try:
            if self.page_blf is not None:
                self.page_blf.refresh()
        except Exception:
            pass

    def View_fournisseur(self) -> None:
        if not hasattr(self, "tbw_blf_lignes"):
            return
        try:
            rows = db.query("SELECT * FROM Fournisseur")
            if hasattr(self, "lbl_blf_stat1_value"):
                self.lbl_blf_stat1_value.setText(str(len(rows)))
            self.tbw_blf_lignes.setRowCount(len(rows))
            for r, row in enumerate(rows):
                for c, val in enumerate(row):
                    if c in (0, 6):
                        continue
                    item = QtWidgets.QTableWidgetItem(str(val))
                    item.setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignHCenter)
                    self.tbw_blf_lignes.setItem(r, c - 1, item)
        except Exception:
            logger.exception("Erreur View_fournisseur")

    def Recharge_stock(self) -> None:
        try:
            from Setting_blf_dialog import Setting_blf_dialog
            dlg = Setting_blf_dialog(
                parent=self,
                user_id=self.user_id,
                user_name=self.identifiant,
            )
            dlg.blf_created.connect(lambda _: self._refresh_after_blf())
            if dlg.exec() == QtWidgets.QDialog.Accepted:
                self._refresh_after_blf()
        except Exception:
            logger.exception("Erreur Recharge_stock")

    def _refresh_after_blf(self) -> None:
        self._reload_produits_master()
        self.Add_produit_tablewidget()
        self.Load_data_onglet_1()

        if self.page_blf is not None:
            try:
                self.page_blf.refresh()
            except Exception:
                logger.exception("Erreur refresh page BLF")

    # ══════════════════════════════════════════════════════════════
    # Sauvegarde / configuration / rapports
    # ══════════════════════════════════════════════════════════════
    def Save_database(self) -> None:
        self._require_perm("sauvegarder")
        try:
            dlg = Setting_save(
                parent=self,
                user_id=self.user_id,
                user_name=self.identifiant)
            dlg.sauvegarde_terminee.connect(self._on_save_done)
            dlg.exec()
        except PermissionDeniedError as e:
            QtWidgets.QMessageBox.warning(self, "Accès refusé", str(e))
        except Exception:
            logger.exception("Erreur Save_database")

    def _on_save_done(self, path: str) -> None:
        logger.info("Sauvegarde terminée : %s", path)
        self.statusbar.showMessage(
            f"Sauvegarde créée : {path}", 5000)

    def Configuration_software(self) -> None:
        self._require_perm("configurer")
        try:
            self.win8 = Configuration()
            self.win8.show()
        except PermissionDeniedError as e:
            QtWidgets.QMessageBox.warning(self, "Accès refusé", str(e))
        except Exception:
            logger.exception("Erreur Configuration_software")

    def _install_page_rapports(self) -> None:
        try:
            self.page_rapports = PageRapports(
                parent=self,
                user_id=self.user_id,
                user_name=self.identifiant,
            )

            target = self.page_7
            layout = target.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(target)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()

            layout.addWidget(self.page_rapports)
            logger.info("PageRapports installée dans page_7")

        except Exception as e:
            logger.exception("Impossible d'installer PageRapports")
            QtWidgets.QMessageBox.warning(
                self, "Erreur",
                f"Impossible d'installer la page rapports :\n{e}")

    def Open_rapports(self) -> None:
        pass

    def _on_rapport_clicked(self) -> None:
        pass

    def _open_taux_change(self):
        try:
            from Setting_taux_change import Setting_taux_change
            dlg = Setting_taux_change(
                parent=self,
                user_id=self.user_id,
                user_name=self.identifiant,
                role=self.role,
                is_owner=self._is_owner,
                is_developer=self._is_developer)
            dlg.taux_modifie.connect(self._on_taux_modifie)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture taux")
            QtWidgets.QMessageBox.critical(
                self, "Erreur", "Impossible d'ouvrir le dialogue.")

    def _on_taux_modifie(self, nouveau_taux: float):
        """Callback après modification du taux."""
        logger.info("Taux modifié : %s", nouveau_taux)
        self.statusbar.showMessage(
            f"Taux de change mis à jour : 1 USD = {nouveau_taux:,.0f} FC"
            .replace(",", " "), 6000)
        # Rafraîchit les affichages
        try:
            self.Get_total_paye()
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════════
    # Rafraîchissement global
    # ══════════════════════════════════════════════════════════════
    def Refresh_all_data(self) -> None:
        if self._is_caissier_restricted():
            return
        self.View_historique()
        self.View_fournisseur()
        self.View_all_products()
        self.View_historique_commande()
        self.Load_data_onglet_1()

        if self.page_clients is not None:
            try:
                self.page_clients.refresh()
            except Exception:
                logger.exception("Erreur refresh page clients")

        if self.page_blf is not None:
            try:
                self.page_blf.refresh()
            except Exception:
                logger.exception("Erreur refresh page BLF")

        if self.page_users is not None:
            try:
                self.page_users.refresh()
            except Exception:
                logger.exception("Erreur refresh page utilisateurs")

        if self.page_audit is not None:
            try:
                self.page_audit.refresh()
            except Exception:
                logger.exception("Erreur refresh page audit")

        if self.page_rapports is not None:
            try:
                self.page_rapports._generer()
            except Exception:
                logger.exception("Erreur refresh page rapports")

        if self.page_historique is not None:
            try:
                self.page_historique.refresh()
            except Exception:
                logger.exception("Erreur refresh page historique")

        if self._page_surveillance_content is not None:
            try:
                self._page_surveillance_content._load_all()
            except Exception:
                logger.exception("Erreur refresh page surveillance")

        # Rafraîchit les graphiques
        try:
            from Charts import install_dashboard_charts
            install_dashboard_charts(self)
            # ─── DIAGNOSTIC OVERLAY (temporaire) ───
            QtCore.QTimer.singleShot(2000, self._diagnose_overlay)
        except Exception:
            logger.exception("Erreur refresh graphiques")

        # Rafraîchit les alertes
        try:
            alerts = getattr(self, "_page_alertes_content", None)
            if alerts is not None:
                alerts.refresh()
        except Exception:
            logger.exception("Erreur refresh alertes")

        # Rafraîchit l'accueil (KPIs)
        try:
            accueil = getattr(self, "_page_accueil_content", None)
            if accueil is not None:
                accueil.refresh()
        except Exception:
            logger.exception("Erreur refresh accueil")

    def _fmt_dual(self, montant_fc: float) -> str:
        """Formate un montant FC avec équivalent USD si activé."""
        try:
            from Database.currency import format_dual
            return format_dual(montant_fc)
        except Exception:
            return f"{float(montant_fc):,.0f} FC".replace(",", " ")

    def _menu_developer(self):
        if not self._is_developer:
            QtWidgets.QMessageBox.warning(
                self, "Accès refusé",
                "Le mode développeur est réservé au compte DEVELOPER.")
            return

        try:
            from Setting_developer import Setting_developer
            dlg = Setting_developer(
                parent=self,
                user_id=self.user_id,
                user_name=self.identifiant)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture mode développeur")

    # ══════════════════════════════════════════════════════════════
    # Déconnexion
    # ══════════════════════════════════════════════════════════════
    def Logout(self) -> None:
        try:
            if (hasattr(self, "tableWidget")
                    and self.tableWidget.rowCount() > 0):
                rep = QtWidgets.QMessageBox.question(
                    self, "Panier non vide",
                    "Des articles sont encore dans le panier de "
                    "facturation. Les perdre et se déconnecter ?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.No)
                if rep != QtWidgets.QMessageBox.Yes:
                    return

            if (self.page_parametres is not None
                    and getattr(self.page_parametres, "_dirty", False)):
                rep = QtWidgets.QMessageBox.question(
                    self, "Modifications non enregistrées",
                    "Des modifications sont en cours dans les "
                    "Paramètres. Les perdre et se déconnecter ?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.No)
                if rep != QtWidgets.QMessageBox.Yes:
                    return

            rep = QtWidgets.QMessageBox.question(
                self, "Se déconnecter",
                f"<b>Se déconnecter de Nova Pharma ?</b><br><br>"
                f"Utilisateur : <b>{self.identifiant}</b><br>"
                f"Rôle : {self.role}",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if rep != QtWidgets.QMessageBox.Yes:
                return

            # ─── MODE CLIENT : logout via API ───
            try:
                from Client.api_singleton import get_api, is_client_mode
                if is_client_mode():
                    api = get_api()
                    if api is not None:
                        try:
                            api.logout()
                        except Exception:
                            logger.exception(
                                "Erreur logout API (on continue)")
            except Exception:
                logger.exception("Erreur logout client")

            # ─── Audit ───
            try:
                from Database import audit
                audit.log(
                    audit.ACTION_DECONNEXION,
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.identifiant,
                    cible_type="session",
                    cible_nom=self.identifiant,
                    details={"role": self.role})
            except Exception:
                logger.exception("Erreur log déconnexion")

            self._is_logging_out = True
            self.logout_requested.emit()
            self.close()

        except Exception:
            logger.exception("Erreur lors de la déconnexion")

    def Force_logout(self, reason: str = "") -> None:
        try:
            self._is_logging_out = True
            logger.info("Déconnexion forcée : %s", reason)
            self.logout_requested.emit()
            self.close()
        except Exception:
            logger.exception("Erreur lors de la déconnexion forcée")

    def _send_heartbeat(self):
        """Envoie un heartbeat au serveur (avec log progressif)."""
        if not is_client_mode():
            return

        api = get_api()
        if api is None:
            return

        imprimante = ""
        try:
            from Database import printer_manager
            imprimante = printer_manager.get_default_printer() or ""
        except Exception:
            pass

        try:
            api.heartbeat(imprimante=imprimante, version="2.0.0")

            # ─── Succès : reset le compteur ───
            if self._heartbeat_failures > 0:
                logger.info(
                    "Heartbeat rétabli après %d échec(s) consécutif(s)",
                    self._heartbeat_failures)
                self._heartbeat_failures = 0

        except Exception as e:
            self._heartbeat_failures += 1

            # Log progressif : 1er échec silencieux, 3e = warning
            if self._heartbeat_failures == 3:
                logger.warning(
                    "Heartbeat échoué 3 fois de suite — "
                    "serveur injoignable : %s", e)
            elif self._heartbeat_failures % 10 == 0:
                logger.warning(
                    "Heartbeat toujours en échec (%d fois) — "
                    "serveur injoignable", self._heartbeat_failures)

    # ══════════════════════════════════════════════════════════════
    # Fermeture
    # ══════════════════════════════════════════════════════════════
    def closeEvent(self, event) -> None:
        try:
            self._timer.stop()
        except Exception:
            pass

        try:
            db.close()
        except Exception:
            pass

        if self._is_logging_out:
            logger.info("MainWindow fermé — déconnexion (user=%s)",
                        self.identifiant)
        else:
            logger.info("MainWindow fermé — arrêt (user=%s)",
                        self.identifiant)

        try:
            self.window_closed.emit()
        except Exception:
            pass

        super().closeEvent(event)

    def _menu_shortcuts(self):
        try:
            from Help_shortcuts import HelpShortcutsDialog
            dlg = HelpShortcutsDialog(parent=self)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture raccourcis")

# ══════════════════════════════════════════════════════════════════
# Test autonome
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s : %(message)s",
    )
    app = QtWidgets.QApplication(sys.argv)
    win = Setting_main_window(
        user_id="TEST", role="ADMIN", identifiant="test@local")
    win.showMaximized()
    sys.exit(app.exec())