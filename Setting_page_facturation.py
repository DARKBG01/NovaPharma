#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_page_facturation.py — Page Facturation standalone.
============================================================
Injectée dans `page_5` du MainWindow.
Expose tous ses widgets pour rester compatible avec le code existant.
"""

import logging
from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore

from Database import db
from Interface_page_facturation import Ui_PageFacturation

logger = logging.getLogger(__name__)


class PageFacturation(QtWidgets.QWidget, Ui_PageFacturation):

    def __init__(self, parent=None, user_id=None,
                 identifiant="", main_window=None):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.identifiant = identifiant
        self.main_window = main_window

        self._setup_icons()
        self._setup_date()
        self._setup_placeholders()

    # ══════════════════════════════════════════════════════════════
    def _setup_icons(self):
        """Charge les icônes SVG sur les headers de cartes."""
        def _load(label, svg, size=18):
            pix = QtGui.QPixmap(f":/Icon/Icons/{svg}.svg")
            if not pix.isNull():
                label.setPixmap(pix.scaled(
                    size, size,
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation))

        # Header principal (fond bleu → icône blanche)
        _load(self.ico_page_header, "receipt_white", 26)

        # Icônes de cartes (fond clair → icône bleue)
        _load(self.ico_card_client,       "user",           18)
        _load(self.ico_card_articles,     "pill",           18)
        _load(self.ico_card_panier,       "shopping-cart",  18)
        _load(self.ico_card_client_info,  "user",           18)
        _load(self.ico_card_resume,       "wallet",         18)

    # ══════════════════════════════════════════════════════════════
    def _setup_date(self):
        """Met à jour la date dans le header."""
        try:
            self.label_23_date.setText(
                datetime.now().strftime("%A %d %B %Y · %H:%M").capitalize())
        except Exception:
            logger.exception("Erreur mise à jour date")

    # ══════════════════════════════════════════════════════════════
    def _setup_placeholders(self):
        """Force les placeholders et la lisibilité."""
        try:
            self.edit_identification_client.setPlaceholderText("—")
            self.edit_numero_client.setPlaceholderText("—")
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════════
    def update_facture_header(self, numero: str, date_str: str):
        """Met à jour le N° facture et la date dans la bannière."""
        try:
            self.label_23.setText(
                f'<html><head/><body><p>'
                f'<span style=" font-size:14pt; font-weight:800; '
                f'color:#ffffff;">Nouvelle vente<br/></span>'
                f'<span style=" font-size:9pt; font-weight:600; '
                f'color:rgba(255,255,255,220);">'
                f'Facture N° {numero}</span></p></body></html>')
            self.label_23_date.setText(date_str)
        except Exception:
            logger.exception("Erreur update header")