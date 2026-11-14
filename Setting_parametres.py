#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_parametres.py — Page Paramètres complète.
===================================================
Onglets : Entreprise / Vente / Facturation / Sauvegarde /
          Sécurité / Impression / Danger / Réseau / Système

Correctifs v2.0.0 (Batch 4 + Phase 1 monitoring) :
  • Fix bug Batch 4 : code mal placé dans _connect_signals
    (allow_admin_on_client n'est plus écrasé silencieusement)
  • Paramètre `role` ajouté (fixe AttributeError sur self.role)
  • hasattr() sur chk_require_pwd_critical (absent du .ui)
  • _fix_spinbox_alignment() : contourne bug Qt6 (QSpinBox)
  • Section "PC de monitoring" (whitelist 3 PC max)
  • Détection des modifications non enregistrées
"""

import logging
import os
import shutil
import socket
import time
from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Client.api_singleton import get_api, is_client_mode
from Database import backup_engine, db, audit, printer_manager
from Interface_page_parametres import Ui_PageParametres
from Notification_manager import notify

logger = logging.getLogger(__name__)

LOGO_DIR = "Assets/Logos"


class PageParametres(QtWidgets.QWidget, Ui_PageParametres):

    parametres_changed = QtCore.Signal()

    def __init__(self, parent=None, user_id=None, user_name="",
                 role="UTILISATEUR",
                 is_owner=False, is_developer=False):
        super().__init__(parent)
        self.setupUi(self)

        # ─── Force tous les onglets actifs (bug fix) ───
        try:
            for i in range(self.tabs.count()):
                self.tabs.setTabEnabled(i, True)
                self.tabs.setTabVisible(i, True)
        except Exception:
            logger.exception("Erreur activation onglets")

        # ─── Session ───
        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self.role = (role or "UTILISATEUR").upper()
        self.is_owner = is_owner
        self.is_developer = is_developer

        # ─── État interne ───
        self._logo_path = None
        self._dirty = False
        self._loading = False

        # ─── Init ───
        self._setup_header()
        self._connect_signals()
        self._apply_permissions()
        self._install_server_config_button()
        self._install_system_tab()
        self._install_license_tab()  # ← AJOUT
        self._connect_monitoring_widgets()
        self._load_all()
        self._fix_spinbox_alignment()
        self._mark_clean()

    # ══════════════════════════════════════════════════════════════
    # Setup
    # ══════════════════════════════════════════════════════════════
    def _setup_header(self):
        """Charge l'icône du header."""
        try:
            pix = QtGui.QPixmap(":/Icon/Icons/settings_white.svg")
            if not pix.isNull():
                self.header_icon.setPixmap(pix.scaled(
                    24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.header_icon.setAlignment(Qt.AlignCenter)
        except Exception:
            logger.exception("Erreur chargement icône header")

    def _connect_signals(self):
        """Connecte tous les signaux des widgets."""
        # ─── Logo ───
        self.btn_upload_logo.clicked.connect(self._on_upload_logo)
        self.btn_remove_logo.clicked.connect(self._on_remove_logo)

        # ─── Sauvegarde ───
        self.btn_browse_save.clicked.connect(self._browse_backup_dir)
        if hasattr(self, "btn_browse_backup_secondary"):
            self.btn_browse_backup_secondary.clicked.connect(
                self._browse_backup_secondary)
        if hasattr(self, "btn_manage_backups"):
            self.btn_manage_backups.clicked.connect(
                self._on_manage_backups)
        if hasattr(self, "chk_backup_secondary"):
            self.chk_backup_secondary.toggled.connect(
                self._on_secondary_toggled)

        # ─── Imprimantes TICKET ───
        if hasattr(self, "btn_refresh_printers_ticket"):
            self.btn_refresh_printers_ticket.clicked.connect(
                self._on_refresh_printers)
        if hasattr(self, "btn_test_print_ticket"):
            self.btn_test_print_ticket.clicked.connect(
                lambda: self._on_test_print("ticket"))
        if hasattr(self, "combo_printer_ticket"):
            self.combo_printer_ticket.currentTextChanged.connect(
                self._mark_dirty)

        # ─── Imprimantes RAPPORT ───
        if hasattr(self, "btn_test_print_report"):
            self.btn_test_print_report.clicked.connect(
                lambda: self._on_test_print("report"))
        if hasattr(self, "combo_printer_report"):
            self.combo_printer_report.currentTextChanged.connect(
                self._mark_dirty)

        # ─── Checkboxes impression ───
        if hasattr(self, "chk_auto_print"):
            self.chk_auto_print.toggled.connect(self._mark_dirty)
        if hasattr(self, "chk_auto_print_report"):
            self.chk_auto_print_report.toggled.connect(self._mark_dirty)
        if hasattr(self, "chk_auto_open_pdf"):
            self.chk_auto_open_pdf.toggled.connect(self._mark_dirty)

        # ─── Danger zone ───
        self.btn_export_db.clicked.connect(self._on_export_db)
        self.btn_restore_db.clicked.connect(self._on_restore_db)
        self.btn_reset_all.clicked.connect(self._on_reset_all)

        # ─── Footer ───
        self.btn_save.clicked.connect(self._on_save)
        self.btn_reload.clicked.connect(self._confirm_reload)

        # ─── Détection des modifications (champs texte) ───
        text_fields = (
            self.edit_nom, self.edit_tel, self.edit_email_ent,
            self.edit_adresse, self.edit_caisse,
            self.edit_dossier_save, self.edit_mentions,
        )
        for w in text_fields:
            try:
                if hasattr(w, "textChanged"):
                    w.textChanged.connect(self._mark_dirty)
            except AttributeError:
                pass

        # ─── Combos ───
        for c in (self.combo_type, self.combo_devise,
                  self.combo_periode_ca):
            c.currentIndexChanged.connect(self._mark_dirty)

        # ─── Spinboxes ───
        spin_names = (
            "spin_marge", "spin_freq_save", "spin_max_save",
            "spin_pwd_min", "spin_pwd_exp", "spin_seuil_stock",
            "spin_max_postes", "spin_taux_change",
        )
        for name in spin_names:
            w = getattr(self, name, None)
            if w is not None:
                try:
                    w.valueChanged.connect(self._mark_dirty)
                except Exception:
                    logger.exception(
                        "Impossible de connecter %s", name)

        # ─── Checkboxes ───
        checkbox_names = (
            "chk_impression_auto",
            "chk_qrcode",
            "chk_sauvegarde_auto",
            "chk_require_digit",
            "chk_require_upper",
            "chk_require_special",
            "chk_require_pwd_critical",
            "chk_backup_urgence",
            "chk_allow_admin_client",
        )
        for name in checkbox_names:
            w = getattr(self, name, None)
            if w is not None:
                try:
                    w.toggled.connect(self._mark_dirty)
                except Exception:
                    logger.exception(
                        "Impossible de connecter %s", name)
            else:
                logger.warning("Widget absent du .ui : %s", name)

    # ══════════════════════════════════════════════════════════════
    # Permissions
    # ══════════════════════════════════════════════════════════════
    def _apply_permissions(self):
        can_admin = (self.is_owner or self.is_developer)

        # ─── Danger Zone : ADMIN uniquement ───
        self.btn_export_db.setEnabled(can_admin)
        self.btn_restore_db.setEnabled(can_admin)
        self.btn_reset_all.setEnabled(can_admin)

        # ─── Mode client : Danger Zone CACHÉE ───
        if self._is_client_readonly():
            try:
                # Retire l'onglet Danger Zone
                for i in range(self.tabs.count() - 1, -1, -1):
                    title = self.tabs.tabText(i).lower()
                    if "danger" in title:
                        self.tabs.removeTab(i)
                        logger.info(
                            "Onglet Danger Zone retiré (mode client)")
                        break
            except Exception:
                logger.exception("Erreur retrait Danger Zone")

            # Applique le read-only
            self._apply_client_readonly()
            return

        # ─── Mode serveur : message si pas admin ───
        if not can_admin:
            self._set_status(
                "Seul le propriétaire ou le développeur peut effectuer "
                "certaines actions sensibles.", "warn")

    def _apply_client_readonly(self) -> None:
        """
        En mode client : verrouille tous les onglets DB.
        Autorise uniquement :
          - chk_allow_admin_client (Sécurité)
          - Impression (QSettings local)
          - Réseau (dialog séparé)
        """
        try:
            # ─── ONGLET ENTREPRISE : tout en lecture seule ───
            self._set_widgets_enabled([
                self.edit_nom, self.edit_tel, self.edit_email_ent,
                self.edit_adresse, self.combo_type,
                self.btn_upload_logo, self.btn_remove_logo,
            ], False)

            # ─── ONGLET VENTE : tout en lecture seule ───
            self._set_widgets_enabled([
                self.combo_devise, self.combo_periode_ca,
                self.edit_caisse, self.spin_marge,
                getattr(self, "spin_max_postes", None),
                getattr(self, "spin_taux_change", None),
                getattr(self, "spin_seuil_stock", None),
            ], False)

            # ─── ONGLET FACTURATION : lecture seule ───
            self._set_widgets_enabled([
                self.chk_impression_auto, self.chk_qrcode,
                self.edit_mentions,
            ], False)

            # ─── ONGLET SAUVEGARDE : lecture seule ───
            self._set_widgets_enabled([
                self.chk_sauvegarde_auto,
                self.spin_freq_save, self.spin_max_save,
                self.edit_dossier_save, self.btn_browse_save,
                getattr(self, "chk_backup_secondary", None),
                getattr(self, "edit_backup_secondary", None),
                getattr(self, "btn_browse_backup_secondary", None),
                getattr(self, "btn_manage_backups", None),
            ], False)

            # ─── ONGLET SÉCURITÉ : lecture seule ───
            self._set_widgets_enabled([
                self.spin_pwd_min, self.spin_pwd_exp,
                self.chk_require_digit, self.chk_require_upper,
                self.chk_require_special,
                getattr(self, "chk_require_pwd_critical", None),
                self.chk_backup_urgence,
            ], False)

            # ✅ SEUL champ Sécurité modifiable en client
            if hasattr(self, "chk_allow_admin_client"):
                self.chk_allow_admin_client.setEnabled(True)
                self.chk_allow_admin_client.setToolTip(
                    "Autorise les connexions ADMIN/OWNER/DEV "
                    "depuis n'importe quel PC client (mode dégradé)")

            # ─── ONGLET IMPRESSION : entièrement modifiable ✅ ───
            # (rien à désactiver : QSettings locaux)

            # ─── Message d'information global ───
            self._set_status(
                "Mode client : paramètres serveur en lecture seule. "
                "Modifiable sur le serveur physique uniquement.", "warn")

            # Badge visuel sur les onglets verrouillés
            self._mark_readonly_tab("Entreprise")
            self._mark_readonly_tab("Vente")
            self._mark_readonly_tab("Facturation")
            self._mark_readonly_tab("Sauvegarde")
            self._mark_readonly_tab("Sécurité")

            logger.info(
                "Paramètres : mode client → read-only appliqué")

        except Exception:
            logger.exception("Erreur application read-only client")

    def _mark_readonly_tab(self, keyword: str):
        """Ajoute un cadenas 🔒 au titre de l'onglet."""
        try:
            for i in range(self.tabs.count()):
                title = self.tabs.tabText(i)
                if keyword.lower() in title.lower() and "🔒" not in title:
                    self.tabs.setTabText(i, f"🔒 {title}")
                    break
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════════
    # Mode client : helpers
    # ══════════════════════════════════════════════════════════════
    def _is_client_readonly(self) -> bool:
        """Vrai si on est en mode client (config serveur)."""
        try:
            return is_client_mode()
        except Exception:
            return False

    def _set_widgets_enabled(self, widgets: list, enabled: bool):
        """Active/désactive une liste de widgets (robuste aux None)."""
        for w in widgets:
            if w is not None:
                try:
                    w.setEnabled(enabled)
                except Exception:
                    pass

    # ══════════════════════════════════════════════════════════════
    # Statut (barre du bas)
    # ══════════════════════════════════════════════════════════════
    def _set_status(self, message: str, status: str = ""):
        """Change le message + applique l'attribut CSS."""
        self.lbl_status.setText(message)
        self.lbl_status.setProperty("status", status)
        self.lbl_status.style().unpolish(self.lbl_status)
        self.lbl_status.style().polish(self.lbl_status)

    def _mark_dirty(self, *_):
        if self._loading:
            return
        if self._dirty:
            return
        self._dirty = True
        self._set_status(
            "Modifications non enregistrées — cliquez sur Enregistrer.",
            "warn")

    def _mark_clean(self):
        self._dirty = False
        self._set_status(
            "Tous les paramètres sont à jour.", "ok")

    # ══════════════════════════════════════════════════════════════
    # Chargement
    # ══════════════════════════════════════════════════════════════
    def _load_all(self):
        self._loading = True
        try:
            self._load_entreprise()
            self._load_vente()
            self._load_facturation()
            self._load_sauvegarde()
            self._load_securite()
            self._load_imprimantes()
        finally:
            self._loading = False

    def _load_entreprise(self):
        try:
            # ─── Mode client → API ───
            if self._is_client_readonly():
                api = get_api()
                if api is None:
                    return
                try:
                    ph = api.get_pharmacie()
                except Exception:
                    logger.exception("Erreur get_pharmacie (API)")
                    return

                self.edit_nom.setText(ph.get("nom") or "")
                self.edit_tel.setText(ph.get("numero") or "")
                self.edit_email_ent.setText(ph.get("email") or "")
                self.edit_adresse.setText(ph.get("adresse") or "")

                t = (ph.get("type") or "MOYENNE").upper()
                idx = self.combo_type.findText(t)
                if idx >= 0:
                    self.combo_type.setCurrentIndex(idx)

                self._load_logo(ph.get("path_logo"))
                return

            # ─── Mode local ───
            ph = db.query_one(
                "SELECT * FROM Pharmacie WHERE id = 1 LIMIT 1")
            if ph:
                self.edit_nom.setText(ph["nom"] or "")
                self.edit_tel.setText(ph["numero"] or "")
                self.edit_email_ent.setText(ph["email"] or "")
                self.edit_adresse.setText(ph["adresse"] or "")

                t = (ph["type"] or "MOYENNE").upper()
                idx = self.combo_type.findText(t)
                if idx >= 0:
                    self.combo_type.setCurrentIndex(idx)

                self._load_logo(ph["path_logo"])
            else:
                self._load_logo(None)
        except Exception:
            logger.exception("Erreur chargement entreprise")

    def _load_logo(self, path):
        self._logo_path = path
        if path and os.path.exists(path):
            pix = QtGui.QPixmap(path)
            if not pix.isNull():
                self.logo_preview.setPixmap(pix.scaled(
                    96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.logo_preview.setStyleSheet(
                    "QLabel { background: #ffffff; border: 1px solid "
                    "#e2e8f0; border-radius: 12px; }")
                self.logo_preview.setText("")
                return
        self.logo_preview.setPixmap(QtGui.QPixmap())
        self.logo_preview.setText("Logo")
        self.logo_preview.setStyleSheet(
            "QLabel { background: #f8fafc; border: 2px dashed #cbd5e1; "
            "border-radius: 12px; color: #94a3b8; font-size: 11px; "
            "font-weight: 700; }")

    def _load_vente(self):
        try:
            # ─── Récupère les valeurs (API ou DB) ───
            if self._is_client_readonly():
                api = get_api()
                if api is None:
                    return
                cfg = api.get_full_config()
                get = lambda k, d: cfg.get(k, d)
            else:
                get = lambda k, d: db.get_config(k, d)

            self.combo_devise.setCurrentText(get("devise", "FC") or "FC")
            self.combo_periode_ca.setCurrentText(
                get("chiffre_affaire_periode", "Mois") or "Mois")

            try:
                marge = float(get("marge_benefice", 30) or 30)
            except Exception:
                marge = 30.0
            self.spin_marge.setValue(marge)

            caisse = get("facture_numero_caisse", "01") or "01"
            self.edit_caisse.setText(caisse)

            if hasattr(self, "spin_max_postes"):
                self.spin_max_postes.setValue(
                    int(get("max_postes", 100) or 100))

            if hasattr(self, "spin_taux_change"):
                try:
                    taux = float(get("taux_change", 2250.0) or 2250.0)
                except Exception:
                    taux = 2250.0
                self.spin_taux_change.setValue(taux)

                can_edit = (self.is_owner or self.is_developer
                            or self.role == "ADMIN")
                self.spin_taux_change.setEnabled(can_edit)
                if not can_edit:
                    self.spin_taux_change.setToolTip(
                        "Réservé aux administrateurs")
        except Exception:
            logger.exception("Erreur chargement vente")

    def _load_facturation(self):
        try:
            if self._is_client_readonly():
                api = get_api()
                if api is None:
                    return
                cfg = api.get_full_config()
                get = lambda k, d: cfg.get(k, d)
            else:
                get = lambda k, d: db.get_config(k, d)

            self.chk_impression_auto.setChecked(
                bool(get("impression_facture_auto", True)))
            self.chk_qrcode.setChecked(
                bool(get("qrcode_actif", True)))

            mentions = get("mentions_ticket", None)
            if not isinstance(mentions, list) or not mentions:
                mentions = [
                    "Les médicaments vendus ne sont ni repris ni échangés",
                    "À conserver hors de la portée des enfants",
                    "Signature ou cachet de la pharmacie",
                ]
            self.edit_mentions.setPlainText("\n".join(mentions))
        except Exception:
            logger.exception("Erreur chargement facturation")

    def _load_sauvegarde(self):
        try:
            if self._is_client_readonly():
                api = get_api()
                if api is None:
                    return
                cfg = api.get_full_config()
                get = lambda k, d: cfg.get(k, d)
            else:
                get = lambda k, d: db.get_config(k, d)

            self.chk_sauvegarde_auto.setChecked(
                bool(get("sauvegarde_auto", False)))
            self.spin_freq_save.setValue(
                int(get("sauvegarde_intervalle_jours", 7) or 7))
            self.spin_max_save.setValue(
                int(get("sauvegarde_max_conservees", 10) or 10))

            self.edit_dossier_save.setText(
                get("backup_dir", "")
                or backup_engine.DEFAULT_BACKUP_DIR)

            if hasattr(self, "chk_backup_secondary"):
                self.chk_backup_secondary.setChecked(
                    bool(get("backup_secondary_enabled", False)))
            if hasattr(self, "edit_backup_secondary"):
                self.edit_backup_secondary.setText(
                    get("backup_secondary_dir", "") or "")
        except Exception:
            logger.exception("Erreur chargement sauvegarde")

    def _load_securite(self):
        try:
            if self._is_client_readonly():
                api = get_api()
                if api is None:
                    return
                cfg = api.get_full_config()
                get = lambda k, d: cfg.get(k, d)
            else:
                get = lambda k, d: db.get_config(k, d)

            self.spin_pwd_min.setValue(
                int(get("pwd_min_length", 8) or 8))
            self.spin_pwd_exp.setValue(
                int(get("pwd_expiration_days", 0) or 0))
            self.chk_require_digit.setChecked(
                bool(get("pwd_require_digit", False)))
            self.chk_require_upper.setChecked(
                bool(get("pwd_require_upper", False)))
            self.chk_require_special.setChecked(
                bool(get("pwd_require_special", False)))

            # ─── Actions critiques ───
            if hasattr(self, "chk_require_pwd_critical"):
                self.chk_require_pwd_critical.setChecked(
                    bool(get("require_password_critical", False)))
            self.chk_backup_urgence.setChecked(
                bool(get("backup_urgence_auto", True)))

            # ─── Seuil stock ───
            self.spin_seuil_stock.setValue(
                int(get("seuil_stock", 20) or 20))

            # ─── Max postes (onglet Vente) ───
            if hasattr(self, "spin_max_postes"):
                self.spin_max_postes.setValue(
                    int(get("max_postes", 100) or 100))

            # ─── SÉCURITÉ PC CLIENT ───
            if hasattr(self, "chk_allow_admin_client"):
                self.chk_allow_admin_client.setChecked(
                    bool(get("allow_admin_on_client", True)))

        except Exception:
            logger.exception("Erreur chargement sécurité")

    def _load_imprimantes(self):
        """Charge les 2 imprimantes (ticket + rapport)."""
        try:
            printers = printer_manager.list_printers()

            # ─── TICKET ───
            if hasattr(self, "combo_printer_ticket"):
                self.combo_printer_ticket.clear()
                if not printers:
                    self.combo_printer_ticket.addItem(
                        "(Aucune imprimante détectée)")
                    self.combo_printer_ticket.setEnabled(False)
                else:
                    self.combo_printer_ticket.addItem(
                        "(Aucune — désactiver)")
                    self.combo_printer_ticket.addItems(printers)
                    current = printer_manager.get_ticket_printer()
                    if current:
                        idx = self.combo_printer_ticket.findText(current)
                        if idx >= 0:
                            self.combo_printer_ticket.setCurrentIndex(idx)
                    self.combo_printer_ticket.setEnabled(True)

            # ─── RAPPORT ───
            if hasattr(self, "combo_printer_report"):
                self.combo_printer_report.clear()
                if not printers:
                    self.combo_printer_report.addItem(
                        "(Aucune imprimante détectée)")
                    self.combo_printer_report.setEnabled(False)
                else:
                    self.combo_printer_report.addItem(
                        "(Aucune — désactiver)")
                    self.combo_printer_report.addItems(printers)
                    current = printer_manager.get_report_printer()
                    if current:
                        idx = self.combo_printer_report.findText(current)
                        if idx >= 0:
                            self.combo_printer_report.setCurrentIndex(idx)
                    self.combo_printer_report.setEnabled(True)

            # ─── Checkboxes ───
            if hasattr(self, "chk_auto_print"):
                self.chk_auto_print.setChecked(
                    bool(db.get_config("printer_auto_print", False)))
            if hasattr(self, "chk_auto_print_report"):
                self.chk_auto_print_report.setChecked(
                    bool(db.get_config(
                        "printer_auto_print_report", False)))
            if hasattr(self, "chk_auto_open_pdf"):
                self.chk_auto_open_pdf.setChecked(
                    bool(db.get_config("printer_auto_open", True)))

        except Exception:
            logger.exception("Erreur chargement imprimantes")

    # ══════════════════════════════════════════════════════════════
    # Onglet Réseau (dynamique)
    # ══════════════════════════════════════════════════════════════
    def _install_server_config_button(self) -> None:
        """Crée un onglet 'Réseau' dédié à la configuration serveur."""
        try:
            if getattr(self, "_server_tab_installed", False):
                return
            self._server_tab_installed = True

            tab = QtWidgets.QWidget()
            tab.setObjectName("tab_reseau")
            tab.setStyleSheet(
                "QWidget#tab_reseau { background: transparent; }")

            v = QtWidgets.QVBoxLayout(tab)
            v.setContentsMargins(24, 24, 24, 24)
            v.setSpacing(16)

            # ─── CARTE 1 : Header ───
            header_card = QtWidgets.QFrame()
            header_card.setObjectName("header_card")
            header_card.setStyleSheet("""
                QFrame#header_card {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1d4ed8, stop:1 #4f46e5);
                    border: none;
                    border-radius: 18px;
                }
                QFrame#header_card QLabel {
                    background: transparent;
                    border: none;
                    color: #ffffff;
                }
            """)
            h_header = QtWidgets.QHBoxLayout(header_card)
            h_header.setContentsMargins(24, 20, 24, 20)
            h_header.setSpacing(16)

            ico = QtWidgets.QLabel()
            ico.setFixedSize(56, 56)
            ico.setAlignment(Qt.AlignCenter)
            ico.setStyleSheet("""
                QLabel {
                    background: rgba(255,255,255,0.15);
                    border: 1px solid rgba(255,255,255,0.3);
                    border-radius: 14px;
                    padding: 10px;
                }
            """)
            pix = QtGui.QPixmap(":/Icon/Icons/server_white.svg")
            if not pix.isNull():
                ico.setPixmap(pix.scaled(
                    28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            h_header.addWidget(ico)

            titles = QtWidgets.QVBoxLayout()
            titles.setSpacing(2)
            t1 = QtWidgets.QLabel("Configuration réseau")
            t1.setStyleSheet(
                "font-size: 20px; font-weight: 800; color: #ffffff; "
                "background: transparent; border: none;")
            titles.addWidget(t1)
            t2 = QtWidgets.QLabel(
                "Définissez le rôle de ce poste : serveur principal "
                "ou client.")
            t2.setStyleSheet(
                "font-size: 12px; color: rgba(255,255,255,0.85); "
                "background: transparent; border: none;")
            titles.addWidget(t2)
            h_header.addLayout(titles)
            h_header.addStretch()
            v.addWidget(header_card)

            # ─── CARTE 2 : État actuel ───
            status_card = QtWidgets.QFrame()
            status_card.setObjectName("status_card")
            status_card.setStyleSheet("""
                QFrame#status_card {
                    background: #ffffff;
                    border: 1px solid #e6ebf2;
                    border-radius: 16px;
                }
                QFrame#status_card QLabel {
                    background: transparent;
                    border: none;
                }
            """)
            v_status = QtWidgets.QVBoxLayout(status_card)
            v_status.setContentsMargins(24, 20, 24, 20)
            v_status.setSpacing(10)

            h_stat = QtWidgets.QHBoxLayout()
            h_stat.setSpacing(10)
            ico_stat = QtWidgets.QLabel()
            ico_stat.setFixedSize(32, 32)
            ico_stat.setAlignment(Qt.AlignCenter)
            ico_stat.setStyleSheet("""
                QLabel {
                    background: #eff6ff;
                    border: 1px solid #dbeafe;
                    border-radius: 10px;
                }
            """)
            pix_stat = QtGui.QPixmap(":/Icon/Icons/activity.svg")
            if not pix_stat.isNull():
                ico_stat.setPixmap(pix_stat.scaled(
                    18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            h_stat.addWidget(ico_stat)
            lbl_act = QtWidgets.QLabel("Mode actuel")
            lbl_act.setStyleSheet(
                "font-size: 13px; font-weight: 800; color: #0f172a; "
                "background: transparent; border: none;")
            h_stat.addWidget(lbl_act)
            h_stat.addStretch()
            v_status.addLayout(h_stat)

            self._lbl_server_mode = QtWidgets.QLabel("—")
            self._lbl_server_mode.setStyleSheet(
                "font-size: 24px; font-weight: 800; color: #0f172a; "
                "background: transparent; border: none; padding-top: 4px;")
            v_status.addWidget(self._lbl_server_mode)

            self._lbl_server_details = QtWidgets.QLabel("—")
            self._lbl_server_details.setStyleSheet(
                "font-size: 12px; color: #64748b; "
                "background: transparent; border: none;")
            self._lbl_server_details.setWordWrap(True)
            v_status.addWidget(self._lbl_server_details)
            v.addWidget(status_card)

            # ─── CARTE 3 : Bouton configurer ───
            action_card = QtWidgets.QFrame()
            action_card.setObjectName("action_card")
            action_card.setStyleSheet("""
                QFrame#action_card {
                    background: #ffffff;
                    border: 1px solid #e6ebf2;
                    border-radius: 16px;
                }
                QFrame#action_card QLabel {
                    background: transparent;
                    border: none;
                }
            """)
            v_action = QtWidgets.QVBoxLayout(action_card)
            v_action.setContentsMargins(24, 20, 24, 20)
            v_action.setSpacing(14)

            sub_act = QtWidgets.QLabel(
                "Changer le rôle de ce poste ou reconfigurer la "
                "connexion au serveur distant.")
            sub_act.setStyleSheet(
                "font-size: 12px; color: #475569; "
                "background: transparent; border: none;")
            sub_act.setWordWrap(True)
            v_action.addWidget(sub_act)

            btn_config = QtWidgets.QPushButton("  Configurer le réseau")
            btn_config.setMinimumHeight(48)
            btn_config.setCursor(QtCore.Qt.PointingHandCursor)
            btn_config.setIcon(
                QtGui.QIcon(":/Icon/Icons/settings_white.svg"))
            btn_config.setIconSize(QtCore.QSize(18, 18))
            btn_config.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3b82f6, stop:1 #2563eb);
                    color: #ffffff;
                    border: 1px solid #1d4ed8;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-weight: 800;
                    font-size: 13px;
                }
                QPushButton:hover { background: #1d4ed8; }
                QPushButton:pressed { background: #1e40af; }
            """)
            btn_config.clicked.connect(self._on_server_config_clicked)
            v_action.addWidget(btn_config)
            v.addWidget(action_card)

            # ─── CARTE 4 : Aide ───
            help_card = QtWidgets.QFrame()
            help_card.setObjectName("help_card")
            help_card.setStyleSheet("""
                QFrame#help_card {
                    background: #f8fafc;
                    border: 1px solid #e6ebf2;
                    border-radius: 16px;
                }
                QFrame#help_card QLabel {
                    background: transparent;
                    border: none;
                }
            """)
            v_help = QtWidgets.QVBoxLayout(help_card)
            v_help.setContentsMargins(24, 20, 24, 20)
            v_help.setSpacing(12)

            h_help = QtWidgets.QHBoxLayout()
            h_help.setSpacing(10)
            ico_help = QtWidgets.QLabel()
            ico_help.setFixedSize(32, 32)
            ico_help.setAlignment(Qt.AlignCenter)
            ico_help.setStyleSheet("""
                QLabel {
                    background: #fef3c7;
                    border: 1px solid #fde68a;
                    border-radius: 10px;
                }
            """)
            pix_help = QtGui.QPixmap(":/Icon/Icons/info.svg")
            if not pix_help.isNull():
                ico_help.setPixmap(pix_help.scaled(
                    18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            h_help.addWidget(ico_help)
            lbl_help_title = QtWidgets.QLabel("Comment ça marche ?")
            lbl_help_title.setStyleSheet(
                "font-size: 13px; font-weight: 800; color: #0f172a; "
                "background: transparent; border: none;")
            h_help.addWidget(lbl_help_title)
            h_help.addStretch()
            v_help.addLayout(h_help)

            help_text = QtWidgets.QLabel(
                "<b>Serveur</b> — ce poste héberge la base de données. "
                "Il doit être allumé pour que les autres postes "
                "fonctionnent.<br><br>"
                "<b>Client</b> — ce poste se connecte à un serveur "
                "distant en réseau. Saisissez l'adresse IP du serveur "
                "principal.<br><br>"
                "Après tout changement, <b>redémarrez l'application</b> "
                "pour appliquer la nouvelle configuration.")
            help_text.setWordWrap(True)
            help_text.setStyleSheet(
                "font-size: 12px; color: #475569; line-height: 1.7; "
                "background: transparent; border: none;")
            v_help.addWidget(help_text)
            v.addWidget(help_card)

            v.addStretch()

            if hasattr(self, "tabs"):
                self.tabs.addTab(tab, "Réseau")
                logger.info("Onglet 'Réseau' ajouté aux paramètres")

            self._refresh_server_status()

        except Exception:
            logger.exception("Erreur installation onglet Réseau")

    # ══════════════════════════════════════════════════════════════
    # Onglet Système (dynamique)
    # ══════════════════════════════════════════════════════════════
    def _install_system_tab(self):
        """Onglet Système : disque, réseau, logs."""
        try:
            tab = QtWidgets.QWidget()
            v = QtWidgets.QVBoxLayout(tab)
            v.setContentsMargins(24, 24, 24, 24)
            v.setSpacing(14)

            card_disk = self._make_status_card("💾 Espace disque")
            self._lbl_disk = QtWidgets.QLabel("—")
            self._lbl_disk.setStyleSheet(
                "color: #0f172a; font-size: 13px; font-weight: 600;")
            card_disk.layout().addWidget(self._lbl_disk)

            self._bar_disk = QtWidgets.QProgressBar()
            self._bar_disk.setRange(0, 100)
            self._bar_disk.setFixedHeight(10)
            card_disk.layout().addWidget(self._bar_disk)
            v.addWidget(card_disk)

            card_net = self._make_status_card("🌐 État réseau")
            self._lbl_net = QtWidgets.QLabel("—")
            self._lbl_net.setStyleSheet(
                "color: #0f172a; font-size: 13px; font-weight: 600;")
            card_net.layout().addWidget(self._lbl_net)
            v.addWidget(card_net)

            card_db = self._make_status_card("🗄️ Base de données")
            self._lbl_db = QtWidgets.QLabel("—")
            self._lbl_db.setStyleSheet(
                "color: #0f172a; font-size: 13px; font-weight: 600;")
            self._lbl_db.setWordWrap(True)
            card_db.layout().addWidget(self._lbl_db)
            v.addWidget(card_db)

            card_logs = self._make_status_card("📋 Logs récents")
            self._lbl_logs = QtWidgets.QLabel("—")
            self._lbl_logs.setStyleSheet(
                "color: #64748b; font-size: 12px;")
            self._lbl_logs.setWordWrap(True)
            card_logs.layout().addWidget(self._lbl_logs)
            v.addWidget(card_logs)

            v.addStretch()

            h = QtWidgets.QHBoxLayout()
            h.addStretch()
            btn = QtWidgets.QPushButton("  Actualiser l'état")
            btn.clicked.connect(self._refresh_system_status)
            h.addWidget(btn)
            v.addLayout(h)

            if hasattr(self, "tabs"):
                self.tabs.addTab(tab, "Système")

            self._refresh_system_status()

        except Exception:
            logger.exception("Erreur onglet système")

    def _make_status_card(self, title: str) -> QtWidgets.QFrame:
        card = QtWidgets.QFrame()
        card.setStyleSheet(
            "QFrame { background: #ffffff; border: 1px solid #e2e8f0; "
            "border-radius: 12px; }")
        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(20, 16, 20, 16)
        v.setSpacing(10)
        lbl = QtWidgets.QLabel(title)
        lbl.setStyleSheet(
            "color: #023E8A; font-size: 13px; font-weight: 800;")
        v.addWidget(lbl)
        return card

    def _refresh_system_status(self):
        """Rafraîchit les 4 cartes système."""
        from Database import system_status

        disk = system_status.get_disk_status()
        if disk:
            txt = (f"{disk['free_gb']} Go libres sur {disk['total_gb']} Go "
                   f"({disk['used_pct']}% utilisé)")
            if disk["alerte"]:
                txt += " ⚠️ ESPACE CRITIQUE"
                self._lbl_disk.setStyleSheet(
                    "color: #b91c1c; font-size: 13px; font-weight: 700;")
            else:
                self._lbl_disk.setStyleSheet(
                    "color: #15803d; font-size: 13px; font-weight: 600;")
            self._lbl_disk.setText(txt)
            self._bar_disk.setValue(int(disk["used_pct"]))

        net = system_status.get_network_status()
        if net["reachable"]:
            txt = (f"✅ Serveur joignable — {net['host']}:{net['port']} "
                   f"({net['latency_ms']} ms)")
            self._lbl_net.setStyleSheet(
                "color: #15803d; font-size: 13px; font-weight: 600;")
        else:
            txt = (f"❌ Serveur injoignable — {net['host']}:{net['port']} "
                   f"({net.get('error', '')})")
            self._lbl_net.setStyleSheet(
                "color: #b91c1c; font-size: 13px; font-weight: 700;")
        self._lbl_net.setText(txt)

        db_st = system_status.get_db_status()
        if db_st:
            lines = [f"📁 {db_st['path']}",
                     f"📊 Taille : {db_st['size_mb']} Mo"]
            for t, n in db_st["tables"].items():
                if n > 0:
                    lines.append(
                        f"  • {t:<20} : {n:>8,}".replace(",", " "))
            self._lbl_db.setText("\n".join(lines))

        logs = system_status.get_logs_status()
        if logs:
            lines = [f"📄 {len(logs)} fichier(s) de log"]
            for lg in logs[:5]:
                lines.append(f"  • {lg['path']} ({lg['size_kb']} Ko, "
                             f"{lg['modified']})")
            self._lbl_logs.setText("\n".join(lines))
        else:
            self._lbl_logs.setText(
                "Aucun fichier .log trouvé dans logs/, Logs/ ou ./")

    def _refresh_server_status(self) -> None:
        """Met à jour l'affichage du mode serveur."""
        try:
            mode = db.get_config("server_mode", "autonome") or "autonome"
            host = db.get_config(
                "server_host", "127.0.0.1") or "127.0.0.1"
            port = int(db.get_config("server_port", 5001) or 5001)

            if mode == "client":
                self._lbl_server_mode.setText("Client")
                self._lbl_server_mode.setStyleSheet(
                    "font-size: 24px; font-weight: 800; color: #2563eb; "
                    "background: transparent; border: none; "
                    "padding-top: 4px;")
                self._lbl_server_details.setText(
                    f"Serveur cible : {host}:{port}")
            elif mode == "serveur":
                self._lbl_server_mode.setText("Serveur principal")
                self._lbl_server_mode.setStyleSheet(
                    "font-size: 24px; font-weight: 800; color: #16a34a; "
                    "background: transparent; border: none; "
                    "padding-top: 4px;")
                self._lbl_server_details.setText(
                    "Héberge les données. Démarrez le service avec : "
                    "python -m Server.run_server")
            else:
                self._lbl_server_mode.setText("Autonome")
                self._lbl_server_mode.setStyleSheet(
                    "font-size: 24px; font-weight: 800; color: #64748b; "
                    "background: transparent; border: none; "
                    "padding-top: 4px;")
                self._lbl_server_details.setText(
                    "Mode local uniquement — pas de partage réseau.")
        except Exception:
            logger.exception("Erreur refresh statut serveur")

    def _on_server_config_clicked(self) -> None:
        """Ouvre le dialogue de configuration réseau."""
        try:
            from Setting_server_config import ServerConfigDialog
            dlg = ServerConfigDialog(parent=self)
            if dlg.exec() == QtWidgets.QDialog.Accepted:
                self._refresh_server_status()
                QtWidgets.QMessageBox.information(
                    self, "Redémarrage requis",
                    "Redémarrez l'application pour appliquer "
                    "le nouveau mode réseau.")
        except Exception:
            logger.exception("Erreur ouverture config réseau")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir la configuration réseau.")

    # ══════════════════════════════════════════════════════════════
    # Monitoring — Widgets (whitelist PC)
    # ══════════════════════════════════════════════════════════════
    def _connect_monitoring_widgets(self) -> None:
        """Connecte les widgets monitoring du .ui (lecture seule)."""
        try:
            # ─── Seul bouton "Actualiser" reste actif ───
            if hasattr(self, "btn_refresh_monitoring"):
                self.btn_refresh_monitoring.clicked.connect(
                    self._refresh_monitoring_table)

            # ─── Cache le bouton "Ajouter" (NovaPharma Dev only) ───
            if hasattr(self, "btn_add_monitoring"):
                self.btn_add_monitoring.setVisible(False)

            # ─── Cache la barre d'ajout complète ───
            if hasattr(self, "monitoring_add_bar"):
                self.monitoring_add_bar.setVisible(False)

            # ─── Message lecture seule (dans tous les cas) ───
            if hasattr(self, "monitoring_client_info"):
                self.monitoring_client_info.setText(
                    "🔒  La whitelist est gérée par NovaPharma Dev. "
                    "Contactez le développeur pour ajouter ou retirer un PC.")
                self.monitoring_client_info.setVisible(True)

            # ─── Largeurs colonnes ───
            if hasattr(self, "table_monitoring"):
                h = self.table_monitoring.horizontalHeader()
                h.setSectionResizeMode(
                    0, QtWidgets.QHeaderView.ResizeToContents)
                h.setSectionResizeMode(
                    1, QtWidgets.QHeaderView.Stretch)
                h.setSectionResizeMode(
                    2, QtWidgets.QHeaderView.ResizeToContents)
                h.setSectionResizeMode(
                    3, QtWidgets.QHeaderView.ResizeToContents)
                h.setSectionResizeMode(
                    4, QtWidgets.QHeaderView.ResizeToContents)

            self._refresh_monitoring_table()
            logger.info(
                "Widgets monitoring connectés (lecture seule)")
        except Exception:
            logger.exception("Erreur connexion widgets monitoring")

    def _refresh_monitoring_table(self) -> None:
        """Charge la liste des machines whitelistées (lecture seule)."""
        try:
            if not hasattr(self, "table_monitoring"):
                return

            items = []
            max_allowed = 3

            if is_client_mode():
                api = get_api()
                if api is None:
                    return
                try:
                    data = api.list_monitoring_machines()
                    items = data.get("items", [])
                    max_allowed = int(data.get("max_allowed", 3))
                except Exception:
                    logger.exception("Erreur API monitoring list")
                    if hasattr(self, "lbl_monitoring_empty"):
                        self.lbl_monitoring_empty.setText(
                            "Impossible de charger la whitelist.")
                        self.lbl_monitoring_empty.setVisible(True)
                        self.table_monitoring.setVisible(False)
                    return
            else:
                try:
                    rows = db.query(
                        """SELECT * FROM MonitoringMachine
                           ORDER BY actif DESC, ajoute_le DESC""")
                    items = [dict(r) for r in rows]
                except Exception:
                    logger.exception("Erreur DB monitoring list")
                    return

            n_actives = sum(
                1 for it in items if int(it.get("actif") or 0) == 1)
            if hasattr(self, "monitoring_count_badge"):
                self.monitoring_count_badge.setText(
                    f"{n_actives} / {max_allowed}")

            t = self.table_monitoring
            t.blockSignals(True)
            t.setRowCount(0)

            if not items:
                if hasattr(self, "lbl_monitoring_empty"):
                    self.lbl_monitoring_empty.setVisible(True)
                t.setVisible(False)
                t.blockSignals(False)
                return

            if hasattr(self, "lbl_monitoring_empty"):
                self.lbl_monitoring_empty.setVisible(False)
            t.setVisible(True)
            t.setRowCount(len(items))

            fn = QtGui.QFont("Segoe UI", 10)
            fm = QtGui.QFont("Courier New", 9)
            fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)

            for i, it in enumerate(items):
                mid = str(it.get("machine_id") or "")
                mid_short = (mid[:12] + "…") if len(mid) > 12 else mid
                it0 = QtWidgets.QTableWidgetItem(mid_short)
                it0.setFont(fm)
                it0.setForeground(QtGui.QColor("#475569"))
                it0.setToolTip(mid)
                t.setItem(i, 0, it0)

                it1 = QtWidgets.QTableWidgetItem(
                    str(it.get("hostname") or "—"))
                it1.setFont(fb)
                it1.setForeground(QtGui.QColor("#0f172a"))
                t.setItem(i, 1, it1)

                role = str(it.get("role_autorise") or "ALL")
                role_label, fg, bg = {
                    "OWNER": ("OWNER", "#92400e", "#fef3c7"),
                    "ADMIN": ("ADMIN", "#1e40af", "#dbeafe"),
                    "DEV": ("DEV", "#4338ca", "#e0e7ff"),
                    "ALL": ("ALL", "#15803d", "#dcfce7"),
                }.get(role, (role, "#334155", "#f1f5f9"))
                it2 = QtWidgets.QTableWidgetItem(role_label)
                it2.setFont(fb)
                it2.setForeground(QtGui.QColor(fg))
                it2.setBackground(QtGui.QColor(bg))
                it2.setTextAlignment(Qt.AlignCenter)
                t.setItem(i, 2, it2)

                date = str(it.get("ajoute_le") or "—")
                if len(date) > 16:
                    date = date[:16]
                it3 = QtWidgets.QTableWidgetItem(date)
                it3.setFont(fn)
                it3.setForeground(QtGui.QColor("#64748b"))
                it3.setTextAlignment(Qt.AlignCenter)
                t.setItem(i, 3, it3)

                # Statut
                actif = int(it.get("actif") or 0) == 1
                statut = "Actif" if actif else "Inactif"
                c_statut = "#15803d" if actif else "#64748b"
                it4 = QtWidgets.QTableWidgetItem(statut)
                it4.setFont(fb)
                it4.setForeground(QtGui.QColor(c_statut))
                it4.setTextAlignment(Qt.AlignCenter)
                t.setItem(i, 4, it4)

            t.blockSignals(False)

        except Exception:
            logger.exception("Erreur refresh monitoring table")

    def _on_add_monitoring_machine(self) -> None:
        """Ajoute le PC courant à la whitelist."""
        try:
            if is_client_mode():
                QtWidgets.QMessageBox.information(
                    self, "Action non autorisée",
                    "La whitelist ne peut être modifiée que depuis "
                    "le serveur physique.")
                return

            from Database import machine_id as mid_module

            mid = mid_module.get_machine_id()
            hostname = socket.gethostname()
            role = self.combo_monitoring_role.currentData() or "ALL"
            role_label = self.combo_monitoring_role.currentText()

            rep = QtWidgets.QMessageBox.question(
                self, "Ajouter ce PC",
                f"<b>Whitelister cette machine ?</b><br><br>"
                f"<b>Hostname :</b> {hostname}<br>"
                f"<b>Machine ID :</b> <code>{mid[:16]}…</code><br>"
                f"<b>Rôle autorisé :</b> {role_label}<br><br>"
                "Cette machine pourra se connecter en mode monitoring.",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if rep != QtWidgets.QMessageBox.Yes:
                return

            # ─── Vérif limite ───
            row = db.query_one(
                "SELECT COUNT(*) AS n FROM MonitoringMachine "
                "WHERE actif = 1")
            n_actives = int(row["n"] or 0) if row else 0
            if n_actives >= 3:
                QtWidgets.QMessageBox.warning(
                    self, "Limite atteinte",
                    "Maximum 3 machines monitoring autorisées. "
                    "Retirez-en une avant d'en ajouter une nouvelle.")
                return

            # ─── Vérif unicité ───
            existing = db.query_one(
                "SELECT id FROM MonitoringMachine WHERE machine_id = ?",
                (mid,))
            if existing:
                QtWidgets.QMessageBox.information(
                    self, "Déjà présente",
                    "Cette machine est déjà dans la whitelist.")
                return

            new_id = db.new_id()
            with db.transaction():
                db.execute(
                    """INSERT INTO MonitoringMachine
                       (id, machine_id, hostname, role_autorise,
                        ajoute_par, ajoute_par_name, actif)
                       VALUES (?,?,?,?,?,?,1)""",
                    (new_id, mid, hostname, role,
                     self.user_id, self.user_name))

                audit.log(
                    "AJOUT_MONITORING_MACHINE",
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.user_name,
                    cible_type="MonitoringMachine",
                    cible_id=new_id,
                    cible_nom=hostname,
                    details={"machine_id": mid, "role_autorise": role},
                    severite="warning")

            logger.info("PC monitoring ajouté : %s (%s)", hostname, role)
            self._refresh_monitoring_table()

            QtWidgets.QMessageBox.information(
                self, "PC ajouté",
                f"Cette machine a été ajoutée à la whitelist "
                f"avec le rôle <b>{role}</b>.")

        except Exception as e:
            logger.exception("Erreur ajout monitoring machine")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'ajouter cette machine :\n{e}")

    def _on_delete_monitoring_machine(self, pk: str,
                                       hostname: str = "") -> None:
        """Supprime une machine de la whitelist."""
        try:
            if is_client_mode():
                QtWidgets.QMessageBox.information(
                    self, "Action non autorisée",
                    "La whitelist ne peut être modifiée que depuis "
                    "le serveur physique.")
                return

            label = hostname or "cette machine"
            rep = QtWidgets.QMessageBox.question(
                self, "Retirer le PC",
                f"<b>Retirer « {label} » de la whitelist ?</b><br><br>"
                "Cette machine ne pourra plus se connecter en "
                "ADMIN / OWNER / DEV.<br><br>"
                "La session en cours reste valide jusqu'au prochain login.",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if rep != QtWidgets.QMessageBox.Yes:
                return

            with db.transaction():
                db.execute(
                    "DELETE FROM MonitoringMachine WHERE id = ?", (pk,))
                audit.log(
                    "SUPPRESSION_MONITORING_MACHINE",
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.user_name,
                    cible_type="MonitoringMachine",
                    cible_id=pk,
                    cible_nom=hostname,
                    severite="warning")

            logger.info("PC monitoring supprimé : %s", hostname or pk)
            self._refresh_monitoring_table()

        except Exception as e:
            logger.exception("Erreur suppression monitoring machine")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible de retirer cette machine :\n{e}")

    # ══════════════════════════════════════════════════════════════
    # Imprimantes — actions
    # ══════════════════════════════════════════════════════════════
    def _on_refresh_printers(self):
        self._load_imprimantes()
        notify.info("Imprimantes actualisées.")

    def _on_test_print(self, kind: str = "ticket"):
        """Test d'impression pour une catégorie donnée."""
        try:
            ok = printer_manager.test_print(kind=kind)
            if ok:
                notify.success(
                    f"Page de test envoyée "
                    f"({'ticket' if kind == 'ticket' else 'rapport A4'}).")
            else:
                notify.danger(
                    "Impossible d'imprimer. Vérifiez la configuration.")
        except Exception:
            logger.exception("Erreur test impression")
            notify.danger("Erreur lors du test d'impression.")

    # ══════════════════════════════════════════════════════════════
    # Logo
    # ══════════════════════════════════════════════════════════════
    def _on_upload_logo(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Choisir un logo",
            os.path.expanduser("~"),
            "Images (*.png *.jpg *.jpeg)")
        if not path:
            return
        pix = QtGui.QPixmap(path)
        if pix.isNull():
            QtWidgets.QMessageBox.warning(
                self, "Erreur", "Impossible de charger cette image.")
            return
        try:
            os.makedirs(LOGO_DIR, exist_ok=True)
            ext = os.path.splitext(path)[1].lower()
            dest = os.path.join(
                LOGO_DIR, f"logo_{int(time.time())}{ext}")
            shutil.copyfile(path, dest)
            self._load_logo(dest)
            self._mark_dirty()
        except Exception as e:
            logger.exception("Erreur copie logo")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))

    def _on_remove_logo(self):
        if not self._logo_path:
            return
        rep = QtWidgets.QMessageBox.question(
            self, "Supprimer le logo",
            "Retirer le logo de la pharmacie ?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if rep == QtWidgets.QMessageBox.Yes:
            self._load_logo(None)
            self._mark_dirty()

    def _on_browse_save(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Dossier de sauvegarde",
            os.path.expanduser("~"))
        if path:
            self.edit_dossier_save.setText(path)

    # ══════════════════════════════════════════════════════════════
    # Danger zone
    # ══════════════════════════════════════════════════════════════
    def _on_export_db(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Exporter la base",
            f"NovaPharma_export_"
            f"{datetime.now().strftime('%Y%m%d_%H%M')}.db",
            "Base SQLite (*.db)")
        if not path:
            return
        try:
            db_path = str(db.DB_PATH)
            db.get_conn().commit()
            shutil.copyfile(db_path, path)

            try:
                taille = (os.path.getsize(path)
                          if os.path.exists(path) else 0)
                audit.log(
                    audit.ACTION_EXPORT_DATABASE,
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.user_name,
                    cible_type="database",
                    cible_id="full_export",
                    cible_nom=os.path.basename(path),
                    details={"chemin": path, "taille_octets": taille})
            except Exception:
                logger.exception("Erreur audit export DB")

            QtWidgets.QMessageBox.information(
                self, "Export réussi",
                f"Base exportée vers :\n{path}")
        except Exception as e:
            logger.exception("Erreur export DB")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))

    def _on_restore_db(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Choisir une sauvegarde",
            os.path.expanduser("~"),
            "Base SQLite (*.db)")
        if not path:
            return

        from Database import critical_actions
        if not critical_actions.require_password_and_backup(
                self, self.user_id, "Restauration base"):
            return

        rep = QtWidgets.QMessageBox.warning(
            self, "Confirmation double",
            f"<b>Remplacer la base actuelle ?</b><br><br>"
            f"Fichier : <code>{os.path.basename(path)}</code><br><br>"
            "L'application va devoir redémarrer.<br>"
            "Toutes les modifications non sauvegardées seront perdues."
            "<br><br>Confirmer ?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if rep != QtWidgets.QMessageBox.Yes:
            return

        text, ok = QtWidgets.QInputDialog.getText(
            self, "Confirmation finale",
            "Tapez RESTAURER pour confirmer :",
            QtWidgets.QLineEdit.Normal, "")
        if not ok or text.strip().upper() != "RESTAURER":
            QtWidgets.QMessageBox.information(
                self, "Annulé", "Restauration annulée.")
            return

        try:
            db.close()
            db_path = str(db.DB_PATH)
            backup = f"{db_path}.before_restore_{int(time.time())}"
            if os.path.exists(db_path):
                shutil.copyfile(db_path, backup)
            shutil.copyfile(path, db_path)

            audit.log("RESTORE_DATABASE",
                      utilisateur_id=self.user_id,
                      utilisateur_name=self.user_name,
                      details={"source": path, "backup": backup})

            QtWidgets.QMessageBox.information(
                self, "Restauration OK",
                "La base a été restaurée.\n\n"
                "L'application va se fermer. Relancez-la manuellement.")
            QtWidgets.QApplication.quit()
        except Exception as e:
            logger.exception("Erreur restauration")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))

    def _on_reset_all(self):
        rep = QtWidgets.QMessageBox.warning(
            self, "Réinitialisation complète",
            "<b>Cette action va TOUT supprimer :</b><br>"
            "• Produits<br>• Clients<br>• Ventes et historique<br>"
            "• BLF et fournisseurs<br>• Utilisateurs (sauf vous)<br>"
            "• Audit log<br><br>"
            "L'application reviendra à son état initial.<br><br>"
            "<b>Continuer ?</b>",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if rep != QtWidgets.QMessageBox.Yes:
            return

        from Database import critical_actions
        if not critical_actions.require_password_and_backup(
                self, self.user_id, "Réinitialisation complète"):
            return

        text, ok = QtWidgets.QInputDialog.getText(
            self, "Confirmation finale",
            "Tapez EFFACER pour confirmer :",
            QtWidgets.QLineEdit.Normal, "")
        if not ok or text.strip().upper() != "EFFACER":
            QtWidgets.QMessageBox.information(
                self, "Annulé", "Réinitialisation annulée.")
            return

        try:
            try:
                audit.log(
                    "RESET_DATABASE",
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.user_name,
                    cible_type="database",
                    cible_id="full_reset",
                    cible_nom="Réinitialisation complète",
                    details={
                        "confirmation": "EFFACER",
                        "timestamp": datetime.now().isoformat(),
                    },
                    severite="danger")
            except Exception:
                logger.exception("Erreur audit reset")

            db.close()
            db_path = str(db.DB_PATH)
            backup = f"{db_path}.before_reset_{int(time.time())}"
            if os.path.exists(db_path):
                shutil.copyfile(db_path, backup)

            for suffix in ("", "-wal", "-shm"):
                f = db_path + suffix
                if os.path.exists(f):
                    os.remove(f)

            QtWidgets.QMessageBox.information(
                self, "Réinitialisation",
                f"Base réinitialisée.\n\nSauvegarde : {backup}\n\n"
                "L'application va se fermer. Relancez-la pour "
                "recommencer le wizard.")
            QtWidgets.QApplication.quit()
        except Exception as e:
            logger.exception("Erreur reset")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))

    # ══════════════════════════════════════════════════════════════
    # Recharger / Enregistrer
    # ══════════════════════════════════════════════════════════════
    def _confirm_reload(self):
        if self._dirty:
            rep = QtWidgets.QMessageBox.question(
                self, "Modifications non enregistrées",
                "Vous avez des modifications non enregistrées. "
                "Les perdre et recharger ?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if rep != QtWidgets.QMessageBox.Yes:
                return
        self._load_all()
        self._mark_clean()

    def _on_save(self):
        # ─── MODE CLIENT : routeur API simplifié ───
        if self._is_client_readonly():
            self._on_save_client()
            return

        # ─── Mode serveur (code existant) ───
        if not self.is_owner and not self.is_developer:
            if self.role_readonly():
                QtWidgets.QMessageBox.warning(
                    self, "Accès refusé",
                    "Seul le propriétaire ou le développeur peut "
                    "modifier les paramètres.")
                return

        try:
            # ─── Snapshot AVANT ───
            avant_config = {
                "nom_entreprise": db.get_config("nom_entreprise", ""),
                "devise": db.get_config("devise", "FC"),
                "chiffre_affaire_periode": db.get_config(
                    "chiffre_affaire_periode", "Mois"),
                "marge_benefice": db.get_config("marge_benefice", 30),
                "qrcode_actif": db.get_config("qrcode_actif", True),
                "impression_facture_auto": db.get_config(
                    "impression_facture_auto", True),
                "sauvegarde_auto": db.get_config(
                    "sauvegarde_auto", False),
                "sauvegarde_intervalle_jours": db.get_config(
                    "sauvegarde_intervalle_jours", 7),
                "seuil_stock": db.get_config("seuil_stock", 20),
                "printer_auto_print": db.get_config(
                    "printer_auto_print", False),
            }

            with db.transaction():
                # ─── Entreprise ───
                nom = self.edit_nom.text().strip()
                if not nom:
                    raise ValueError(
                        "Le nom de la pharmacie est obligatoire.")

                type_ = self.combo_type.currentText().strip().upper()
                tel = self.edit_tel.text().strip()
                email = self.edit_email_ent.text().strip()
                adresse = self.edit_adresse.text().strip()

                ph = db.query_one(
                    "SELECT id FROM Pharmacie WHERE id = 1 LIMIT 1")
                if ph:
                    db.execute("""
                        UPDATE Pharmacie SET
                            nom = ?, type = ?, numero = ?,
                            email = ?, adresse = ?, path_logo = ?,
                            updated_at = datetime('now')
                        WHERE id = 1
                    """, (nom, type_, tel, email, adresse,
                          self._logo_path))
                else:
                    db.execute("""
                        INSERT INTO Pharmacie
                        (id, nom, type, numero, email, adresse,
                         path_logo, actif)
                        VALUES (1, ?, ?, ?, ?, ?, ?, 1)
                    """, (nom, type_, tel, email, adresse,
                          self._logo_path))

                # ─── Vente ───
                db.set_config("devise",
                              self.combo_devise.currentText(),
                              type_="str")
                db.set_config("chiffre_affaire_periode",
                              self.combo_periode_ca.currentText(),
                              type_="str")
                db.set_config("marge_benefice",
                              self.spin_marge.value(),
                              type_="float")

                # ─── Code caisse ───
                caisse = self.edit_caisse.text().strip()
                import re as _re
                if not caisse:
                    caisse = "01"
                if not _re.match(r"^\d{1,2}$", caisse):
                    raise ValueError(
                        "Code caisse invalide : 1 ou 2 chiffres "
                        "uniquement (ex : 01, 02, 15).")
                db.set_config("facture_numero_caisse",
                              caisse, type_="str")

                # ─── Max postes ───
                if hasattr(self, "spin_max_postes"):
                    db.set_config("max_postes",
                                  self.spin_max_postes.value(),
                                  type_="int")

                # ─── Taux de change ───
                if hasattr(self, "spin_taux_change"):
                    can_edit = (self.is_owner or self.is_developer
                                or self.role == "ADMIN")
                    if can_edit:
                        from Database.currency import set_taux
                        set_taux(
                            self.spin_taux_change.value(),
                            user_id=self.user_id,
                            user_name=self.user_name)

                # ─── Facturation ───
                db.set_config("impression_facture_auto",
                              self.chk_impression_auto.isChecked(),
                              type_="bool")
                db.set_config("qrcode_actif",
                              self.chk_qrcode.isChecked(),
                              type_="bool")

                mentions = [
                    m.strip() for m in
                    self.edit_mentions.toPlainText().split("\n")
                    if m.strip()
                ]
                db.set_config("mentions_ticket", mentions, type_="json")

                # ─── Sauvegarde ───
                db.set_config("sauvegarde_auto",
                              self.chk_sauvegarde_auto.isChecked(),
                              type_="bool")
                db.set_config("sauvegarde_intervalle_jours",
                              self.spin_freq_save.value(),
                              type_="int")
                db.set_config("sauvegarde_max_conservees",
                              self.spin_max_save.value(),
                              type_="int")

                dossier = self.edit_dossier_save.text().strip()
                db.set_config(
                    "backup_dir",
                    dossier or backup_engine.DEFAULT_BACKUP_DIR,
                    type_="str")

                if hasattr(self, "chk_backup_secondary"):
                    db.set_config(
                        "backup_secondary_enabled",
                        self.chk_backup_secondary.isChecked(),
                        type_="bool")
                if hasattr(self, "edit_backup_secondary"):
                    db.set_config(
                        "backup_secondary_dir",
                        self.edit_backup_secondary.text().strip(),
                        type_="str")

                # ─── Sécurité ───
                db.set_config("pwd_min_length",
                              self.spin_pwd_min.value(), type_="int")
                db.set_config("pwd_expiration_days",
                              self.spin_pwd_exp.value(), type_="int")
                db.set_config("pwd_require_digit",
                              self.chk_require_digit.isChecked(),
                              type_="bool")
                db.set_config("pwd_require_upper",
                              self.chk_require_upper.isChecked(),
                              type_="bool")
                db.set_config("pwd_require_special",
                              self.chk_require_special.isChecked(),
                              type_="bool")

                if hasattr(self, "chk_require_pwd_critical"):
                    db.set_config(
                        "require_password_critical",
                        self.chk_require_pwd_critical.isChecked(),
                        type_="bool")
                db.set_config("backup_urgence_auto",
                              self.chk_backup_urgence.isChecked(),
                              type_="bool")

                db.set_config("seuil_stock",
                              self.spin_seuil_stock.value(),
                              type_="int")

                # ─── SÉCURITÉ PC CLIENT ───
                if hasattr(self, "chk_allow_admin_client"):
                    db.set_config(
                        "allow_admin_on_client",
                        self.chk_allow_admin_client.isChecked(),
                        type_="bool")

                # ─── Impression : TICKET ───
                if hasattr(self, "combo_printer_ticket"):
                    name = self.combo_printer_ticket.currentText()
                    if name.startswith("("):
                        name = ""
                    printer_manager.set_ticket_printer(name)

                # ─── Impression : RAPPORT ───
                if hasattr(self, "combo_printer_report"):
                    name = self.combo_printer_report.currentText()
                    if name.startswith("("):
                        name = ""
                    printer_manager.set_report_printer(name)

                # ─── Auto-print ───
                if hasattr(self, "chk_auto_print"):
                    db.set_config("printer_auto_print",
                                  self.chk_auto_print.isChecked(),
                                  type_="bool")
                if hasattr(self, "chk_auto_print_report"):
                    db.set_config(
                        "printer_auto_print_report",
                        self.chk_auto_print_report.isChecked(),
                        type_="bool")
                if hasattr(self, "chk_auto_open_pdf"):
                    db.set_config(
                        "printer_auto_open",
                        self.chk_auto_open_pdf.isChecked(),
                        type_="bool")

                audit.log("MODIF_CONFIG",
                          utilisateur_id=self.user_id,
                          utilisateur_name=self.user_name,
                          cible_type="configuration",
                          details={"source": "page_parametres"})

            # ═══ AUDIT CONFIG (diff) ═══
            try:
                apres_config = {
                    "nom_entreprise": db.get_config(
                        "nom_entreprise", ""),
                    "devise": db.get_config("devise", "FC"),
                    "chiffre_affaire_periode": db.get_config(
                        "chiffre_affaire_periode", "Mois"),
                    "marge_benefice": db.get_config(
                        "marge_benefice", 30),
                    "qrcode_actif": db.get_config(
                        "qrcode_actif", True),
                    "impression_facture_auto": db.get_config(
                        "impression_facture_auto", True),
                    "sauvegarde_auto": db.get_config(
                        "sauvegarde_auto", False),
                    "sauvegarde_intervalle_jours": db.get_config(
                        "sauvegarde_intervalle_jours", 7),
                    "seuil_stock": db.get_config("seuil_stock", 20),
                    "printer_auto_print": db.get_config(
                        "printer_auto_print", False),
                }
                d = audit.diff(avant_config, apres_config)
                if d["champs_modifies"]:
                    audit.log(
                        audit.ACTION_MODIF_CONFIG,
                        utilisateur_id=self.user_id,
                        utilisateur_name=self.user_name,
                        cible_type="Configuration",
                        cible_id="system",
                        cible_nom="Paramètres système",
                        details={
                            "champs_modifies": list(
                                d["champs_modifies"].keys()),
                            "source": "page_parametres",
                        },
                        avant=avant_config,
                        apres=apres_config)
            except Exception:
                logger.exception("Erreur audit config")

            logger.info("Paramètres enregistrés")
            self._mark_clean()
            self.parametres_changed.emit()

        except ValueError as ve:
            QtWidgets.QMessageBox.warning(
                self, "Champ manquant", str(ve))
        except Exception as e:
            logger.exception("Erreur sauvegarde paramètres")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'enregistrer :\n{e}")

    def _on_save_client(self) -> None:
        """
        En mode client, seuls 2 types de paramètres sont modifiables :
          1. allow_admin_on_client (API)
          2. Imprimantes (QSettings locales)
        """
        try:
            api = get_api()
            if api is None:
                QtWidgets.QMessageBox.critical(
                    self, "Erreur", "API non initialisée.")
                return

            # ─── 1. Config serveur modifiable ───
            updates = {}
            if hasattr(self, "chk_allow_admin_client"):
                new_val = self.chk_allow_admin_client.isChecked()
                current = None
                try:
                    cfg = api.get_full_config()
                    current = bool(cfg.get(
                        "allow_admin_on_client", True))
                except Exception:
                    pass
                if current is not None and new_val != current:
                    updates["allow_admin_on_client"] = new_val

            # ─── 2. Imprimantes (QSettings locales) ───
            try:
                if hasattr(self, "combo_printer_ticket"):
                    name = self.combo_printer_ticket.currentText()
                    if name.startswith("("):
                        name = ""
                    printer_manager.set_ticket_printer(name)

                if hasattr(self, "combo_printer_report"):
                    name = self.combo_printer_report.currentText()
                    if name.startswith("("):
                        name = ""
                    printer_manager.set_report_printer(name)

                if hasattr(self, "chk_auto_print"):
                    # Auto-print est global → API
                    cfg = api.get_full_config()
                    cur_ap = bool(cfg.get("printer_auto_print", False))
                    new_ap = self.chk_auto_print.isChecked()
                    if cur_ap != new_ap:
                        updates["printer_auto_print"] = new_ap

                if hasattr(self, "chk_auto_print_report"):
                    cfg = api.get_full_config()
                    cur_ar = bool(cfg.get(
                        "printer_auto_print_report", False))
                    new_ar = self.chk_auto_print_report.isChecked()
                    if cur_ar != new_ar:
                        updates["printer_auto_print_report"] = new_ar

                if hasattr(self, "chk_auto_open_pdf"):
                    cfg = api.get_full_config()
                    cur_ao = bool(cfg.get("printer_auto_open", True))
                    new_ao = self.chk_auto_open_pdf.isChecked()
                    if cur_ao != new_ao:
                        updates["printer_auto_open"] = new_ao
            except Exception:
                logger.exception("Erreur save imprimantes (local)")

            # ─── 3. Envoi API ───
            if updates:
                api.save_config(updates)
                logger.info(
                    "Config mise à jour via API (client) : %s",
                    list(updates.keys()))

            self._mark_clean()
            self.parametres_changed.emit()

            QtWidgets.QMessageBox.information(
                self, "Modifications enregistrées",
                "Les paramètres modifiables en mode client "
                "ont été enregistrés.")

        except Exception as e:
            logger.exception("Erreur save client")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'enregistrer :\n{e}")

    # ══════════════════════════════════════════════════════════════
    # ONGLET LICENCE (Phase 2+)
    # ══════════════════════════════════════════════════════════════
    def _install_license_tab(self) -> None:
        """Crée l'onglet Licence avec Machine ID, activation et contact."""
        try:
            if getattr(self, "_license_tab_installed", False):
                return
            self._license_tab_installed = True

            tab = QtWidgets.QWidget()
            tab.setObjectName("tab_licence")
            tab.setStyleSheet(
                "QWidget#tab_licence { background: transparent; }")

            v = QtWidgets.QVBoxLayout(tab)
            v.setContentsMargins(24, 24, 24, 24)
            v.setSpacing(16)

            # Carte 1 : État actuel
            self._license_status_card = self._make_license_status_card()
            v.addWidget(self._license_status_card)

            # Carte 2 : Machine ID + clé
            v.addWidget(self._make_license_key_card())

            # Carte 3 : Contact
            v.addWidget(self._make_license_contact_card())

            v.addStretch()

            if hasattr(self, "tabs"):
                self.tabs.addTab(tab, "Licence")
                logger.info("Onglet 'Licence' ajouté aux paramètres")

            # Met à jour l'état
            self._refresh_license_status()

        except Exception:
            logger.exception("Erreur installation onglet Licence")

    def _make_license_status_card(self) -> QtWidgets.QFrame:
        """Carte qui montre l'état actuel de la licence."""
        card = QtWidgets.QFrame()
        card.setObjectName("license_status_card")
        card.setStyleSheet("""
            QFrame#license_status_card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1d4ed8, stop:1 #4f46e5);
                border: none;
                border-radius: 16px;
            }
            QFrame#license_status_card QLabel {
                background: transparent;
                border: none;
                color: #ffffff;
            }
        """)
        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(24, 20, 24, 20)
        v.setSpacing(8)

        # Titre
        t1 = QtWidgets.QLabel("État de votre licence")
        t1.setStyleSheet(
            "font-size: 14px; font-weight: 700; "
            "color: rgba(255,255,255,0.85);")
        v.addWidget(t1)

        # Statut principal
        self._lbl_license_status = QtWidgets.QLabel("—")
        self._lbl_license_status.setStyleSheet(
            "font-size: 26px; font-weight: 800; color: #ffffff; "
            "padding-top: 4px;")
        v.addWidget(self._lbl_license_status)

        # Détail
        self._lbl_license_detail = QtWidgets.QLabel("")
        self._lbl_license_detail.setStyleSheet(
            "font-size: 12px; color: rgba(255,255,255,0.85);")
        v.addWidget(self._lbl_license_detail)

        return card

    def _make_license_key_card(self) -> QtWidgets.QFrame:
        """Carte avec Machine ID + champ clé + bouton activer."""
        card = QtWidgets.QFrame()
        card.setObjectName("license_key_card")
        card.setStyleSheet("""
            QFrame#license_key_card {
                background: #ffffff;
                border: 1px solid #e6ebf2;
                border-radius: 16px;
            }
            QFrame#license_key_card QLabel {
                background: transparent;
                border: none;
            }
        """)
        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(24, 20, 24, 20)
        v.setSpacing(12)

        # Header
        h = QtWidgets.QHBoxLayout()
        ico = QtWidgets.QLabel("🔐")
        ico.setStyleSheet("font-size: 18px;")
        h.addWidget(ico)
        title = QtWidgets.QLabel("Activation de la licence")
        title.setStyleSheet(
            "font-size: 15px; font-weight: 800; color: #0f172a;")
        h.addWidget(title)
        h.addStretch()
        v.addLayout(h)

        # Machine ID
        lbl_mid = QtWidgets.QLabel("VOTRE MACHINE ID")
        lbl_mid.setStyleSheet(
            "color: #94a3b8; font-size: 10px; font-weight: 800; "
            "letter-spacing: 1px;")
        v.addWidget(lbl_mid)

        h_mid = QtWidgets.QHBoxLayout()
        h_mid.setSpacing(8)

        from Database import machine_id as mid_module
        self._license_mid = mid_module.get_machine_id()

        inp_mid = QtWidgets.QLineEdit(self._license_mid)
        inp_mid.setReadOnly(True)
        inp_mid.setStyleSheet("""
            QLineEdit {
                background: #f1f5f9;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 10px 14px;
                color: #64748b;
                font-family: 'Courier New';
                font-size: 11px;
            }
        """)
        h_mid.addWidget(inp_mid, 1)

        btn_copy = QtWidgets.QPushButton("📋")
        btn_copy.setFixedSize(42, 42)
        btn_copy.setCursor(Qt.PointingHandCursor)
        btn_copy.setToolTip("Copier le Machine ID")
        btn_copy.setStyleSheet("""
            QPushButton {
                background: #f8fafc;
                border: 1px solid #dbe3ec;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover { background: #eff6ff; }
        """)
        btn_copy.clicked.connect(
            lambda: QtWidgets.QApplication.clipboard().setText(
                self._license_mid))
        h_mid.addWidget(btn_copy)
        v.addLayout(h_mid)

        hint = QtWidgets.QLabel(
            "Envoyez ce Machine ID à TEAM NOVA pour recevoir votre clé "
            "de licence.")
        hint.setStyleSheet(
            "color: #94a3b8; font-size: 10px; font-style: italic;")
        hint.setWordWrap(True)
        v.addWidget(hint)

        # Champ clé
        lbl_key = QtWidgets.QLabel("CLÉ DE LICENCE")
        lbl_key.setStyleSheet(
            "color: #94a3b8; font-size: 10px; font-weight: 800; "
            "letter-spacing: 1px; padding-top: 6px;")
        v.addWidget(lbl_key)

        self._license_input_key = QtWidgets.QLineEdit()
        self._license_input_key.setPlaceholderText(
            "NOVA-XXXX-XXXX-XXXX-XXXX")
        self._license_input_key.setMinimumHeight(46)
        self._license_input_key.setStyleSheet("""
            QLineEdit {
                background: #f8fafc;
                border: 1.5px solid #dbe3ec;
                border-radius: 10px;
                padding: 12px 14px;
                color: #0f172a;
                font-family: 'Courier New';
                font-size: 13px;
                font-weight: 700;
            }
            QLineEdit:focus { border-color: #0077B6; }
        """)
        self._license_input_key.returnPressed.connect(
            self._on_activate_license)
        v.addWidget(self._license_input_key)

        # Bouton activer
        btn_activate = QtWidgets.QPushButton("  Activer ma licence")
        btn_activate.setMinimumHeight(46)
        btn_activate.setCursor(Qt.PointingHandCursor)
        btn_activate.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: #ffffff;
                border: 1px solid #1d4ed8;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 13px;
                font-weight: 800;
            }
            QPushButton:hover { background: #1d4ed8; }
        """)
        btn_activate.clicked.connect(self._on_activate_license)
        v.addWidget(btn_activate)

        return card

    def _make_license_contact_card(self) -> QtWidgets.QFrame:
        """Carte avec les 3 canaux de contact."""
        card = QtWidgets.QFrame()
        card.setObjectName("license_contact_card")
        card.setStyleSheet("""
            QFrame#license_contact_card {
                background: #eff6ff;
                border: 1px solid #bfdbfe;
                border-radius: 16px;
            }
            QFrame#license_contact_card QLabel {
                background: transparent;
                border: none;
            }
        """)
        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(24, 20, 24, 20)
        v.setSpacing(12)

        # Titre
        title = QtWidgets.QLabel("💡 Besoin d'une licence ?")
        title.setStyleSheet(
            "font-size: 14px; font-weight: 800; color: #023E8A;")
        v.addWidget(title)

        sub = QtWidgets.QLabel(
            "Contactez TEAM NOVA pour obtenir votre clé d'activation :")
        sub.setStyleSheet("font-size: 11px; color: #1e40af;")
        v.addWidget(sub)

        # 3 boutons
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(10)

        # WhatsApp
        btn_wa = QtWidgets.QPushButton(
            "  WhatsApp\n  +243 808 775 085")
        btn_wa.setMinimumHeight(52)
        btn_wa.setCursor(Qt.PointingHandCursor)
        btn_wa.setStyleSheet("""
            QPushButton {
                background: #25D366; color: #ffffff;
                border: 1px solid #1eb955;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 11px; font-weight: 700;
                text-align: left;
            }
            QPushButton:hover { background: #1eb955; }
        """)
        btn_wa.clicked.connect(self._open_whatsapp_license)
        h.addWidget(btn_wa, 1)

        # Email
        btn_mail = QtWidgets.QPushButton(
            "  Email\n  teamnovaoff@gmail.com")
        btn_mail.setMinimumHeight(52)
        btn_mail.setCursor(Qt.PointingHandCursor)
        btn_mail.setStyleSheet("""
            QPushButton {
                background: #dc2626; color: #ffffff;
                border: 1px solid #b91c1c;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 11px; font-weight: 700;
                text-align: left;
            }
            QPushButton:hover { background: #b91c1c; }
        """)
        btn_mail.clicked.connect(self._open_email_license)
        h.addWidget(btn_mail, 1)

        # Facebook
        btn_fb = QtWidgets.QPushButton(
            "  Facebook\n  Team Nova")
        btn_fb.setMinimumHeight(52)
        btn_fb.setCursor(Qt.PointingHandCursor)
        btn_fb.setStyleSheet("""
            QPushButton {
                background: #1877F2; color: #ffffff;
                border: 1px solid #1560c4;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 11px; font-weight: 700;
                text-align: left;
            }
            QPushButton:hover { background: #1560c4; }
        """)
        btn_fb.clicked.connect(self._open_facebook_license)
        h.addWidget(btn_fb, 1)

        v.addLayout(h)
        return card

    def _refresh_license_status(self) -> None:
        """Met à jour la carte d'état (essai / licence / à vie)."""
        try:
            from Core.license_manager import (
                get_trial_days_left, _get_stored_license, _verify_license)

            # Vérifie d'abord s'il y a une licence valide
            stored = _get_stored_license()
            if stored:
                ok, payload, _ = _verify_license(stored)
                if ok:
                    # Licence à vie ?
                    if payload.get("lifetime"):
                        self._lbl_license_status.setText(
                            "✓ LICENCE À VIE")
                        self._lbl_license_detail.setText(
                            "Nova Pharma est activé définitivement.")
                        return

                    # Licence temporaire
                    import datetime as _dt
                    exp_ts = payload.get("exp", 0)
                    exp_date = _dt.datetime.fromtimestamp(
                        exp_ts).strftime("%d/%m/%Y")
                    self._lbl_license_status.setText(
                        "✓ LICENCE ACTIVE")
                    self._lbl_license_detail.setText(
                        f"Valide jusqu'au {exp_date}")
                    return

            # Sinon : essai en cours
            days = get_trial_days_left()
            if days > 0:
                self._lbl_license_status.setText(
                    f"⏱ Essai : {days} jour(s)")
                self._lbl_license_detail.setText(
                    f"Activez votre licence avant expiration pour "
                    f"continuer à utiliser Nova Pharma.")
            elif days == 0:
                self._lbl_license_status.setText("⚠ ESSAI EXPIRÉ")
                self._lbl_license_detail.setText(
                    "Saisissez votre clé ci-dessous pour continuer.")
            else:
                self._lbl_license_status.setText("—")
                self._lbl_license_detail.setText("État inconnu.")
        except Exception:
            logger.exception("Erreur refresh statut licence")
            self._lbl_license_status.setText("—")

    def _on_activate_license(self) -> None:
        """Active la licence saisie dans le champ."""
        try:
            key = self._license_input_key.text().strip().upper()

            if not key:
                QtWidgets.QMessageBox.warning(
                    self, "Clé manquante",
                    "Saisissez une clé de licence.")
                return

            from Core.license_manager import save_license, _verify_license

            ok, payload, msg = _verify_license(key)
            if not ok:
                QtWidgets.QMessageBox.critical(
                    self, "Licence invalide", msg)
                return

            if not save_license(key):
                QtWidgets.QMessageBox.critical(
                    self, "Erreur",
                    "Impossible d'enregistrer la licence.")
                return

            # Message adapté
            if payload.get("lifetime"):
                message = (
                    "✓ Licence À VIE activée !\n\n"
                    "Nova Pharma est maintenant activé définitivement.")
            else:
                import datetime as _dt
                exp_ts = payload.get("exp", 0)
                exp_date = _dt.datetime.fromtimestamp(
                    exp_ts).strftime("%d/%m/%Y")
                message = (
                    f"✓ Licence activée !\n\n"
                    f"Valide jusqu'au {exp_date}.")

            QtWidgets.QMessageBox.information(
                self, "Activation réussie", message)

            # Vide le champ et rafraîchit
            self._license_input_key.clear()
            self._refresh_license_status()

            logger.info("Licence activée depuis Paramètres")

        except Exception as e:
            logger.exception("Erreur activation licence")
            QtWidgets.QMessageBox.critical(
                self, "Erreur", f"Impossible d'activer :\n{e}")

    def _open_whatsapp_license(self) -> None:
        try:
            QtGui.QDesktopServices.openUrl(
                QtCore.QUrl("https://wa.me/243808775085"))
        except Exception:
            logger.exception("Erreur ouverture WhatsApp")

    def _open_email_license(self) -> None:
        try:
            from Database import machine_id as mid_module
            mid = mid_module.get_machine_id()
            url = QtCore.QUrl(
                f"mailto:teamnovaoff@gmail.com"
                f"?subject=Demande%20de%20licence%20Nova%20Pharma"
                f"&body=Bonjour%20TEAM%20NOVA,%0D%0A%0D%0A"
                f"Je%20souhaite%20activer%20ma%20licence%20Nova%20Pharma."
                f"%0D%0A%0D%0AMon%20Machine%20ID%20:%20{mid}")
            QtGui.QDesktopServices.openUrl(url)
        except Exception:
            logger.exception("Erreur ouverture email")

    def _open_facebook_license(self) -> None:
        try:
            QtGui.QDesktopServices.openUrl(
                QtCore.QUrl(
                    "https://web.facebook.com/people/"
                    "Team-Nova/61581757163137/"))
        except Exception:
            logger.exception("Erreur ouverture Facebook")

    def role_readonly(self):
        """Retourne True si l'utilisateur n'a pas le droit de modifier."""
        return not (self.is_owner or self.is_developer)

    # ══════════════════════════════════════════════════════════════
    # Dossiers de backup
    # ══════════════════════════════════════════════════════════════
    def _browse_backup_dir(self):
        start = (self.edit_dossier_save.text().strip()
                 or backup_engine.DEFAULT_BACKUP_DIR)
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Dossier principal de sauvegarde", start)
        if folder:
            self.edit_dossier_save.setText(folder)

    def _browse_backup_secondary(self):
        start = (self.edit_backup_secondary.text().strip()
                 or os.path.expanduser("~"))
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Dossier secondaire (USB / NAS / réseau)", start)
        if folder:
            self.edit_backup_secondary.setText(folder)

    def _on_manage_backups(self):
        try:
            from Setting_backup_manager import Setting_backup_manager
            dlg = Setting_backup_manager(
                parent=self,
                user_id=self.user_id,
                user_name=self.user_name)
            dlg.exec()
            self._load_sauvegarde()
        except Exception:
            logger.exception("Erreur ouverture gestionnaire backup")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir le gestionnaire de sauvegardes.")

    def _on_secondary_toggled(self, checked):
        if hasattr(self, "edit_backup_secondary"):
            self.edit_backup_secondary.setEnabled(checked)
        if hasattr(self, "btn_browse_backup_secondary"):
            self.btn_browse_backup_secondary.setEnabled(checked)

    # ══════════════════════════════════════════════════════════════
    # Spinbox alignment — contourne bug Qt6 sur QSpinBox
    # ══════════════════════════════════════════════════════════════
    def _fix_spinbox_alignment(self) -> None:
        """
        Force l'alignement centré sur tous les QSpinBox/QDoubleSpinBox.
        Le CSS qproperty-alignment ne marche pas sur QSpinBox (bug Qt6)
        → setAlignment() en Python contourne.
        """
        names = (
            "spin_marge", "spin_freq_save", "spin_max_save",
            "spin_pwd_min", "spin_pwd_exp", "spin_seuil_stock",
            "spin_max_postes", "spin_taux_change",
        )
        for name in names:
            w = getattr(self, name, None)
            if w is not None:
                try:
                    w.setAlignment(Qt.AlignCenter)
                except Exception:
                    logger.exception(
                        "Erreur alignment spinbox %s", name)


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    from Database import db, seed
    app = QtWidgets.QApplication(sys.argv)
    db.get_conn()
    seed.run()

    w = PageParametres(
        user_id="TEST", user_name="Test",
        role="ADMIN", is_owner=True)
    w.resize(1200, 800)
    w.show()
    sys.exit(app.exec())