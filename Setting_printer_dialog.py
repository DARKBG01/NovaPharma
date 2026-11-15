#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_printer_dialog.py — Config imprimantes sur ce poste.
=============================================================
Accessible pour TOUS les rôles (y compris CAISSIER).
Configuration stockée en QSettings LOCAL (par PC).
"""

import logging

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import printer_manager

logger = logging.getLogger(__name__)


class PrinterConfigDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Imprimantes — Ce poste")
        from Ui_helpers import make_dialog_responsive
        make_dialog_responsive(self, 560, 520)
        self.setModal(True)
        self._build_ui()
        self._load()

    # ══════════════════════════════════════════════════════════════
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
            QLabel#section {
                color: #0f172a; font-size: 13px; font-weight: 800;
            }
            QFrame#card {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QComboBox {
                background: #f8fafc;
                border: 1.5px solid #dbe3ec;
                border-radius: 10px;
                padding: 8px 12px;
                color: #0f172a;
                font-size: 13px;
                min-height: 24px;
            }
            QComboBox:focus { border-color: #0077B6; }
            QPushButton {
                background: #0077B6; color: white;
                border: none; border-radius: 10px;
                padding: 8px 18px; font-weight: 700;
                font-size: 12px; min-width: 100px;
            }
            QPushButton:hover { background: #023E8A; }
            QPushButton#btn_secondary {
                background: transparent; color: #64748b;
                border: 1.5px solid #e2e8f0;
            }
            QPushButton#btn_secondary:hover {
                background: #fef2f2; color: #dc2626;
                border-color: #fecaca;
            }
        """)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        # Header
        t = QtWidgets.QLabel("Configuration des imprimantes")
        t.setObjectName("title")
        root.addWidget(t)

        s = QtWidgets.QLabel(
            "Chaque poste a sa propre configuration. "
            "Les noms d'imprimantes sont ceux du système.")
        s.setObjectName("sub")
        s.setWordWrap(True)
        root.addWidget(s)

        # Carte TICKET
        card_ticket = QtWidgets.QFrame()
        card_ticket.setObjectName("card")
        cv_t = QtWidgets.QVBoxLayout(card_ticket)
        cv_t.setContentsMargins(16, 14, 16, 14)
        cv_t.setSpacing(10)

        lbl_t = QtWidgets.QLabel("🎫 Ticket (80mm)")
        lbl_t.setObjectName("section")
        cv_t.addWidget(lbl_t)

        row_t = QtWidgets.QHBoxLayout()
        row_t.setSpacing(8)

        self.combo_ticket = QtWidgets.QComboBox()
        row_t.addWidget(self.combo_ticket, 1)

        btn_test_t = QtWidgets.QPushButton("Test")
        btn_test_t.clicked.connect(lambda: self._test("ticket"))
        row_t.addWidget(btn_test_t)

        cv_t.addLayout(row_t)
        root.addWidget(card_ticket)

        # Carte RAPPORT
        card_report = QtWidgets.QFrame()
        card_report.setObjectName("card")
        cv_r = QtWidgets.QVBoxLayout(card_report)
        cv_r.setContentsMargins(16, 14, 16, 14)
        cv_r.setSpacing(10)

        lbl_r = QtWidgets.QLabel("📄 Rapport (A4)")
        lbl_r.setObjectName("section")
        cv_r.addWidget(lbl_r)

        row_r = QtWidgets.QHBoxLayout()
        row_r.setSpacing(8)

        self.combo_report = QtWidgets.QComboBox()
        row_r.addWidget(self.combo_report, 1)

        btn_test_r = QtWidgets.QPushButton("Test")
        btn_test_r.clicked.connect(lambda: self._test("report"))
        row_r.addWidget(btn_test_r)

        cv_r.addLayout(row_r)
        root.addWidget(card_report)

        root.addStretch()

        # Footer
        hf = QtWidgets.QHBoxLayout()
        hf.addStretch()

        btn_cancel = QtWidgets.QPushButton("Fermer")
        btn_cancel.setObjectName("btn_secondary")
        btn_cancel.clicked.connect(self.reject)
        hf.addWidget(btn_cancel)

        btn_save = QtWidgets.QPushButton("Enregistrer")
        btn_save.clicked.connect(self._on_save)
        hf.addWidget(btn_save)

        root.addLayout(hf)

    # ══════════════════════════════════════════════════════════════
    def _load(self):
        """Charge imprimantes système + sélection actuelle."""
        try:
            printers = printer_manager.list_printers()

            self.combo_ticket.clear()
            self.combo_report.clear()

            if not printers:
                for c in (self.combo_ticket, self.combo_report):
                    c.addItem("(Aucune imprimante détectée)")
                    c.setEnabled(False)
                return

            # Ajoute option "désactiver"
            self.combo_ticket.addItem("(Aucune — désactiver)")
            self.combo_ticket.addItems(printers)

            self.combo_report.addItem("(Aucune — désactiver)")
            self.combo_report.addItems(printers)

            # Sélection actuelle
            cur_t = printer_manager.get_ticket_printer()
            if cur_t:
                idx = self.combo_ticket.findText(cur_t)
                if idx >= 0:
                    self.combo_ticket.setCurrentIndex(idx)

            cur_r = printer_manager.get_report_printer()
            if cur_r:
                idx = self.combo_report.findText(cur_r)
                if idx >= 0:
                    self.combo_report.setCurrentIndex(idx)

        except Exception:
            logger.exception("Erreur chargement imprimantes")

    def _test(self, kind: str):
        try:
            ok = printer_manager.test_print(kind=kind)
            if ok:
                QtWidgets.QMessageBox.information(
                    self, "Test réussi",
                    "Une page de test a été envoyée à l'imprimante.")
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Échec",
                    "Impossible d'imprimer. Vérifiez que l'imprimante "
                    "est allumée et connectée.")
        except Exception:
            logger.exception("Erreur test impression")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Erreur lors du test d'impression.")

    def _on_save(self):
        try:
            # Récupère les noms
            name_t = self.combo_ticket.currentText()
            if name_t.startswith("("):
                name_t = ""

            name_r = self.combo_report.currentText()
            if name_r.startswith("("):
                name_r = ""

            # Sauvegarde en QSettings (local poste)
            printer_manager.set_ticket_printer(name_t)
            printer_manager.set_report_printer(name_r)

            logger.info(
                "Imprimantes configurées sur ce poste : "
                "ticket=%s, report=%s", name_t or "(système)", name_r or "(système)")

            QtWidgets.QMessageBox.information(
                self, "Enregistré",
                f"Configuration enregistrée sur ce poste.\n\n"
                f"🎫 Ticket : {name_t or '(imprimante système)'}\n"
                f"📄 Rapport : {name_r or '(imprimante système)'}")

            self.accept()

        except Exception:
            logger.exception("Erreur sauvegarde imprimantes")
            QtWidgets.QMessageBox.critical(
                self, "Erreur", "Impossible d'enregistrer.")