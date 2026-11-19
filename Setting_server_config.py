#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_server_config.py — Configuration réseau (serveur / client).
====================================================================
Design Nova Pharma : cartes aérées, icônes SVG, zéro emoji.

v2.1 — Refonte UI : padding généreux, scroll, radios en cartes.
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
        self.setMinimumSize(760, 720)
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

            /* ═══ RESET global ═══ */
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

            /* ═══ SCROLL AREA ═══ */
            QDialog#ServerConfigDialog QScrollArea {
                background: transparent;
                border: none;
            }
            QDialog#ServerConfigDialog QScrollBar:vertical {
                background: transparent;
                width: 10px;
                margin: 4px 2px 4px 0;
            }
            QDialog#ServerConfigDialog QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 5px;
                min-height: 32px;
            }
            QDialog#ServerConfigDialog QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QDialog#ServerConfigDialog QScrollBar::add-line:vertical,
            QDialog#ServerConfigDialog QScrollBar::sub-line:vertical {
                height: 0;
            }
            QDialog#ServerConfigDialog QScrollBar::add-page:vertical,
            QDialog#ServerConfigDialog QScrollBar::sub-page:vertical {
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
                font-size: 21px;
                font-weight: 800;
                color: #ffffff;
            }
            QDialog#ServerConfigDialog QLabel#header_sub {
                font-size: 12px;
                color: rgba(255,255,255,0.88);
            }

            /* ═══ CORPS ═══ */
            QDialog#ServerConfigDialog QWidget#body {
                background: transparent;
            }

            /* ═══ CARTES ═══ */
            QDialog#ServerConfigDialog QFrame#card {
                background: #ffffff;
                border: 1px solid #e6ebf2;
                border-radius: 18px;
            }

            /* ═══ TITRES CARTES ═══ */
            QDialog#ServerConfigDialog QLabel#card_title {
                color: #0f172a;
                font-size: 15px;
                font-weight: 800;
                letter-spacing: 0.2px;
                border: none;
            }
            QDialog#ServerConfigDialog QLabel#card_sub {
                color: #64748b;
                font-size: 12px;
                line-height: 1.5;
                border: none;
            }

            /* ═══ LABELS DE CHAMPS ═══ */
            QDialog#ServerConfigDialog QLabel#field_label {
                color: #64748b;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1.1px;
                border: none;
                background: transparent;
            }

            /* ═══ ICÔNES PILL ═══ */
            QDialog#ServerConfigDialog QLabel#icon_pill_blue {
                background: #eff6ff;
                border: 1px solid #dbeafe;
                border-radius: 11px;
            }
            QDialog#ServerConfigDialog QLabel#icon_pill_orange {
                background: #fef3c7;
                border: 1px solid #fde68a;
                border-radius: 11px;
            }
            QDialog#ServerConfigDialog QLabel#icon_pill_green {
                background: #dcfce7;
                border: 1px solid #bbf7d0;
                border-radius: 11px;
            }

            /* ═══ CHAMPS ═══ */
            QDialog#ServerConfigDialog QLineEdit,
            QDialog#ServerConfigDialog QSpinBox,
            QDialog#ServerConfigDialog QTimeEdit {
                background: #ffffff;
                border: 1.5px solid #dbe3ec;
                border-radius: 10px;
                padding: 12px 16px;
                font-size: 13px;
                color: #0f172a;
                min-height: 44px;
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
                background: #ffffff;
            }

            /* ═══ RADIOS (cartes cliquables) ═══ */
            QDialog#ServerConfigDialog QRadioButton#mode_card {
                color: #334155;
                font-size: 13px;
                font-weight: 600;
                padding: 18px 20px;
                spacing: 14px;
                background: #ffffff;
                border: 2px solid #e6ebf2;
                border-radius: 14px;
            }
            QDialog#ServerConfigDialog QRadioButton#mode_card:hover {
                background: #f8fafc;
                border-color: #c3cedd;
            }
            QDialog#ServerConfigDialog QRadioButton#mode_card:checked {
                background: #eff6ff;
                border-color: #2563eb;
                color: #0f172a;
            }
            QDialog#ServerConfigDialog QRadioButton#mode_card::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #cbd5e1;
                background: #ffffff;
            }
            QDialog#ServerConfigDialog QRadioButton#mode_card::indicator:hover {
                border-color: #2563eb;
            }
            QDialog#ServerConfigDialog QRadioButton#mode_card::indicator:checked {
                background: #2563eb;
                border-color: #2563eb;
            }

            /* ═══ CHECKBOX ═══ */
            QDialog#ServerConfigDialog QCheckBox {
                color: #334155;
                font-size: 13px;
                font-weight: 600;
                padding: 8px 0;
                spacing: 12px;
                background: transparent;
                border: none;
            }
            QDialog#ServerConfigDialog QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #cbd5e1;
                border-radius: 6px;
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
                padding: 10px 22px;
                font-weight: 700;
                font-size: 13px;
                min-height: 48px;
            }
            QDialog#ServerConfigDialog QPushButton#btn_test:hover {
                background: #f8fafc;
                border-color: #c3cedd;
                color: #0f172a;
            }
            QDialog#ServerConfigDialog QPushButton#btn_test:pressed {
                background: #eff6ff;
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
                border-radius: 11px;
                padding: 12px 28px;
                font-weight: 700;
                font-size: 13px;
                min-height: 50px;
                min-width: 130px;
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
                border-radius: 11px;
                padding: 12px 32px;
                font-weight: 800;
                font-size: 13px;
                min-height: 50px;
                min-width: 170px;
            }
            QDialog#ServerConfigDialog QPushButton#btn_save:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
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
        header.setMinimumHeight(110)
        header.setMaximumHeight(110)

        h = QtWidgets.QHBoxLayout(header)
        h.setContentsMargins(28, 20, 28, 20)
        h.setSpacing(18)

        ico = QtWidgets.QLabel()
        ico.setObjectName("header_ico")
        ico.setFixedSize(60, 60)
        ico.setAlignment(Qt.AlignCenter)
        pix = QtGui.QPixmap(":/Icon/Icons/server_white.svg")
        if not pix.isNull():
            ico.setPixmap(pix.scaled(
                30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(ico)

        titles = QtWidgets.QVBoxLayout()
        titles.setSpacing(3)

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
        # CORPS (avec scroll)
        # ═══════════════════════════════════════════════════════════
        body = QtWidgets.QWidget()
        body.setObjectName("body")

        # ─── Scroll ───
        scroll = QtWidgets.QScrollArea(body)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        inner = QtWidgets.QWidget()
        inner.setStyleSheet("background: transparent;")
        v_inner = QtWidgets.QVBoxLayout(inner)
        v_inner.setContentsMargins(28, 24, 28, 24)
        v_inner.setSpacing(18)

        # ─── Wrapper centré max 760px ───
        wrapper = QtWidgets.QHBoxLayout()
        wrapper.setContentsMargins(0, 0, 0, 0)
        wrapper.addStretch()

        container = QtWidgets.QWidget()
        container.setMaximumWidth(760)
        container.setStyleSheet("background: transparent;")
        v_container = QtWidgets.QVBoxLayout(container)
        v_container.setContentsMargins(0, 0, 0, 0)
        v_container.setSpacing(18)

        # ─── Cartes ───
        v_container.addWidget(self._make_role_card())

        self.card2 = self._make_connexion_card()
        v_container.addWidget(self.card2)

        v_container.addWidget(self._make_horaires_card())
        v_container.addStretch()

        wrapper.addWidget(container)
        wrapper.addStretch()

        v_inner.addLayout(wrapper)
        scroll.setWidget(inner)

        v_body = QtWidgets.QVBoxLayout(body)
        v_body.setContentsMargins(0, 0, 0, 0)
        v_body.setSpacing(0)
        v_body.addWidget(scroll)

        root.addWidget(body, 1)

        # ═══════════════════════════════════════════════════════════
        # FOOTER
        # ═══════════════════════════════════════════════════════════
        footer = QtWidgets.QFrame()
        footer.setObjectName("footer")
        footer.setMinimumHeight(82)
        hf = QtWidgets.QHBoxLayout(footer)
        hf.setContentsMargins(28, 18, 28, 18)
        hf.setSpacing(14)
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
            btn_save.setIconSize(QtCore.QSize(18, 18))
        btn_save.clicked.connect(self._on_save)
        hf.addWidget(btn_save)

        root.addWidget(footer)

        self.radio_client.toggled.connect(self._on_mode_changed)

    # ══════════════════════════════════════════════════════════════
    # CARTE 1 — Rôle du poste (radios en cartes)
    # ══════════════════════════════════════════════════════════════
    def _make_role_card(self) -> QtWidgets.QFrame:
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(28, 24, 28, 24)
        v.setSpacing(16)

        # ─── Header carte ───
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(12)

        ico = QtWidgets.QLabel()
        ico.setObjectName("icon_pill_blue")
        ico.setFixedSize(38, 38)
        ico.setAlignment(Qt.AlignCenter)
        pix = QtGui.QPixmap(":/Icon/Icons/server.svg")
        if not pix.isNull():
            ico.setPixmap(pix.scaled(
                20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(ico)

        v_head = QtWidgets.QVBoxLayout()
        v_head.setSpacing(2)

        title = QtWidgets.QLabel("Rôle de ce poste")
        title.setObjectName("card_title")
        v_head.addWidget(title)

        sub = QtWidgets.QLabel(
            "Choisissez comment ce poste participe au réseau.")
        sub.setObjectName("card_sub")
        sub.setWordWrap(True)
        v_head.addWidget(sub)

        h.addLayout(v_head, 1)
        v.addLayout(h)

        # ─── Radio 1 : Serveur (carte cliquable) ───
        self.radio_serveur = QtWidgets.QRadioButton(
            "Serveur principal  —  héberge la base et l'API pour les "
            "autres postes")
        self.radio_serveur.setObjectName("mode_card")
        self.radio_serveur.setCursor(Qt.PointingHandCursor)
        v.addWidget(self.radio_serveur)

        # ─── Radio 2 : Client (carte cliquable) ───
        self.radio_client = QtWidgets.QRadioButton(
            "Client  —  se connecte à un serveur distant en réseau")
        self.radio_client.setObjectName("mode_card")
        self.radio_client.setCursor(Qt.PointingHandCursor)
        v.addWidget(self.radio_client)

        return card

    # ══════════════════════════════════════════════════════════════
    # CARTE 2 — Connexion au serveur
    # ══════════════════════════════════════════════════════════════
    def _make_connexion_card(self) -> QtWidgets.QFrame:
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(28, 24, 28, 24)
        v.setSpacing(16)

        # ─── Header ───
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(12)

        ico = QtWidgets.QLabel()
        ico.setObjectName("icon_pill_orange")
        ico.setFixedSize(38, 38)
        ico.setAlignment(Qt.AlignCenter)
        pix = QtGui.QPixmap(":/Icon/Icons/globe.svg")
        if not pix.isNull():
            ico.setPixmap(pix.scaled(
                20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(ico)

        v_head = QtWidgets.QVBoxLayout()
        v_head.setSpacing(2)

        title = QtWidgets.QLabel("Connexion au serveur distant")
        title.setObjectName("card_title")
        v_head.addWidget(title)

        sub = QtWidgets.QLabel(
            "Adresse IP et port du serveur principal à joindre.")
        sub.setObjectName("card_sub")
        sub.setWordWrap(True)
        v_head.addWidget(sub)

        h.addLayout(v_head, 1)
        v.addLayout(h)

        # ─── Form ───
        form = QtWidgets.QFormLayout()
        form.setSpacing(16)
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

        # ─── Test + statut ───
        h_test = QtWidgets.QHBoxLayout()
        h_test.setSpacing(14)

        self.btn_test = QtWidgets.QPushButton("  Tester la connexion")
        self.btn_test.setObjectName("btn_test")
        self.btn_test.setCursor(Qt.PointingHandCursor)
        icon_wifi = QtGui.QIcon(":/Icon/Icons/wifi.svg")
        if not icon_wifi.isNull():
            self.btn_test.setIcon(icon_wifi)
            self.btn_test.setIconSize(QtCore.QSize(18, 18))
        self.btn_test.clicked.connect(self._on_test)
        h_test.addWidget(self.btn_test)

        h_test.addStretch()

        self.lbl_test = QtWidgets.QLabel("")
        self.lbl_test.setStyleSheet(
            "font-size: 12px; font-weight: 700; "
            "background: transparent; border: none;")
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
        v.setContentsMargins(28, 24, 28, 24)
        v.setSpacing(16)

        # ─── Header ───
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(12)

        ico = QtWidgets.QLabel()
        ico.setObjectName("icon_pill_green")
        ico.setFixedSize(38, 38)
        ico.setAlignment(Qt.AlignCenter)
        pix = QtGui.QPixmap(":/Icon/Icons/clock.svg")
        if not pix.isNull():
            ico.setPixmap(pix.scaled(
                20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(ico)

        v_head = QtWidgets.QVBoxLayout()
        v_head.setSpacing(2)

        title = QtWidgets.QLabel("Plage horaire d'ouverture")
        title.setObjectName("card_title")
        v_head.addWidget(title)

        sub = QtWidgets.QLabel(
            "En dehors de ces horaires, le serveur refuse toute "
            "requête (sauf le ping de santé).")
        sub.setObjectName("card_sub")
        sub.setWordWrap(True)
        v_head.addWidget(sub)

        h.addLayout(v_head, 1)
        v.addLayout(h)

        # ─── Checkbox ───
        self.chk_horaires = QtWidgets.QCheckBox(
            "Activer la plage horaire")
        self.chk_horaires.setCursor(Qt.PointingHandCursor)
        v.addWidget(self.chk_horaires)

        # ─── Form horaires ───
        form = QtWidgets.QFormLayout()
        form.setSpacing(16)
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
        """Carte connexion toujours visible (IP/Port modifiables)."""
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
            f"color: {color}; font-size: 12px; font-weight: 700; "
            f"background: transparent; border: none;")

    # ══════════════════════════════════════════════════════════════
    def _on_save(self):
        """Sauvegarde avec double confirmation."""
        try:
            new_mode = "client" if self.radio_client.isChecked() else "serveur"
            new_host = self.edit_host.text().strip()
            new_port = self.edit_port.value()

            old_mode = db.get_config("server_mode", "autonome") or "autonome"
            old_host = db.get_config("server_host", "127.0.0.1") or "127.0.0.1"
            old_port = int(db.get_config("server_port", 5001) or 5001)

            if (new_mode == old_mode
                    and new_host == old_host
                    and new_port == old_port):
                QtWidgets.QMessageBox.information(
                    self, "Aucun changement",
                    "La configuration n'a pas été modifiée.")
                return

            if new_mode == "client" and not new_host:
                QtWidgets.QMessageBox.warning(
                    self, "IP manquante",
                    "L'adresse IP est obligatoire en mode client.")
                return

            # ─── Confirmation 1 ───
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
                self, "Confirmation", msg,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if rep != QtWidgets.QMessageBox.Yes:
                return

            # ─── Confirmation 2 ───
            text, ok = QtWidgets.QInputDialog.getText(
                self, "Confirmation finale",
                "Tapez CONFIRMER pour valider le changement :",
                QtWidgets.QLineEdit.Normal, "")
            if not ok or text.strip().upper() != "CONFIRMER":
                QtWidgets.QMessageBox.information(
                    self, "Annulé", "Modification annulée.")
                return

            # ─── Sauvegarde ───
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