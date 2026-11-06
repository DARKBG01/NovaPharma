#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_parametres.py — Page Paramètres complète.
===================================================
6 onglets : Entreprise / Vente / Facturation / Sauvegarde / Sécurité / Danger

Améliorations :
  • Détection des modifications non enregistrées
  • Feedback visuel (statut coloré)
  • Icône du header chargée
  • Sécurité renforcée pour la danger zone
"""

import logging
import os
import shutil
import time
from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import backup_engine, db, audit, printer_manager
from Interface_page_parametres import Ui_PageParametres
from Notification_manager import notify

logger = logging.getLogger(__name__)

LOGO_DIR = "Assets/Logos"


class PageParametres(QtWidgets.QWidget, Ui_PageParametres):

    parametres_changed = QtCore.Signal()

    def __init__(self, parent=None, user_id=None, user_name="",
                 is_owner=False, is_developer=False):
        super().__init__(parent)
        self.setupUi(self)
        # ─── Force tous les onglets à être actifs (bug fix) ───
        try:
            for i in range(self.tabs.count()):
                self.tabs.setTabEnabled(i, True)
                self.tabs.setTabVisible(i, True)
        except Exception:
            logger.exception("Erreur activation onglets")

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self.is_owner = is_owner
        self.is_developer = is_developer

        self._logo_path = None
        self._dirty = False          # modifs non enregistrées
        self._loading = False        # évite le dirty pendant le load

        # Init
        self._setup_header()
        self._connect_signals()
        self._apply_permissions()
        self._install_server_config_button()  # ← AJOUT
        self._install_system_tab()  # ← AJOUT
        self._load_all()
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
        # Logo
        self.btn_upload_logo.clicked.connect(self._on_upload_logo)
        self.btn_remove_logo.clicked.connect(self._on_remove_logo)

        # Sauvegarde — dossier principal
        self.btn_browse_save.clicked.connect(self._browse_backup_dir)

        # Sauvegarde — dossier secondaire (SI le widget existe)
        if hasattr(self, "btn_browse_backup_secondary"):
            self.btn_browse_backup_secondary.clicked.connect(
                self._browse_backup_secondary)

        # Gestionnaire d'archives (SI le widget existe)
        if hasattr(self, "btn_manage_backups"):
            self.btn_manage_backups.clicked.connect(
                self._on_manage_backups)

        # Case "backup secondaire" : active/désactive le champ
        if hasattr(self, "chk_backup_secondary"):
            self.chk_backup_secondary.toggled.connect(
                self._on_secondary_toggled)
            
        # Imprimantes
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

        # ─── Checkboxes ───
        if hasattr(self, "chk_auto_print"):
            self.chk_auto_print.toggled.connect(self._mark_dirty)
        if hasattr(self, "chk_auto_print_report"):
            self.chk_auto_print_report.toggled.connect(self._mark_dirty)
        if hasattr(self, "chk_auto_open_pdf"):
            self.chk_auto_open_pdf.toggled.connect(self._mark_dirty)

        # Dans _connect_signals :
        if hasattr(self, "chk_allow_admin_client"):
            self.chk_allow_admin_client.toggled.connect(self._mark_dirty)

        # Dans _load_securite :
        self.chk_allow_admin_client.setChecked(
            bool(db.get_config("allow_admin_on_client", True)))

        # Dans _on_save :
        db.set_config("allow_admin_on_client",
                      self.chk_allow_admin_client.isChecked(),
                      type_="bool")

        # Danger zone
        self.btn_export_db.clicked.connect(self._on_export_db)
        self.btn_restore_db.clicked.connect(self._on_restore_db)
        self.btn_reset_all.clicked.connect(self._on_reset_all)

        # Footer
        self.btn_save.clicked.connect(self._on_save)
        self.btn_reload.clicked.connect(self._confirm_reload)

        # Détection des modifications
        for w in (self.edit_nom, self.edit_tel, self.edit_email_ent,
                  self.edit_adresse, self.edit_caisse,
                  self.edit_dossier_save, self.edit_mentions):
            try:
                w.textChanged.connect(self._mark_dirty)
            except AttributeError:
                pass

        for c in (self.combo_type, self.combo_devise,
                  self.combo_periode_ca):
            c.currentIndexChanged.connect(self._mark_dirty)

        spin_names = (
            "spin_marge",
            "spin_freq_save",
            "spin_max_save",
            "spin_pwd_min",
            "spin_pwd_exp",
            "spin_seuil_stock",
            "spin_max_postes",
            "spin_taux_change",
        )
        for name in spin_names:
            w = getattr(self, name, None)
            if w is not None:
                try:
                    w.valueChanged.connect(self._mark_dirty)
                except Exception:
                    logger.exception(
                        "Impossible de connecter %s", name)

        # ─── Checkboxes : connexion robuste (hasattr) ───
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
                logger.warning(
                    "Widget absent du .ui : %s", name)

        # ─── Spin max_postes ───
        if hasattr(self, "spin_max_postes"):
            self.spin_max_postes.valueChanged.connect(self._mark_dirty)

        # Danger zone
        self.btn_export_db.clicked.connect(self._on_export_db)

    # ══════════════════════════════════════════════════════════════
    # Permissions
    # ══════════════════════════════════════════════════════════════
    def _apply_permissions(self):
        can_admin = (self.is_owner or self.is_developer)
        self.btn_export_db.setEnabled(can_admin)
        self.btn_restore_db.setEnabled(can_admin)
        self.btn_reset_all.setEnabled(can_admin)

        if not can_admin:
            self._set_status(
                "Seul le propriétaire ou le développeur peut effectuer "
                "certaines actions sensibles.", "warn")

    # ══════════════════════════════════════════════════════════════
    # Statut
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
            self.combo_devise.setCurrentText(
                db.get_config("devise", "FC"))
            self.combo_periode_ca.setCurrentText(
                db.get_config("chiffre_affaire_periode", "Mois"))
            try:
                marge = float(db.get_config("marge_benefice", 30))
            except Exception:
                marge = 30.0
            self.spin_marge.setValue(marge)

            # ─── Code caisse (défaut 01 au lieu de A) ───
            caisse = db.get_config("facture_numero_caisse", "01") or "01"
            self.edit_caisse.setText(caisse)

            # ─── Max postes ───
            if hasattr(self, "spin_max_postes"):
                self.spin_max_postes.setValue(
                    int(db.get_config("max_postes", 100)))

            # ─── Taux de change ───
            if hasattr(self, "spin_taux_change"):
                try:
                    taux = float(db.get_config("taux_change", 2250.0))
                except Exception:
                    taux = 2250.0
                self.spin_taux_change.setValue(taux)

                # Permission : ADMIN/OWNER/DEV uniquement
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
            self.chk_impression_auto.setChecked(
                bool(db.get_config("impression_facture_auto", True)))
            self.chk_qrcode.setChecked(
                bool(db.get_config("qrcode_actif", True)))

            mentions = db.get_config("mentions_ticket", None)
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
            from Database import backup_engine

            self.chk_sauvegarde_auto.setChecked(
                bool(db.get_config("sauvegarde_auto", False)))
            self.spin_freq_save.setValue(
                int(db.get_config("sauvegarde_intervalle_jours", 7)))
            self.spin_max_save.setValue(
                int(db.get_config("sauvegarde_max_conservees", 10)))

            # ─── NOUVEAU : dossier principal ───
            self.edit_dossier_save.setText(
                db.get_config("backup_dir", "")
                or backup_engine.DEFAULT_BACKUP_DIR)

            # ─── NOUVEAU : backup secondaire (USB/NAS) ───
            self.chk_backup_secondary.setChecked(
                bool(db.get_config("backup_secondary_enabled", False)))
            self.edit_backup_secondary.setText(
                db.get_config("backup_secondary_dir", "") or "")

        except Exception:
            logger.exception("Erreur chargement sauvegarde")

    def _install_server_config_button(self) -> None:
        """Crée un onglet 'Réseau' dédié à la configuration serveur."""
        try:
            if getattr(self, "_server_tab_installed", False):
                return
            self._server_tab_installed = True

            # ─── Crée le contenu de l'onglet ───
            tab = QtWidgets.QWidget()
            tab.setObjectName("tab_reseau")
            tab.setStyleSheet("QWidget#tab_reseau { background: transparent; }")

            v = QtWidgets.QVBoxLayout(tab)
            v.setContentsMargins(24, 24, 24, 24)
            v.setSpacing(16)

            # ═══════════════════════════════════════════════════════
            # CARTE 1 : Header avec icône + titre
            # ═══════════════════════════════════════════════════════
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

            # Icône serveur
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

            # Titres
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

            # ═══════════════════════════════════════════════════════
            # CARTE 2 : État actuel
            # ═══════════════════════════════════════════════════════
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

            # Ligne titre + pill icône
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

            # Ligne mode en gros
            self._lbl_server_mode = QtWidgets.QLabel("—")
            self._lbl_server_mode.setStyleSheet(
                "font-size: 24px; font-weight: 800; color: #0f172a; "
                "background: transparent; border: none; padding-top: 4px;")
            v_status.addWidget(self._lbl_server_mode)

            # Détails
            self._lbl_server_details = QtWidgets.QLabel("—")
            self._lbl_server_details.setStyleSheet(
                "font-size: 12px; color: #64748b; "
                "background: transparent; border: none;")
            self._lbl_server_details.setWordWrap(True)
            v_status.addWidget(self._lbl_server_details)

            v.addWidget(status_card)

            # ═══════════════════════════════════════════════════════
            # CARTE 3 : Bouton configurer
            # ═══════════════════════════════════════════════════════
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

            # Sous-titre
            sub_act = QtWidgets.QLabel(
                "Changer le rôle de ce poste ou reconfigurer la "
                "connexion au serveur distant.")
            sub_act.setStyleSheet(
                "font-size: 12px; color: #475569; "
                "background: transparent; border: none;")
            sub_act.setWordWrap(True)
            v_action.addWidget(sub_act)

            # Bouton principal
            btn_config = QtWidgets.QPushButton("  Configurer le réseau")
            btn_config.setMinimumHeight(48)
            btn_config.setCursor(QtCore.Qt.PointingHandCursor)
            btn_config.setIcon(QtGui.QIcon(":/Icon/Icons/settings_white.svg"))
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
                    text-align: center;
                }
                QPushButton:hover {
                    background: #1d4ed8;
                }
                QPushButton:pressed {
                    background: #1e40af;
                }
            """)
            btn_config.clicked.connect(self._on_server_config_clicked)
            v_action.addWidget(btn_config)

            v.addWidget(action_card)

            # ═══════════════════════════════════════════════════════
            # CARTE 4 : Aide
            # ═══════════════════════════════════════════════════════
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

            # Header aide
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

            # Texte d'aide
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

            # ─── Ajoute l'onglet au QTabWidget ───
            if hasattr(self, "tabs"):
                self.tabs.addTab(tab, "Réseau")
                logger.info("Onglet 'Réseau' ajouté aux paramètres")
            else:
                logger.warning("self.tabs introuvable — pas d'onglet")

            # ─── Charge l'état ───
            self._refresh_server_status()

        except Exception:
            logger.exception("Erreur installation onglet Réseau")

    def _install_system_tab(self):
        """Onglet Système : disque, réseau, logs."""
        try:
            tab = QtWidgets.QWidget()
            v = QtWidgets.QVBoxLayout(tab)
            v.setContentsMargins(24, 24, 24, 24)
            v.setSpacing(14)

            # ─── Carte Disque ───
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

            # ─── Carte Réseau ───
            card_net = self._make_status_card("🌐 État réseau")
            self._lbl_net = QtWidgets.QLabel("—")
            self._lbl_net.setStyleSheet(
                "color: #0f172a; font-size: 13px; font-weight: 600;")
            card_net.layout().addWidget(self._lbl_net)
            v.addWidget(card_net)

            # ─── Carte DB ───
            card_db = self._make_status_card("🗄️ Base de données")
            self._lbl_db = QtWidgets.QLabel("—")
            self._lbl_db.setStyleSheet(
                "color: #0f172a; font-size: 13px; font-weight: 600;")
            self._lbl_db.setWordWrap(True)
            card_db.layout().addWidget(self._lbl_db)
            v.addWidget(card_db)

            # ─── Carte Logs ───
            card_logs = self._make_status_card("📋 Logs récents")
            self._lbl_logs = QtWidgets.QLabel("—")
            self._lbl_logs.setStyleSheet(
                "color: #64748b; font-size: 12px;")
            self._lbl_logs.setWordWrap(True)
            card_logs.layout().addWidget(self._lbl_logs)
            v.addWidget(card_logs)

            v.addStretch()

            # Bouton refresh
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
        """Rafraîchit les 4 cartes."""
        from Database import system_status

        # ─── Disque ───
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

        # ─── Réseau ───
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

        # ─── DB ───
        db_st = system_status.get_db_status()
        if db_st:
            lines = [f"📁 {db_st['path']}",
                     f"📊 Taille : {db_st['size_mb']} Mo"]
            for t, n in db_st["tables"].items():
                if n > 0:
                    lines.append(f"  • {t:<20} : {n:>8,}".replace(",", " "))
            self._lbl_db.setText("\n".join(lines))

        # ─── Logs ───
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
        """Met à jour l'affichage du mode serveur (avec icônes, sans emoji)."""
        try:
            mode = db.get_config("server_mode", "autonome") or "autonome"
            host = db.get_config("server_host", "127.0.0.1") or "127.0.0.1"
            port = int(db.get_config("server_port", 5001) or 5001)

            if mode == "client":
                self._lbl_server_mode.setText("Client")
                self._lbl_server_mode.setStyleSheet(
                    "font-size: 24px; font-weight: 800; color: #2563eb; "
                    "background: transparent; border: none; padding-top: 4px;")
                self._lbl_server_details.setText(
                    f"Serveur cible : {host}:{port}")
            elif mode == "serveur":
                self._lbl_server_mode.setText("Serveur principal")
                self._lbl_server_mode.setStyleSheet(
                    "font-size: 24px; font-weight: 800; color: #16a34a; "
                    "background: transparent; border: none; padding-top: 4px;")
                self._lbl_server_details.setText(
                    "Héberge les données. Démarrez le service avec : "
                    "python -m Server.run_server")
            else:
                self._lbl_server_mode.setText("Autonome")
                self._lbl_server_mode.setStyleSheet(
                    "font-size: 24px; font-weight: 800; color: #64748b; "
                    "background: transparent; border: none; padding-top: 4px;")
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
    # Imprimantes
    # ══════════════════════════════════════════════════════════════
    def _load_imprimantes(self):
        """Charge les 2 imprimantes (ticket + rapport)."""
        try:
            printers = printer_manager.list_printers()

            # ─── Combo TICKET ───
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

            # ─── Combo RAPPORT ───
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

            # ─── Checkboxes (DB, globales) ───
            self.chk_auto_print.setChecked(
                bool(db.get_config("printer_auto_print", False)))
            if hasattr(self, "chk_auto_print_report"):
                self.chk_auto_print_report.setChecked(
                    bool(db.get_config(
                        "printer_auto_print_report", False)))
            self.chk_auto_open_pdf.setChecked(
                bool(db.get_config("printer_auto_open", True)))

        except Exception:
            logger.exception("Erreur chargement imprimantes")

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

    def _load_securite(self):
        try:
            self.spin_pwd_min.setValue(
                int(db.get_config("pwd_min_length", 8)))
            self.spin_pwd_exp.setValue(
                int(db.get_config("pwd_expiration_days", 0)))
            self.chk_require_digit.setChecked(
                bool(db.get_config("pwd_require_digit", False)))
            self.chk_require_upper.setChecked(
                bool(db.get_config("pwd_require_upper", False)))
            self.chk_require_special.setChecked(
                bool(db.get_config("pwd_require_special", False)))

            # ─── Actions critiques ───
            self.chk_require_pwd_critical.setChecked(
                bool(db.get_config("require_password_critical", False)))
            self.chk_backup_urgence.setChecked(
                bool(db.get_config("backup_urgence_auto", True)))

            # Seuil d'alerte stock
            self.spin_seuil_stock.setValue(
                int(db.get_config("seuil_stock", 20)))

            # ─── Max postes (dans onglet Vente) ───
            if hasattr(self, "spin_max_postes"):
                self.spin_max_postes.setValue(
                    int(db.get_config("max_postes", 100)))

                # ─── SÉCURITÉ PC CLIENT ───
            if hasattr(self, "chk_allow_admin_client"):
                self.chk_allow_admin_client.setChecked(
                    bool(db.get_config("allow_admin_on_client", True)))

        except Exception:
            logger.exception("Erreur chargement sécurité")

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
            dest = os.path.join(LOGO_DIR, f"logo_{int(time.time())}{ext}")
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
            from Database import audit

            db_path = str(db.DB_PATH)
            db.get_conn().commit()
            shutil.copyfile(db_path, path)

            # ═══ AUDIT ═══
            try:
                import os as _os
                taille = _os.path.getsize(path) if _os.path.exists(path) else 0
                audit.log(
                    audit.ACTION_EXPORT_DATABASE,
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.user_name,
                    cible_type="database",
                    cible_id="full_export",
                    cible_nom=_os.path.basename(path),
                    details={
                        "chemin": path,
                        "taille_octets": taille,
                    })
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

        # ─── Vérification critique ───
        from Database import critical_actions
        if not critical_actions.require_password_and_backup(
                self, self.user_id, "Restauration base"):
            return

        rep = QtWidgets.QMessageBox.warning(
            self, "Confirmation double",
            f"<b>Remplacer la base actuelle ?</b><br><br>"
            f"Fichier : <code>{os.path.basename(path)}</code><br><br>"
            f"L'application va devoir redémarrer.<br>"
            f"Toutes les modifications non sauvegardées seront perdues."
            f"<br><br>Confirmer ?",
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

        # ─── Vérification critique ───
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
            from Database import audit

            # ═══ AUDIT AVANT RESET (important) ═══
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
                f"L'application va se fermer. Relancez-la pour "
                f"recommencer le wizard.")
            QtWidgets.QApplication.quit()
        except Exception as e:
            logger.exception("Erreur reset")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))

    # ══════════════════════════════════════════════════════════════
    # Recharger avec confirmation
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

    # ══════════════════════════════════════════════════════════════
    # Enregistrement
    # ══════════════════════════════════════════════════════════════
    def _on_save(self):
        if not self.is_owner and not self.is_developer:
            if self.role_readonly():
                QtWidgets.QMessageBox.warning(
                    self, "Accès refusé",
                    "Seul le propriétaire ou le développeur peut "
                    "modifier les paramètres.")
                return

        try:
            from Database import audit

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
                "sauvegarde_auto": db.get_config("sauvegarde_auto", False),
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

                # ─── Code caisse : VALIDATION (1-2 chiffres) ───
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

                # ─── Taux de change (sensible) ───
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

                mentions = [m.strip() for m in
                            self.edit_mentions.toPlainText().split("\n")
                            if m.strip()]
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

                # Dossier principal de backup
                dossier = self.edit_dossier_save.text().strip()
                db.set_config("backup_dir",
                              dossier or backup_engine.DEFAULT_BACKUP_DIR,
                              type_="str")

                # Backup secondaire (USB/NAS)
                db.set_config("backup_secondary_enabled",
                              self.chk_backup_secondary.isChecked(),
                              type_="bool")
                db.set_config("backup_secondary_dir",
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

                # ─── Sécurité actions critiques ───
                db.set_config("require_password_critical",
                              self.chk_require_pwd_critical.isChecked(),
                              type_="bool")
                db.set_config("backup_urgence_auto",
                              self.chk_backup_urgence.isChecked(),
                              type_="bool")

                # Seuil stock
                db.set_config("seuil_stock",
                              self.spin_seuil_stock.value(),
                              type_="int")

                # ─── SÉCURITÉ PC CLIENT ───
                if hasattr(self, "chk_allow_admin_client"):
                    db.set_config("allow_admin_on_client",
                                  self.chk_allow_admin_client.isChecked(),
                                  type_="bool")

                # ─── Impression : TICKET (QSettings per-machine) ───
                if hasattr(self, "combo_printer_ticket"):
                    name = self.combo_printer_ticket.currentText()
                    if name.startswith("("):
                        name = ""
                    printer_manager.set_ticket_printer(name)

                # ─── Impression : RAPPORT (QSettings per-machine) ───
                if hasattr(self, "combo_printer_report"):
                    name = self.combo_printer_report.currentText()
                    if name.startswith("("):
                        name = ""
                    printer_manager.set_report_printer(name)

                # ─── Auto-print (DB, globale) ───
                db.set_config("printer_auto_print",
                              self.chk_auto_print.isChecked(),
                              type_="bool")
                if hasattr(self, "chk_auto_print_report"):
                    db.set_config("printer_auto_print_report",
                                  self.chk_auto_print_report.isChecked(),
                                  type_="bool")
                db.set_config("printer_auto_open",
                              self.chk_auto_open_pdf.isChecked(),
                              type_="bool")

                # Audit
                audit.log("MODIF_CONFIG",
                          utilisateur_id=self.user_id,
                          utilisateur_name=self.user_name,
                          cible_type="configuration",
                          details={"source": "page_parametres"})

            # ═══ AUDIT CONFIG ═══
            try:
                apres_config = {
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
            QtWidgets.QMessageBox.warning(self, "Champ manquant", str(ve))
        except Exception as e:
            logger.exception("Erreur sauvegarde paramètres")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'enregistrer :\n{e}")

    def role_readonly(self):
        """Retourne True si l'utilisateur n'a pas le droit de modifier."""
        return not (self.is_owner or self.is_developer)

    # ══════════════════════════════════════════════════════════════
    # Dossiers de backup
    # ══════════════════════════════════════════════════════════════
    def _browse_backup_dir(self):
        """Choisit le dossier principal de backup."""
        from Database import backup_engine
        start = (self.edit_dossier_save.text().strip()
                 or backup_engine.DEFAULT_BACKUP_DIR)
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Dossier principal de sauvegarde", start)
        if folder:
            self.edit_dossier_save.setText(folder)

    def _browse_backup_secondary(self):
        """Choisit le dossier secondaire (USB/NAS)."""
        start = (self.edit_backup_secondary.text().strip()
                 or os.path.expanduser("~"))
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Dossier secondaire (USB / NAS / réseau)", start)
        if folder:
            self.edit_backup_secondary.setText(folder)

    def _on_manage_backups(self):
        """Ouvre le gestionnaire des archives de sauvegarde."""
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
        """Active/désactive le champ du dossier secondaire."""
        if hasattr(self, "edit_backup_secondary"):
            self.edit_backup_secondary.setEnabled(checked)
        if hasattr(self, "btn_browse_backup_secondary"):
            self.btn_browse_backup_secondary.setEnabled(checked)

# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    from Database import db, seed
    app = QtWidgets.QApplication(sys.argv)
    db.get_conn()
    seed.run()

    w = PageParametres(user_id="TEST", user_name="Test", is_owner=True)
    w.resize(1200, 800)
    w.show()
    sys.exit(app.exec())