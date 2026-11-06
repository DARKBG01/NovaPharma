#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_server_config.py — Configuration réseau (serveur / client).
====================================================================
Design Nova Pharma : cartes, icônes SVG, zéro emoji, zéro bordure parasite.
"""

import logging

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import db
from Client import client_api

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
class ServerConfigDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ServerConfigDialog")
        self.setWindowTitle("Configuration réseau — Nova Pharma")
        self.setMinimumSize(700, 680)
        self.setModal(True)

        self._build_ui()
        self._load()

    # ══════════════════════════════════════════════════════════════
    def _build_ui(self):
        self.setStyleSheet("""
            /* ═══ RACINE ═══ */
            QDialog#ServerConfigDialog {
                background: #f0f4f8;
            }

            /* ═══ RESET global : annule l'héritage du MainWindow ═══ */
            QDialog#ServerConfigDialog QLabel {
                background: transparent;
                border: none;
                padding: 0px;
                color: #0f172a;
            }
            QDialog#ServerConfigDialog QFrame {
                border: none;
                background: transparent;
            }

            /* ═══ HEADER ═══ */
            QDialog#ServerConfigDialog QFrame#header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1d4ed8, stop:1 #4f46e5);
                border: none;
            }
            QDialog#ServerConfigDialog QFrame#header QLabel {
                color: #ffffff;
                border: none;
                background: transparent;
            }
            QDialog#ServerConfigDialog QLabel#header_ico {
                background: rgba(255,255,255,0.15);
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 14px;
            }
            QDialog#ServerConfigDialog QLabel#header_title {
                font-size: 20px;
                font-weight: 800;
                color: #ffffff;
            }
            QDialog#ServerConfigDialog QLabel#header_sub {
                font-size: 11px;
                color: rgba(255,255,255,0.85);
            }

            /* ═══ CORPS ═══ */
            QDialog#ServerConfigDialog QWidget#body {
                background: transparent;
            }

            /* ═══ CARTES ═══ */
            QDialog#ServerConfigDialog QFrame#card {
                background: #ffffff;
                border: 1px solid #e6ebf2;
                border-radius: 16px;
            }

            /* ═══ TITRES CARTES ═══ */
            QDialog#ServerConfigDialog QLabel#card_title {
                color: #0f172a;
                font-size: 13px;
                font-weight: 800;
                letter-spacing: 0.3px;
                border: none;
            }
            QDialog#ServerConfigDialog QLabel#card_sub {
                color: #64748b;
                font-size: 11px;
                border: none;
            }

            /* ═══ LABELS DE CHAMPS ═══ */
            QDialog#ServerConfigDialog QLabel#field_label {
                color: #64748b;
                font-size: 10px;
                font-weight: 800;
                letter-spacing: 1px;
                border: none;
                background: transparent;
            }

            /* ═══ ICÔNES PILL ═══ */
            QDialog#ServerConfigDialog QLabel#icon_pill_blue {
                background: #eff6ff;
                border: 1px solid #dbeafe;
                border-radius: 10px;
            }
            QDialog#ServerConfigDialog QLabel#icon_pill_orange {
                background: #fef3c7;
                border: 1px solid #fde68a;
                border-radius: 10px;
            }
            QDialog#ServerConfigDialog QLabel#icon_pill_green {
                background: #dcfce7;
                border: 1px solid #bbf7d0;
                border-radius: 10px;
            }

            /* ═══ CHAMPS ═══ */
            QDialog#ServerConfigDialog QLineEdit,
            QDialog#ServerConfigDialog QSpinBox,
            QDialog#ServerConfigDialog QTimeEdit {
                background: #ffffff;
                border: 1.5px solid #dbe3ec;
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 12px;
                color: #0f172a;
                min-height: 22px;
            }
            QDialog#ServerConfigDialog QLineEdit:hover,
            QDialog#ServerConfigDialog QSpinBox:hover,
            QDialog#ServerConfigDialog QTimeEdit:hover {
                border-color: #b9c6d8;
            }
            QDialog#ServerConfigDialog QLineEdit:focus,
            QDialog#ServerConfigDialog QSpinBox:focus,
            QDialog#ServerConfigDialog QTimeEdit:focus {
                border-color: #2563eb;
            }

            /* ═══ RADIOS ═══ */
            QDialog#ServerConfigDialog QRadioButton {
                color: #334155;
                font-size: 12px;
                font-weight: 600;
                padding: 10px 4px;
                spacing: 10px;
                background: transparent;
                border: none;
            }
            QDialog#ServerConfigDialog QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #cbd5e1;
                background: #ffffff;
            }
            QDialog#ServerConfigDialog QRadioButton::indicator:hover {
                border-color: #2563eb;
            }
            QDialog#ServerConfigDialog QRadioButton::indicator:checked {
                background: #2563eb;
                border-color: #2563eb;
            }

            /* ═══ CHECKBOX ═══ */
            QDialog#ServerConfigDialog QCheckBox {
                color: #334155;
                font-size: 12px;
                font-weight: 600;
                padding: 6px 0;
                spacing: 10px;
                background: transparent;
                border: none;
            }
            QDialog#ServerConfigDialog QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #cbd5e1;
                border-radius: 5px;
                background: #ffffff;
            }
            QDialog#ServerConfigDialog QCheckBox::indicator:hover {
                border-color: #2563eb;
            }
            QDialog#ServerConfigDialog QCheckBox::indicator:checked {
                background: #2563eb;
                border-color: #2563eb;
            }

            /* ═══ BOUTON TEST ═══ */
            QDialog#ServerConfigDialog QPushButton#btn_test {
                background: #ffffff;
                color: #475569;
                border: 1.5px solid #dbe3ec;
                border-radius: 10px;
                padding: 8px 18px;
                font-weight: 700;
                font-size: 12px;
                min-height: 38px;
            }
            QDialog#ServerConfigDialog QPushButton#btn_test:hover {
                background: #f8fafc;
                border-color: #c3cedd;
                color: #0f172a;
            }

            /* ═══ FOOTER ═══ */
            QDialog#ServerConfigDialog QFrame#footer {
                background: #ffffff;
                border: none;
                border-top: 1px solid #e6ebf2;
            }
            QDialog#ServerConfigDialog QPushButton#btn_cancel {
                background: #ffffff;
                color: #475569;
                border: 1.5px solid #dbe3ec;
                border-radius: 10px;
                padding: 10px 24px;
                font-weight: 700;
                font-size: 12px;
                min-height: 42px;
                min-width: 120px;
            }
            QDialog#ServerConfigDialog QPushButton#btn_cancel:hover {
                background: #f8fafc;
                border-color: #c3cedd;
            }
            QDialog#ServerConfigDialog QPushButton#btn_save {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: #ffffff;
                border: 1px solid #1d4ed8;
                border-radius: 10px;
                padding: 10px 24px;
                font-weight: 800;
                font-size: 12px;
                min-height: 42px;
                min-width: 150px;
            }
            QDialog#ServerConfigDialog QPushButton#btn_save:hover {
                background: #1d4ed8;
            }
            QDialog#ServerConfigDialog QPushButton#btn_save:pressed {
                background: #1e40af;
            }
        """)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ═══════════════════════════════════════════════════════════
        # HEADER
        # ═══════════════════════════════════════════════════════════
        header = QtWidgets.QFrame()
        header.setObjectName("header")
        header.setMinimumHeight(100)
        header.setMaximumHeight(100)

        h = QtWidgets.QHBoxLayout(header)
        h.setContentsMargins(24, 16, 24, 16)
        h.setSpacing(16)

        # Icône serveur
        ico = QtWidgets.QLabel()
        ico.setObjectName("header_ico")
        ico.setFixedSize(56, 56)
        ico.setAlignment(Qt.AlignCenter)
        pix = QtGui.QPixmap(":/Icon/Icons/server_white.svg")
        if not pix.isNull():
            ico.setPixmap(pix.scaled(
                28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(ico)

        # Titres
        titles = QtWidgets.QVBoxLayout()
        titles.setSpacing(2)

        t1 = QtWidgets.QLabel("Configuration réseau")
        t1.setObjectName("header_title")
        titles.addWidget(t1)

        t2 = QtWidgets.QLabel(
            "Définissez le rôle de ce poste dans le réseau")
        t2.setObjectName("header_sub")
        titles.addWidget(t2)

        h.addLayout(titles)
        h.addStretch()

        root.addWidget(header)

        # ═══════════════════════════════════════════════════════════
        # CORPS
        # ═══════════════════════════════════════════════════════════
        body = QtWidgets.QWidget()
        body.setObjectName("body")
        v = QtWidgets.QVBoxLayout(body)
        v.setContentsMargins(24, 20, 24, 20)
        v.setSpacing(14)

        # ─── CARTE 1 : Rôle du poste ───
        v.addWidget(self._make_role_card())

        # ─── CARTE 2 : Connexion serveur (masquée si serveur local) ───
        self.card2 = self._make_connexion_card()
        v.addWidget(self.card2)

        # ─── CARTE 3 : Plage horaire ───
        v.addWidget(self._make_horaires_card())

        v.addStretch()

        root.addWidget(body, 1)

        # ═══════════════════════════════════════════════════════════
        # FOOTER
        # ═══════════════════════════════════════════════════════════
        footer = QtWidgets.QFrame()
        footer.setObjectName("footer")
        footer.setMinimumHeight(70)
        hf = QtWidgets.QHBoxLayout(footer)
        hf.setContentsMargins(24, 14, 24, 14)
        hf.setSpacing(12)
        hf.addStretch()

        btn_cancel = QtWidgets.QPushButton("Annuler")
        btn_cancel.setObjectName("btn_cancel")
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.clicked.connect(self.reject)
        hf.addWidget(btn_cancel)

        btn_save = QtWidgets.QPushButton("  Enregistrer")
        btn_save.setObjectName("btn_save")
        btn_save.setCursor(Qt.PointingHandCursor)
        icon_save = QtGui.QIcon(":/Icon/Icons/save_white.svg")
        if not icon_save.isNull():
            btn_save.setIcon(icon_save)
            btn_save.setIconSize(QtCore.QSize(16, 16))
        btn_save.clicked.connect(self._on_save)
        hf.addWidget(btn_save)

        root.addWidget(footer)

        # Toggle visibilité carte 2
        self.radio_client.toggled.connect(self._on_mode_changed)

    # ══════════════════════════════════════════════════════════════
    # CARTE 1 — Rôle du poste
    # ══════════════════════════════════════════════════════════════
    def _make_role_card(self) -> QtWidgets.QFrame:
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(20, 16, 20, 16)
        v.setSpacing(10)

        # Header
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(10)

        ico = QtWidgets.QLabel()
        ico.setObjectName("icon_pill_blue")
        ico.setFixedSize(32, 32)
        ico.setAlignment(Qt.AlignCenter)
        pix = QtGui.QPixmap(":/Icon/Icons/server.svg")
        if not pix.isNull():
            ico.setPixmap(pix.scaled(
                18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(ico)

        title = QtWidgets.QLabel("Rôle de ce poste")
        title.setObjectName("card_title")
        h.addWidget(title)
        h.addStretch()

        v.addLayout(h)

        # Radios
        self.radio_serveur = QtWidgets.QRadioButton(
            "Serveur principal  —  héberge la base et l'API pour les "
            "autres postes")
        self.radio_client = QtWidgets.QRadioButton(
            "Client  —  se connecte à un serveur distant en réseau")
        v.addWidget(self.radio_serveur)
        v.addWidget(self.radio_client)

        return card

    # ══════════════════════════════════════════════════════════════
    # CARTE 2 — Connexion au serveur
    # ══════════════════════════════════════════════════════════════
    def _make_connexion_card(self) -> QtWidgets.QFrame:
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(20, 16, 20, 16)
        v.setSpacing(12)

        # Header
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(10)

        ico = QtWidgets.QLabel()
        ico.setObjectName("icon_pill_orange")
        ico.setFixedSize(32, 32)
        ico.setAlignment(Qt.AlignCenter)
        pix = QtGui.QPixmap(":/Icon/Icons/globe.svg")
        if not pix.isNull():
            ico.setPixmap(pix.scaled(
                18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(ico)

        title = QtWidgets.QLabel("Connexion au serveur distant")
        title.setObjectName("card_title")
        h.addWidget(title)
        h.addStretch()

        v.addLayout(h)

        # Champs
        form = QtWidgets.QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        form.setFieldGrowthPolicy(
            QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

        lbl_host = QtWidgets.QLabel("IP DU SERVEUR")
        lbl_host.setObjectName("field_label")
        self.edit_host = QtWidgets.QLineEdit()
        self.edit_host.setPlaceholderText("Ex : 192.168.1.15")
        form.addRow(lbl_host, self.edit_host)

        lbl_port = QtWidgets.QLabel("PORT")
        lbl_port.setObjectName("field_label")
        self.edit_port = QtWidgets.QSpinBox()
        self.edit_port.setRange(1, 65535)
        self.edit_port.setValue(5001)
        form.addRow(lbl_port, self.edit_port)

        v.addLayout(form)

        # Bouton tester + statut
        h_test = QtWidgets.QHBoxLayout()
        h_test.setSpacing(10)

        self.btn_test = QtWidgets.QPushButton("  Tester la connexion")
        self.btn_test.setObjectName("btn_test")
        self.btn_test.setCursor(Qt.PointingHandCursor)
        icon_wifi = QtGui.QIcon(":/Icon/Icons/wifi.svg")
        if not icon_wifi.isNull():
            self.btn_test.setIcon(icon_wifi)
            self.btn_test.setIconSize(QtCore.QSize(16, 16))
        self.btn_test.clicked.connect(self._on_test)
        h_test.addWidget(self.btn_test)

        h_test.addStretch()

        self.lbl_test = QtWidgets.QLabel("")
        self.lbl_test.setStyleSheet(
            "font-size: 11px; font-weight: 700; background: transparent; "
            "border: none;")
        h_test.addWidget(self.lbl_test)

        v.addLayout(h_test)

        return card

    # ══════════════════════════════════════════════════════════════
    # CARTE 3 — Plage horaire
    # ══════════════════════════════════════════════════════════════
    def _make_horaires_card(self) -> QtWidgets.QFrame:
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(20, 16, 20, 16)
        v.setSpacing(10)

        # Header
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(10)

        ico = QtWidgets.QLabel()
        ico.setObjectName("icon_pill_green")
        ico.setFixedSize(32, 32)
        ico.setAlignment(Qt.AlignCenter)
        pix = QtGui.QPixmap(":/Icon/Icons/clock.svg")
        if not pix.isNull():
            ico.setPixmap(pix.scaled(
                18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(ico)

        title = QtWidgets.QLabel("Plage horaire d'ouverture")
        title.setObjectName("card_title")
        h.addWidget(title)
        h.addStretch()

        v.addLayout(h)

        sub = QtWidgets.QLabel(
            "En dehors de ces horaires, le serveur refuse toute "
            "requête (sauf le ping de santé).")
        sub.setObjectName("card_sub")
        sub.setWordWrap(True)
        v.addWidget(sub)

        self.chk_horaires = QtWidgets.QCheckBox(
            "Activer la plage horaire")
        v.addWidget(self.chk_horaires)

        form = QtWidgets.QFormLayout()
        form.setSpacing(10)
        form.setFieldGrowthPolicy(
            QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

        lbl_deb = QtWidgets.QLabel("OUVERTURE")
        lbl_deb.setObjectName("field_label")
        self.edit_h_debut = QtWidgets.QTimeEdit()
        self.edit_h_debut.setDisplayFormat("HH:mm")
        form.addRow(lbl_deb, self.edit_h_debut)

        lbl_fin = QtWidgets.QLabel("FERMETURE")
        lbl_fin.setObjectName("field_label")
        self.edit_h_fin = QtWidgets.QTimeEdit()
        self.edit_h_fin.setDisplayFormat("HH:mm")
        form.addRow(lbl_fin, self.edit_h_fin)

        v.addLayout(form)

        return card

    # ══════════════════════════════════════════════════════════════
    def _on_mode_changed(self):
        """Affiche TOUJOURS la carte de connexion (IP/Port modifiables à tout moment)."""
        self.card2.setVisible(True)

    # ══════════════════════════════════════════════════════════════
    def _load(self):
        try:
            mode = db.get_config("server_mode", "autonome")
            if mode == "client":
                self.radio_client.setChecked(True)
            else:
                self.radio_serveur.setChecked(True)

            self.edit_host.setText(
                db.get_config("server_host", "127.0.0.1") or "")
            self.edit_port.setValue(
                int(db.get_config("server_port", 5001) or 5001))

            self.chk_horaires.setChecked(
                bool(db.get_config("server_horaires_actif", False)))

            h_deb = db.get_config("server_horaires_debut", "07:00")
            h_fin = db.get_config("server_horaires_fin", "22:00")
            try:
                hh, mm = h_deb.split(":")
                self.edit_h_debut.setTime(QtCore.QTime(int(hh), int(mm)))
            except Exception:
                self.edit_h_debut.setTime(QtCore.QTime(7, 0))
            try:
                hh, mm = h_fin.split(":")
                self.edit_h_fin.setTime(QtCore.QTime(int(hh), int(mm)))
            except Exception:
                self.edit_h_fin.setTime(QtCore.QTime(22, 0))

            self._on_mode_changed()
        except Exception:
            logger.exception("Erreur chargement config serveur")

    # ══════════════════════════════════════════════════════════════
    def _on_test(self):
        host = self.edit_host.text().strip()
        port = self.edit_port.value()
        if not host:
            self._set_status("IP manquante", "#dc2626")
            return

        self._set_status("Test en cours…", "#64748b")
        QtWidgets.QApplication.processEvents()

        try:
            api = client_api.NovaApiClient(f"http://{host}:{port}")
            info = api.sante()
            self._set_status(
                f"Connecté — version {info.get('version', '?')}",
                "#16a34a")
        except Exception as e:
            self._set_status(f"Échec : {e}", "#dc2626")

    def _set_status(self, msg, color):
        self.lbl_test.setText(f"●  {msg}")
        self.lbl_test.setStyleSheet(
            f"color: {color}; font-size: 11px; font-weight: 700; "
            f"background: transparent; border: none;")

    # ══════════════════════════════════════════════════════════════
    def _on_save(self):
        """Sauvegarde avec double confirmation."""
        try:
            # ─── Valeurs à enregistrer ───
            new_mode = "client" if self.radio_client.isChecked() else "serveur"
            new_host = self.edit_host.text().strip()
            new_port = self.edit_port.value()

            # ─── Valeurs actuelles ───
            old_mode = db.get_config("server_mode", "autonome") or "autonome"
            old_host = db.get_config("server_host", "127.0.0.1") or "127.0.0.1"
            old_port = int(db.get_config("server_port", 5001) or 5001)

            # ─── Aucun changement ───
            if (new_mode == old_mode
                    and new_host == old_host
                    and new_port == old_port):
                QtWidgets.QMessageBox.information(
                    self, "Aucun changement",
                    "La configuration n'a pas été modifiée.")
                return

            # ─── Validation ───
            if new_mode == "client" and not new_host:
                QtWidgets.QMessageBox.warning(
                    self, "IP manquante",
                    "L'adresse IP est obligatoire en mode client.")
                return

            # ═══════════════════════════════════════════════════════════
            # CONFIRMATION 1 — Avertissement
            # ═══════════════════════════════════════════════════════════
            msg = (
                "<b>⚠️  Modifier la configuration réseau ?</b><br><br>"
                f"<b>Mode</b> : {old_mode} → <b>{new_mode}</b><br>"
                f"<b>IP</b> : {old_host} → <b>{new_host}</b><br>"
                f"<b>Port</b> : {old_port} → <b>{new_port}</b><br><br>"
                "<b style='color:#dc2626;'>Conséquences :</b><br>"
                "• L'application devra être <b>redémarrée</b><br>"
                "• Les sessions en cours seront perdues<br>"
                "• Vérifiez que le serveur est joignable<br><br>"
                "Continuer ?"
            )
            rep = QtWidgets.QMessageBox.warning(
                self, "Confirmation",
                msg,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if rep != QtWidgets.QMessageBox.Yes:
                return

            # ═══════════════════════════════════════════════════════════
            # CONFIRMATION 2 — Saisie manuelle
            # ═══════════════════════════════════════════════════════════
            text, ok = QtWidgets.QInputDialog.getText(
                self, "Confirmation finale",
                "Tapez CONFIRMER pour valider le changement :",
                QtWidgets.QLineEdit.Normal, "")
            if not ok or text.strip().upper() != "CONFIRMER":
                QtWidgets.QMessageBox.information(
                    self, "Annulé", "Modification annulée.")
                return

            # ═══════════════════════════════════════════════════════════
            # SAUVEGARDE
            # ═══════════════════════════════════════════════════════════
            with db.transaction():
                db.set_config("server_mode", new_mode, type_="str")
                db.set_config("server_host", new_host, type_="str")
                db.set_config("server_port", new_port, type_="int")
                db.set_config("server_horaires_actif",
                              self.chk_horaires.isChecked(), type_="bool")
                db.set_config("server_horaires_debut",
                              self.edit_h_debut.time().toString("HH:mm"),
                              type_="str")
                db.set_config("server_horaires_fin",
                              self.edit_h_fin.time().toString("HH:mm"),
                              type_="str")

            # ─── Audit ───
            try:
                from Database import audit
                audit.log(
                    "MODIF_CONFIG_RESEAU",
                    utilisateur_id=getattr(self, "user_id", None),
                    cible_type="Configuration",
                    cible_id="reseau",
                    cible_nom="Configuration réseau",
                    details={
                        "old_mode": old_mode, "new_mode": new_mode,
                        "old_host": old_host, "new_host": new_host,
                        "old_port": old_port, "new_port": new_port,
                    },
                    severite="warning")
            except Exception:
                logger.exception("Erreur audit config réseau")

            logger.info(
                "Config réseau : %s → %s | %s:%d → %s:%d",
                old_mode, new_mode, old_host, old_port, new_host, new_port)

            # ═══════════════════════════════════════════════════════════
            # PROPOSE REDÉMARRAGE
            # ═══════════════════════════════════════════════════════════
            rep2 = QtWidgets.QMessageBox.question(
                self, "Configuration enregistrée ✅",
                "<b>Configuration sauvegardée.</b><br><br>"
                "L'application doit être redémarrée pour "
                "appliquer ces changements.<br><br>"
                "Redémarrer maintenant ?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.Yes)

            if rep2 == QtWidgets.QMessageBox.Yes:
                self._restart_application()
            else:
                self.accept()

        except Exception as e:
            logger.exception("Erreur sauvegarde config serveur")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))

    def _restart_application(self):
        """Ferme et relance l'application."""
        import sys
        import os
        try:
            logger.info("Redémarrage de l'application…")
            QtWidgets.QApplication.quit()
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception:
            logger.exception("Erreur redémarrage")
            QtWidgets.QMessageBox.critical(
                self, "Redémarrage manuel requis",
                "Fermez et relancez l'application manuellement.")
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    from Database import db, seed
    app = QtWidgets.QApplication(sys.argv)
    db.get_conn()
    seed.run()
    dlg = ServerConfigDialog()
    sys.exit(dlg.exec())