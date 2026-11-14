#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
license_dialog.py — Dialogue d'activation de licence.
"""

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import machine_id
from Core.license_manager import save_license, _verify_license


class LicenseDialog(QtWidgets.QDialog):
    """Dialogue pour saisir la clé de licence."""

    def __init__(self, message: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nova Pharma — Activation")
        self.setModal(True)
        self.setFixedSize(640, 820)
        self._build_ui(message)

    def _build_ui(self, message: str):
        self.setStyleSheet("""
            QDialog { background: #f0f4f8; }
            QLabel { background: transparent; color: #334155; }
            QLabel#title {
                color: #023E8A; font-size: 20px; font-weight: 800;
            }
            QLabel#sub { color: #64748b; font-size: 12px; }
            QLabel#error {
                background: #fef2f2; color: #b91c1c;
                border: 1px solid #fecaca; border-radius: 8px;
                padding: 10px 14px; font-size: 11px; font-weight: 600;
            }
            QFrame#card {
                background: #ffffff; border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QLineEdit {
                background: #f8fafc; border: 1.5px solid #dbe3ec;
                border-radius: 10px; padding: 10px 14px;
                color: #0f172a; font-size: 13px;
            }
            QLineEdit:focus { border-color: #0077B6; }
            QLineEdit#mid_input {
                background: #f1f5f9; border: 1px solid #cbd5e1;
                font-family: 'Courier New'; font-size: 11px;
                color: #64748b;
            }
            QPushButton {
                background: #0077B6; color: white; border: none;
                border-radius: 10px; padding: 10px 24px;
                font-weight: 700; font-size: 13px; min-height: 20px;
            }
            QPushButton:hover { background: #023E8A; }
            QPushButton#btn_cancel {
                background: transparent; color: #64748b;
                border: 1.5px solid #e2e8f0;
            }
            QPushButton#btn_cancel:hover {
                background: #fef2f2; color: #dc2626;
                border-color: #fecaca;
            }
            /* ═══ Boutons contact ═══ */
            QPushButton#btn_whatsapp {
                background: #25D366; color: #ffffff;
                border: 1px solid #1eb955;
                border-radius: 10px;
                padding: 12px 16px;
                font-size: 12px; font-weight: 700;
                text-align: left;
                min-height: 42px;
            }
            QPushButton#btn_whatsapp:hover { background: #1eb955; }
            QPushButton#btn_email {
                background: #dc2626; color: #ffffff;
                border: 1px solid #b91c1c;
                border-radius: 10px;
                padding: 12px 16px;
                font-size: 12px; font-weight: 700;
                text-align: left;
                min-height: 42px;
            }
            QPushButton#btn_email:hover { background: #b91c1c; }
            QPushButton#btn_facebook {
                background: #1877F2; color: #ffffff;
                border: 1px solid #1560c4;
                border-radius: 10px;
                padding: 12px 16px;
                font-size: 12px; font-weight: 700;
                text-align: left;
                min-height: 42px;
            }
            QPushButton#btn_facebook:hover { background: #1560c4; }
        """)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(14)

        # Header
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(14)

        icon = QtWidgets.QLabel()
        icon.setFixedSize(56, 56)
        icon.setAlignment(Qt.AlignCenter)
        icon.setText("🔐")
        icon.setStyleSheet("""
            QLabel {
                background: #eff6ff; border: 1px solid #bfdbfe;
                border-radius: 14px; font-size: 26px;
            }
        """)
        h.addWidget(icon)

        v_title = QtWidgets.QVBoxLayout()
        v_title.setSpacing(2)

        t1 = QtWidgets.QLabel("Activation de Nova Pharma")
        t1.setObjectName("title")
        v_title.addWidget(t1)

        t2 = QtWidgets.QLabel("Saisissez votre clé de licence pour continuer")
        t2.setObjectName("sub")
        v_title.addWidget(t2)

        h.addLayout(v_title)
        h.addStretch()
        root.addLayout(h)

        # Message d'erreur
        if message:
            err_lbl = QtWidgets.QLabel(message)
            err_lbl.setObjectName("error")
            err_lbl.setWordWrap(True)
            root.addWidget(err_lbl)

        # Carte Machine ID
        card_mid = QtWidgets.QFrame()
        card_mid.setObjectName("card")
        v_mid = QtWidgets.QVBoxLayout(card_mid)
        v_mid.setContentsMargins(18, 14, 18, 14)
        v_mid.setSpacing(8)

        lbl_mid = QtWidgets.QLabel("VOTRE MACHINE ID")
        lbl_mid.setStyleSheet(
            "color: #94a3b8; font-size: 10px; font-weight: 800; "
            "letter-spacing: 1px;")
        v_mid.addWidget(lbl_mid)

        mid = machine_id.get_machine_id()
        h_mid = QtWidgets.QHBoxLayout()
        h_mid.setSpacing(8)

        self.inp_mid = QtWidgets.QLineEdit(mid)
        self.inp_mid.setObjectName("mid_input")
        self.inp_mid.setReadOnly(True)
        h_mid.addWidget(self.inp_mid, 1)

        btn_copy = QtWidgets.QPushButton("📋")
        btn_copy.setFixedSize(38, 38)
        btn_copy.setCursor(Qt.PointingHandCursor)
        btn_copy.setToolTip("Copier le Machine ID")
        btn_copy.setStyleSheet("""
            QPushButton {
                background: #f8fafc; border: 1px solid #dbe3ec;
                border-radius: 8px; font-size: 14px;
            }
            QPushButton:hover { background: #eff6ff; }
        """)
        btn_copy.clicked.connect(
            lambda: QtWidgets.QApplication.clipboard().setText(mid))
        h_mid.addWidget(btn_copy)

        v_mid.addLayout(h_mid)

        hint = QtWidgets.QLabel(
            "Envoyez ce Machine ID à TEAM NOVA pour recevoir votre clé.")
        hint.setStyleSheet(
            "color: #94a3b8; font-size: 10px; font-style: italic;")
        hint.setWordWrap(True)
        v_mid.addWidget(hint)

        root.addWidget(card_mid)

        # Carte clé de licence
        card_key = QtWidgets.QFrame()
        card_key.setObjectName("card")
        v_key = QtWidgets.QVBoxLayout(card_key)
        v_key.setContentsMargins(18, 14, 18, 14)
        v_key.setSpacing(8)

        lbl_key = QtWidgets.QLabel("CLÉ DE LICENCE")
        lbl_key.setStyleSheet(
            "color: #94a3b8; font-size: 10px; font-weight: 800; "
            "letter-spacing: 1px;")
        v_key.addWidget(lbl_key)

        self.inp_key = QtWidgets.QLineEdit()
        self.inp_key.setPlaceholderText("NOVA-XXXX-XXXX-XXXX-XXXX")
        self.inp_key.setMinimumHeight(48)
        self.inp_key.returnPressed.connect(self._on_activate)
        v_key.addWidget(self.inp_key)

        root.addWidget(card_key)

        # ═══════════════════════════════════════════════════════════
        # NOUVEAU : Bloc "Besoin d'une licence ?"
        # ═══════════════════════════════════════════════════════════
        card_buy = QtWidgets.QFrame()
        card_buy.setObjectName("card")
        card_buy.setStyleSheet("""
            QFrame#card {
                background: #eff6ff;
                border: 1px solid #bfdbfe;
                border-radius: 12px;
            }
        """)
        v_buy = QtWidgets.QVBoxLayout(card_buy)
        v_buy.setContentsMargins(18, 14, 18, 14)
        v_buy.setSpacing(10)

        # Titre
        lbl_buy = QtWidgets.QLabel("💡 Besoin d'une licence ?")
        lbl_buy.setStyleSheet(
            "color: #023E8A; font-size: 13px; font-weight: 800;")
        v_buy.addWidget(lbl_buy)

        lbl_buy_sub = QtWidgets.QLabel(
            "Contactez TEAM NOVA pour obtenir votre clé d'activation :")
        lbl_buy_sub.setStyleSheet(
            "color: #1e40af; font-size: 11px;")
        v_buy.addWidget(lbl_buy_sub)

        # 3 boutons contact
        h_contact = QtWidgets.QHBoxLayout()
        h_contact.setSpacing(8)

        # WhatsApp
        btn_whatsapp = QtWidgets.QPushButton("  WhatsApp\n  +243 808 775 085")
        btn_whatsapp.setObjectName("btn_whatsapp")
        btn_whatsapp.setCursor(Qt.PointingHandCursor)
        btn_whatsapp.clicked.connect(self._open_whatsapp)
        h_contact.addWidget(btn_whatsapp, 1)

        # Email
        btn_email = QtWidgets.QPushButton("  Email\n  teamnovaoff@gmail.com")
        btn_email.setObjectName("btn_email")
        btn_email.setCursor(Qt.PointingHandCursor)
        btn_email.clicked.connect(self._open_email)
        h_contact.addWidget(btn_email, 1)

        # Facebook
        btn_facebook = QtWidgets.QPushButton("  Facebook\n  Team Nova")
        btn_facebook.setObjectName("btn_facebook")
        btn_facebook.setCursor(Qt.PointingHandCursor)
        btn_facebook.clicked.connect(self._open_facebook)
        h_contact.addWidget(btn_facebook, 1)

        v_buy.addLayout(h_contact)

        root.addWidget(card_buy)

        root.addStretch()

        # Boutons
        h_btn = QtWidgets.QHBoxLayout()
        h_btn.setSpacing(10)
        h_btn.addStretch()

        btn_cancel = QtWidgets.QPushButton("Annuler")
        btn_cancel.setObjectName("btn_cancel")
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.clicked.connect(self.reject)
        h_btn.addWidget(btn_cancel)

        self.btn_activate = QtWidgets.QPushButton("Activer")
        self.btn_activate.setMinimumWidth(140)
        self.btn_activate.setCursor(Qt.PointingHandCursor)
        self.btn_activate.setDefault(True)
        self.btn_activate.clicked.connect(self._on_activate)
        h_btn.addWidget(self.btn_activate)

        root.addLayout(h_btn)

    # ══════════════════════════════════════════════════════════════
    # Ouverture des canaux de contact
    # ══════════════════════════════════════════════════════════════
    def _open_whatsapp(self):
        from PySide6 import QtGui, QtCore
        url = QtCore.QUrl("https://wa.me/243808775085")
        QtGui.QDesktopServices.openUrl(url)

    def _open_email(self):
        from PySide6 import QtGui, QtCore
        url = QtCore.QUrl(
            "mailto:teamnovaoff@gmail.com"
            "?subject=Demande%20de%20licence%20Nova%20Pharma"
            f"&body=Bonjour%20TEAM%20NOVA,%0D%0A%0D%0A"
            f"Je%20souhaite%20acqu%C3%A9rir%20une%20licence%20Nova%20Pharma."
            f"%0D%0A%0D%0AMon%20Machine%20ID%20:%20"
            f"{machine_id.get_machine_id()}"
        )
        QtGui.QDesktopServices.openUrl(url)

    def _open_facebook(self):
        from PySide6 import QtGui, QtCore
        url = QtCore.QUrl(
            "https://web.facebook.com/people/Team-Nova/61581757163137/")
        QtGui.QDesktopServices.openUrl(url)

    def _on_activate(self):
        key = self.inp_key.text().strip().upper()

        if not key:
            QtWidgets.QMessageBox.warning(
                self, "Clé manquante", "Saisissez une clé de licence.")
            return

        ok, payload, msg = _verify_license(key)

        if not ok:
            QtWidgets.QMessageBox.critical(
                self, "Licence invalide", msg)
            return

        # Message adapté selon le type de licence
        if payload.get("lifetime"):
            message = (
                "✓ Licence À VIE activée !\n\n"
                "Nova Pharma est maintenant activé définitivement. "
                "Aucune expiration."
            )
        else:
            import datetime as _dt
            exp_ts = payload.get("exp", 0)
            exp_date = _dt.datetime.fromtimestamp(exp_ts).strftime("%d/%m/%Y")
            message = (
                f"✓ Licence activée !\n\n"
                f"Votre licence est valide jusqu'au {exp_date}."
            )

        if save_license(key):
            QtWidgets.QMessageBox.information(
                self, "Activation réussie", message)
            self.accept()
        else:
            QtWidgets.QMessageBox.critical(
                self, "Erreur", "Impossible d'enregistrer la licence.")