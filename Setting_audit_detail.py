#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_audit_detail.py — Fiche détail d'une entrée d'audit.
==============================================================
"""

import json
import logging

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Client.api_singleton import is_client_mode, get_api
from Database import db
from Interface_audit_detail import Ui_Dialog

logger = logging.getLogger(__name__)


class Setting_audit_detail(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, parent=None, entry_id=None):
        super().__init__(parent)
        self.setupUi(self)

        self.entry_id = entry_id
        self._entry = None

        self.btn_close.clicked.connect(self.accept)

        self._load_entry()
        self._refresh_ui()

    def _load_entry(self):
        try:
            if is_client_mode():
                api = get_api()
                self._entry = api.get_audit(self.entry_id)
            else:
                row = db.query_one(
                    "SELECT * FROM AuditLog WHERE id = ? LIMIT 1",
                    (self.entry_id,))
                self._entry = dict(row) if row else None
        except Exception:
            logger.exception("Erreur chargement entrée audit")
            self._entry = None

    def _refresh_ui(self):
        if not self._entry:
            self.val_action.setText("Entrée introuvable")
            return

        e = self._entry

        self.val_action.setText(e.get("action") or "—")
        self.val_user.setText(
            e.get("utilisateur_name") or e.get("utilisateur_id") or "—")
        self.val_date.setText(e.get("date_action") or "—")
        self.val_id.setText(e.get("id") or "—")
        self.val_machine.setText(e.get("machine_name") or "—")

        # Cible
        parts = []
        if e.get("cible_type"):
            parts.append(e["cible_type"])
        if e.get("cible_nom"):
            parts.append(e["cible_nom"])
        if e.get("cible_id"):
            parts.append(f"({e['cible_id']})")
        self.val_cible.setText(" — ".join(parts) or "—")

        # Détails JSON pretty
        self.txt_details.setPlainText(
            self._pretty_json(e.get("details")))

        # Avant / Après
        self.txt_avant.setPlainText(
            self._pretty_json(e.get("avant")) or "(aucun état avant)")
        self.txt_apres.setPlainText(
            self._pretty_json(e.get("apres")) or "(aucun état après)")

    @staticmethod
    def _pretty_json(value):
        if not value:
            return ""
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except Exception:
                return value
        try:
            return json.dumps(value, indent=2, ensure_ascii=False)
        except Exception:
            return str(value)