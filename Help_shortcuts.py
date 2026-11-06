#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Help_shortcuts.py — Boîte de dialogue "Raccourcis clavier".
"""

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt


# ══════════════════════════════════════════════════════════════════
SHORTCUTS = [
    ("Fichier", [
        ("Ctrl + N", "Nouvelle facture"),
        ("Ctrl + Shift + C", "Nouveau client"),
        ("Ctrl + Shift + P", "Nouveau produit"),
        ("Ctrl + S", "Sauvegarder la base"),
        ("Ctrl + Q", "Quitter"),
    ]),
    ("Édition", [
        ("F5", "Actualiser toutes les données"),
        ("Ctrl + F", "Recherche rapide"),
        ("Ctrl + Shift + X", "Vider le panier"),
        ("Ctrl + K", "Recherche globale"),
        ("Ctrl + Alt + P", "Configurer l'imprimante"),
        ("Ctrl + Alt + T", "Modifier le taux de change (admin)"),  # ← AJOUT
    ]),
    ("Ventes", [
        ("Ctrl + F1", "Démarrer une vente"),
        ("Ctrl + F2", "Ventes du jour"),
        ("Ctrl + Shift + Z", "Clôturer la caisse (Rapport Z)"),
    ]),
    ("Stock", [
        ("Ctrl + P", "Voir les produits"),
        ("Ctrl + R", "Voir les ruptures"),
        ("Ctrl + B", "Nouveau BLF"),
        ("Ctrl + Shift + F", "Nouveau fournisseur"),
    ]),
    ("Rapports", [
        ("Ctrl + Alt + V", "Rapport Ventes"),
        ("Ctrl + Alt + E", "Rapport Équipe"),
        ("Ctrl + Alt + O", "Rapport Opérations"),
    ]),
    ("Administration", [
        ("Ctrl + U", "Utilisateurs"),
        ("Ctrl + A", "Audit"),
        ("Ctrl + Shift + B", "Sauvegarde immédiate"),
        ("Ctrl + ,", "Paramètres"),
    ]),
    ("Aide", [
        ("F1", "Guide utilisateur"),
        ("Ctrl + /", "Raccourcis clavier"),
        ("Ctrl + Shift + A", "À propos"),
    ]),
]


class HelpShortcutsDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Raccourcis clavier — Nova Pharma")
        self.setMinimumSize(720, 640)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet("""
            QDialog { background: #f0f4f8; }
            QLabel { color: #334155; background: transparent; }

            QLabel#header_title {
                color: #ffffff; font-size: 18px; font-weight: 800;
                background: transparent;
            }
            QLabel#header_sub {
                color: #CAF0F8; font-size: 11px;
                background: transparent;
            }
            QFrame#header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #023E8A, stop:0.5 #0077B6, stop:1 #00B4D8);
                border-top-left-radius: 14px;
                border-top-right-radius: 14px;
            }
            QFrame#card {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QLabel#section {
                color: #023E8A; font-size: 13px; font-weight: 800;
                background: transparent;
            }
            QLabel#shortcut_key {
                background: #f1f5f9;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 4px 10px;
                color: #0f172a;
                font-size: 11px;
                font-weight: 800;
                font-family: 'Courier New';
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0077B6, stop:1 #023E8A);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 28px;
                font-size: 13px;
                font-weight: 700;
                min-width: 120px;
            }
            QPushButton:hover { background: #023E8A; }
        """)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ─── Header ───
        header = QtWidgets.QFrame()
        header.setObjectName("header")
        header.setMinimumHeight(80)
        h = QtWidgets.QHBoxLayout(header)
        h.setContentsMargins(24, 16, 24, 16)
        h.setSpacing(14)

        ico = QtWidgets.QLabel("⌨")
        ico.setStyleSheet("font-size: 32px; background: transparent;")
        h.addWidget(ico)

        v = QtWidgets.QVBoxLayout()
        v.setSpacing(2)
        t1 = QtWidgets.QLabel("Raccourcis clavier")
        t1.setObjectName("header_title")
        v.addWidget(t1)
        t2 = QtWidgets.QLabel(
            "Toutes les actions disponibles via le clavier")
        t2.setObjectName("header_sub")
        v.addWidget(t2)
        h.addLayout(v)
        h.addStretch()
        root.addWidget(header)

        # ─── Scroll ───
        scroll = QtWidgets.QScrollArea()
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent;")

        content = QtWidgets.QWidget()
        content.setStyleSheet("background: transparent;")
        v_content = QtWidgets.QVBoxLayout(content)
        v_content.setContentsMargins(20, 20, 20, 20)
        v_content.setSpacing(14)

        for section, items in SHORTCUTS:
            card = QtWidgets.QFrame()
            card.setObjectName("card")
            v_card = QtWidgets.QVBoxLayout(card)
            v_card.setContentsMargins(20, 16, 20, 16)
            v_card.setSpacing(10)

            lbl = QtWidgets.QLabel(section)
            lbl.setObjectName("section")
            v_card.addWidget(lbl)

            for key, desc in items:
                row = QtWidgets.QHBoxLayout()
                row.setSpacing(14)

                key_lbl = QtWidgets.QLabel(key)
                key_lbl.setObjectName("shortcut_key")
                key_lbl.setMinimumWidth(160)
                key_lbl.setAlignment(Qt.AlignCenter)
                row.addWidget(key_lbl)

                desc_lbl = QtWidgets.QLabel(desc)
                desc_lbl.setStyleSheet(
                    "color: #475569; font-size: 12px; "
                    "background: transparent;")
                row.addWidget(desc_lbl, 1)

                v_card.addLayout(row)

            v_content.addWidget(card)

        v_content.addStretch()
        scroll.setWidget(content)
        root.addWidget(scroll, 1)

        # ─── Footer ───
        footer = QtWidgets.QFrame()
        footer.setStyleSheet(
            "background: #ffffff; "
            "border-top: 1px solid #e2e8f0;")
        footer.setMinimumHeight(70)
        hf = QtWidgets.QHBoxLayout(footer)
        hf.setContentsMargins(20, 14, 20, 14)
        hf.addStretch()

        btn = QtWidgets.QPushButton("Fermer")
        btn.clicked.connect(self.accept)
        hf.addWidget(btn)
        root.addWidget(footer)