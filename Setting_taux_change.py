#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_taux_change.py — Dialog accès rapide au taux de change.
================================================================
Accessible via Ctrl+Alt+T. Réservé ADMIN/OWNER/DEV.
"""

import logging

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import db
from Database.currency import get_config_devises, set_taux, to_usd

logger = logging.getLogger(__name__)


class Setting_taux_change(QtWidgets.QDialog):

    taux_modifie = QtCore.Signal(float)

    def __init__(self, parent=None, user_id=None,
                 user_name="", role="UTILISATEUR",
                 is_owner=False, is_developer=False):
        super().__init__(parent)
        self.setWindowTitle("Taux de change")
        self.setMinimumWidth(480)
        self.setModal(True)

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"

        # ═══ Permission ═══
        can_edit = (is_owner or is_developer
                    or (role or "").upper() == "ADMIN")
        if not can_edit:
            QtWidgets.QMessageBox.warning(
                self, "Accès refusé",
                "Seul un administrateur, propriétaire ou développeur "
                "peut modifier le taux de change.")
            QtCore.QTimer.singleShot(0, self.reject)
            return

        self._build_ui()
        self._load()

    def _build_ui(self):
        self.setStyleSheet("""
            QDialog { background: #f0f4f8; }
            QLabel { color: #334155; background: transparent; }
            QLabel#title {
                color: #023E8A; font-size: 18px; font-weight: 800;
            }
            QLabel#sub {
                color: #64748b; font-size: 11px;
            }
            QLabel#current {
                color: #15803d; font-size: 20px; font-weight: 800;
                background: #f0fdf4; border: 1px solid #bbf7d0;
                border-radius: 10px; padding: 14px;
            }
            QDoubleSpinBox {
                background: #f8fafc;
                border: 1.5px solid #dbe3ec;
                border-radius: 10px;
                padding: 10px 14px;
                color: #0f172a;
                font-size: 16px;
                font-weight: 700;
                min-height: 26px;
            }
            QDoubleSpinBox:focus { border-color: #0077B6; }
            QPushButton {
                background: #0077B6; color: white;
                border: none; border-radius: 10px;
                padding: 10px 24px; font-weight: 700;
                font-size: 13px; min-width: 120px;
            }
            QPushButton:hover { background: #023E8A; }
            QPushButton#btn_cancel {
                background: transparent; color: #64748b;
                border: 1.5px solid #e2e8f0;
            }
        """)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        t = QtWidgets.QLabel("💱 Taux de change")
        t.setObjectName("title")
        root.addWidget(t)

        s = QtWidgets.QLabel(
            "Définissez combien de FC vaut 1 USD. Ce taux est utilisé "
            "pour l'affichage des montants et les paiements USD.")
        s.setObjectName("sub")
        s.setWordWrap(True)
        root.addWidget(s)

        self.lbl_current = QtWidgets.QLabel("—")
        self.lbl_current.setObjectName("current")
        self.lbl_current.setAlignment(Qt.AlignCenter)
        root.addWidget(self.lbl_current)

        lbl_in = QtWidgets.QLabel("NOUVEAU TAUX (1 USD = X FC)")
        lbl_in.setStyleSheet(
            "color: #64748b; font-size: 11px; font-weight: 700; "
            "letter-spacing: 1px;")
        root.addWidget(lbl_in)

        self.spin_taux = QtWidgets.QDoubleSpinBox()
        self.spin_taux.setRange(1.0, 999999.99)
        self.spin_taux.setDecimals(2)
        self.spin_taux.setSuffix(" FC")
        self.spin_taux.setValue(2250.0)
        self.spin_taux.valueChanged.connect(self._on_preview)
        root.addWidget(self.spin_taux)

        self.lbl_preview = QtWidgets.QLabel("—")
        self.lbl_preview.setStyleSheet(
            "color: #64748b; font-size: 11px; font-style: italic;")
        root.addWidget(self.lbl_preview)

        root.addStretch()

        hf = QtWidgets.QHBoxLayout()
        hf.addStretch()

        btn_cancel = QtWidgets.QPushButton("Annuler")
        btn_cancel.setObjectName("btn_cancel")
        btn_cancel.clicked.connect(self.reject)
        hf.addWidget(btn_cancel)

        btn_save = QtWidgets.QPushButton("Enregistrer")
        btn_save.clicked.connect(self._on_save)
        hf.addWidget(btn_save)

        root.addLayout(hf)

    def _load(self):
        try:
            cfg = get_config_devises()
            taux = cfg["taux"]
            self.lbl_current.setText(
                f"Actuel : 1 USD = {taux:,.0f} FC".replace(",", " "))
            self.spin_taux.setValue(taux)
            self._on_preview()
        except Exception:
            logger.exception("Erreur chargement taux")

    def _on_preview(self):
        try:
            nouveau = self.spin_taux.value()
            # Aperçu : 10 000 FC
            eq = to_usd(10000, nouveau)
            self.lbl_preview.setText(
                f"Exemple : 10 000 FC ≈ $ {eq:,.2f}".replace(",", " "))
        except Exception:
            pass

    def _on_save(self):
        nouveau = self.spin_taux.value()

        if nouveau <= 0:
            QtWidgets.QMessageBox.warning(
                self, "Taux invalide", "Le taux doit être > 0.")
            return

        # Confirmation
        rep = QtWidgets.QMessageBox.question(
            self, "Confirmation",
            f"<b>Changer le taux de change ?</b><br><br>"
            f"Nouveau : <b>1 USD = {nouveau:,.0f} FC</b><br><br>"
            "Ce taux sera utilisé pour tous les calculs USD.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if rep != QtWidgets.QMessageBox.Yes:
            return

        ok = set_taux(nouveau, self.user_id, self.user_name)
        if ok:
            self.taux_modifie.emit(nouveau)
            QtWidgets.QMessageBox.information(
                self, "Taux enregistré",
                f"Le taux de change a été mis à jour : "
                f"1 USD = {nouveau:,.0f} FC".replace(",", " "))
            self.accept()
        else:
            QtWidgets.QMessageBox.critical(
                self, "Erreur", "Impossible d'enregistrer le taux.")